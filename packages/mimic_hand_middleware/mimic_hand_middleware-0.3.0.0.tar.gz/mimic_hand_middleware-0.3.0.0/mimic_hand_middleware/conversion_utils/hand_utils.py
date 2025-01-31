"""Utilities for all hand prototypes of mimic.

Utility functions and values shared between all hands we make.
Made by Ben Forrai (ben.forrai@mimicrobotics.com)
"""

# Standard
import importlib
import os
from enum import Enum
from pathlib import Path

import defusedxml.ElementTree as ET

# Third-party
import numpy as np

# Local
from mimic_hand_api.rp2040_api import HandChirality, parse_hand_id

# Constants
MAX_HANDS = 5
HAND_CALIBRATION_FOLDER = Path.home() / '.mimic' / 'calibration' / 'hand'
PROTOTYPE_UTILS_MAP = {
    'P0.44': 'mimic_hand_middleware.conversion_utils.P045.p04',
    'P0.45': 'mimic_hand_middleware.conversion_utils.P045.p04',
    'P0.46': 'mimic_hand_middleware.conversion_utils.P046.p046',
    'P0.50': 'mimic_hand_middleware.conversion_utils.P050.p05',
}

KINEMATICS_UTILS_MAP = {
    'P0.44': 'mimic_hand_middleware.kinematics.P045',
    'P0.45': 'mimic_hand_middleware.kinematics.P045',
    'P0.46': 'mimic_hand_middleware.kinematics.P046',
    'P0.50': 'mimic_hand_middleware.kinematics.P050',
}


def get_urdf_path(prototype: str) -> str:
    """Return the path to the kinematic description based on prototype name.

    Gets the path to the kinematic description to the robot hand in the
    mimic_viz ROS2 package if we're using ROS. If not, the urdf is loaded from
    the middleware directory.
    """
    # check is the MIMIC_USE_ROS env variable exists and is set
    if 'MIMIC_USE_ROS' in os.environ:
        from ament_index_python.packages import get_package_share_directory

        resources_path = get_package_share_directory('mimic_viz')
    else:
        script_path = os.path.dirname(os.path.realpath(__file__))
        resources_path = os.path.join(script_path, '../hand_definitions')
    urdf_path = os.path.join(resources_path, f'urdf/{prototype}/converted.urdf')
    return urdf_path


def parse_urdf(urdf_path: str) -> list:
    """Get a list of all the joints from a .urdf file

    Iterate through all joints in a .urdf, and if they are not constant offset
    joints (denoted by _offset at the end of the joint name), add them to a
    list that is returned.
    """
    # get full list from the .urdf file
    joint_names = []
    tree = ET.parse(urdf_path)
    root = tree.getroot()
    for joint in root.iter('joint'):
        joint_name = joint.attrib['name']
        if not joint_name.endswith('offset'):
            joint_names.append(joint_name)
    return joint_names


def map_prototype_name_to_utils_path(prototype_name: str) -> str:
    """Map the prototype name to the path to its utils module.

    :param prototype_name: The name of the prototype.
    :return: The utils path in string format, relative to
        mimic_hand_middleware/conversion_utils.
    """
    prototype_utils_path = PROTOTYPE_UTILS_MAP.get(prototype_name, None)
    assert (
        prototype_utils_path is not None
    ), f'No utils found for prototype {prototype_name}'

    return prototype_utils_path


def get_prototype_utils_library(prototype_name: str) -> 'HandUtils':
    """Get the utils library for the given prototype name."""
    prototype_utils_path = map_prototype_name_to_utils_path(prototype_name)
    prototype_utils_module = importlib.import_module(prototype_utils_path)
    prototype_utils_module.init_matrices()
    return prototype_utils_module


def get_hand_chirality_from_str(hand_chirality_str: str) -> HandChirality:
    """Parse a string to a HandChirality enum.

    If str is 'right'/'left' (whitespace and upper/lowercase does not matter),
    return the adequate HandChirality. If not, raise a ValueError.
    """
    hand_chirality_str = hand_chirality_str.strip().lower()
    if hand_chirality_str == 'right':
        return HandChirality.RIGHT
    elif hand_chirality_str == 'left':
        return HandChirality.LEFT
    else:
        err_msg = f'String {hand_chirality_str} could not be converted to right/left!'
        raise ValueError(err_msg)


def map_prototype_name_to_kinematics_path(prototype_name: str) -> str:
    """Map the prototype name to the path to its kinematics module.

    :param prototype_name: The name of the prototype.
    :return: The kinematics path in string format, relative to
        mimic_hand_middleware/kinematics.
    """
    kinematics_utils_path = KINEMATICS_UTILS_MAP.get(prototype_name, None)
    assert (
        kinematics_utils_path is not None
    ), f'No kinematics found for prototype {prototype_name}'
    return kinematics_utils_path


def get_calibration_path(prototype_name: str) -> Path:
    """Get the path to the calibration file for the hand.

    :param prototype_name: The name of the prototype.
    :return: The path to the calibration file in string format.
    """
    prototype_name = prototype_name.split('_')[0]
    prototype_name = prototype_name.replace('.', '_')
    return HAND_CALIBRATION_FOLDER / f'{prototype_name}_motor_config.yaml'


class AngleRepresentation(Enum):
    """Represent angles in either rad/deg.

    simple enum for denoting rad/deg representations used during motor cmds.
    """

    RAD = 0
    DEG = 1
