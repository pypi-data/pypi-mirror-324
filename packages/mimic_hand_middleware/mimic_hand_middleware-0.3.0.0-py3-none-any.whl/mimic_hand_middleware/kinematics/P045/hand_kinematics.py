"""
Implements the joint-to-tendon length kinematics of the P04 prototype.
"""

import copy
import os

import numpy as np
import yaml

from ...conversion_utils.P045 import p04
from .mcp_kinematics_simple import SimpleMCPKinematics

# Custom
from .pip_kinematics import PIPKinematics
from .thumb_kinematics import SimpleThumbKinematics


class HandKinematics:
    """
    Implements the full angle-to-tendon kinematics of the hand.
    """

    def __init__(self, yaml_name: str = 'p045.yaml') -> None:
        """
        Initializes the pip, mcp and thumb kinematics models based on the yaml
        parameter file of the hand.
        """
        self.yaml_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../../hand_definitions/yaml',
            yaml_name,
        )
        with open(self.yaml_path) as yaml_file:
            hand_kinematic_params = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        self._pip_kinematics = PIPKinematics(
            x=hand_kinematic_params['pip_joint_values']['x'],
            y=hand_kinematic_params['pip_joint_values']['y'],
            r=hand_kinematic_params['pip_joint_values']['r'],
            scale=hand_kinematic_params['pip_joint_values']['scale'],
        )
        self._mcp_kinematics = SimpleMCPKinematics(
            hand_kinematic_params['mcp_joint_values']
        )
        self._thumb_kinematics = SimpleThumbKinematics(
            hand_kinematic_params['thumb_joint_values']
        )
        self._pip_joint_idxes = p04.PIP_JOINT_IDXES
        self._pip_joint_idxes_swapped = copy.deepcopy(self._pip_joint_idxes)
        self._pip_joint_idxes_swapped[1], self._pip_joint_idxes_swapped[2] = (
            self._pip_joint_idxes_swapped[2],
            self._pip_joint_idxes_swapped[1],
        )
        self._mcp_joint_idxes = p04.MCP_JOINT_IDXES
        self._thumb_joint_idxes = p04.THUMB_JOINT_IDXES
        self._num_tendons = sum(
            [
                len(self._pip_joint_idxes),
                len(self._mcp_joint_idxes),
                len(self._thumb_joint_idxes),
            ]
        )
        self.spool_rad = hand_kinematic_params['spool_radius']

    def get_tendon_lengths_m_from_joint_angles_rad(
        self,
        angles_rad: np.ndarray,
        switch_middle_ring_pip: bool = False,
        switch_middle_ring_mcp: bool = False,
        prepend_0: bool = False,
    ) -> np.ndarray:
        """
        Takes in a joint angle array of shape (n_joints,) (in rad), and returns
        an array of the shape (n_motors,) (in meters).
        If prepend_0 is set, a 0 value is added at the beginning of the array
        to account for the extra unused motors for the wrist.
        """
        tendon_lengths = np.zeros((self._num_tendons))
        if switch_middle_ring_pip:
            tendon_lengths[self._pip_joint_idxes_swapped] = (
                self._pip_kinematics.get_tendon_length_from_angle(
                    angles=angles_rad[self._pip_joint_idxes]
                )
            )
        else:
            tendon_lengths[self._pip_joint_idxes] = (
                self._pip_kinematics.get_tendon_length_from_angle(
                    angles=angles_rad[self._pip_joint_idxes]
                )
            )

        # mcp array needs to be reshaped
        mcp_angles = np.zeros((4, 2))
        mcp_angles[:, 0] = angles_rad[self._mcp_joint_idxes][::2]
        mcp_angles[:, 1] = angles_rad[self._mcp_joint_idxes][1::2]
        tendon_lengths[self._mcp_joint_idxes] = (
            self._mcp_kinematics.get_tendon_length_from_angle(
                angles=mcp_angles,
                switch_middle_ring=switch_middle_ring_mcp,
            )
        )
        tendon_lengths[self._thumb_joint_idxes] = (
            self._thumb_kinematics.get_tendon_length_from_angle(
                angles=angles_rad[self._thumb_joint_idxes]
            )
        )
        if prepend_0:
            tendon_lengths = np.insert(tendon_lengths, 0, 0.0, axis=0)
        return tendon_lengths
