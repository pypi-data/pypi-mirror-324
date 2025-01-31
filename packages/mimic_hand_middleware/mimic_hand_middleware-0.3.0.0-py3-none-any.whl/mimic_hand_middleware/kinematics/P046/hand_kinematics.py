"""Get tendon lengths from joint angles on P046 series hands.

This file implements the joint-to-tendon length kinematics of the P04 prototype.
Its main class, the HandKinematics class provides the following public functions:
- get_tendon_lengths_m_from_joint_angles_rad: calculate desired (calibrated) tendon
    lengths from a set of joint angles. Both the input and the output is a np array,
    with shape (num_tendons,)

Written by Ben Forrai (ben.forrai@mimicrobotics.com) on 29.01.25.
Project reference R0007
"""

# Standard
import copy
from pathlib import Path

# Third-party
import numpy as np
import yaml

from mimic_hand_middleware.conversion_utils.P046 import p046

from .mcp_kinematics import MCPKinematics

# Custom
from .pip_kinematics import PIPKinematics
from .thumb_kinematics import ThumbKinematics


class HandKinematics:
    """Implement the full angle-to-tendon kinematics of the P046 hand."""

    def __init__(self: 'HandKinematics', yaml_name: str = 'p046.yaml') -> None:
        """Create the HandKinematics instance.

        Initializes the pip, mcp and thumb kinematics models based on the yaml
        parameter file of the hand.

        :param: yaml_name: name of the kinematic constant yaml to load.
        :type: str
        :return: None
        """
        self.yaml_path = (
            Path(__file__).parent.parent.parent
            / 'hand_definitions'
            / 'yaml'
            / yaml_name
        )
        with Path.open(self.yaml_path) as yaml_file:
            hand_kinematic_params = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        self._pip_kinematics = PIPKinematics(
            hand_kinematic_params['pip_joint_values'],
        )
        self._mcp_kinematics = MCPKinematics(
            hand_kinematic_params['mcp_joint_values'],
        )
        self._thumb_kinematics = ThumbKinematics(
            hand_kinematic_params['thumb_joint_values'],
        )
        self._pip_joint_idxes = p046.PIP_JOINT_IDXES
        self._pip_joint_idxes_swapped = copy.deepcopy(self._pip_joint_idxes)
        self._pip_joint_idxes_swapped[1], self._pip_joint_idxes_swapped[2] = (
            self._pip_joint_idxes_swapped[2],
            self._pip_joint_idxes_swapped[1],
        )
        self._mcp_joint_idxes = p046.MCP_JOINT_IDXES
        self._thumb_joint_idxes = p046.THUMB_JOINT_IDXES
        self._num_tendons = sum(
            [
                len(self._pip_joint_idxes),
                len(self._mcp_joint_idxes),
                len(self._thumb_joint_idxes),
            ],
        )
        self.spool_rad = hand_kinematic_params['spool_radius']

    def get_tendon_lengths_m_from_joint_angles_rad(
        self: 'HandKinematics',
        angles_rad: np.ndarray,
    ) -> np.ndarray:
        """Convert desired joint angles to calibrated tendon length commands.

        Takes in a joint angle array of shape (n_joints,) (in rad), and returns
        an array of the shape (n_motors,) (in meters).

        :param: angles_rad: desired joint angles in randians, assumed to be of
            shape (num_of_tendons).
        :type: np.ndarray
        """
        tendon_lengths = np.zeros(self._num_tendons)
        tendon_lengths[self._pip_joint_idxes] = (
            self._pip_kinematics.get_tendon_length_from_angle(
                angles=angles_rad[self._pip_joint_idxes],
            )
        )

        # mcp array needs to be reshaped
        mcp_angles = np.zeros((4, 2))
        mcp_angles[:, 0] = angles_rad[self._mcp_joint_idxes][::2]
        mcp_angles[:, 1] = angles_rad[self._mcp_joint_idxes][1::2]
        tendon_lengths[self._mcp_joint_idxes] = (
            self._mcp_kinematics.get_tendon_length_from_angle(
                angles=mcp_angles,
            )
        )
        tendon_lengths[self._thumb_joint_idxes] = (
            self._thumb_kinematics.get_tendon_length_from_angle(
                angles=angles_rad[self._thumb_joint_idxes],
            )
        )
        return tendon_lengths
