"""MCP kinematics for the P046 hand.

This file implements the MCP (metacarpophalangeal) kinematics of the P046 hand
through the MCPKinematics class. The class has the following public
functions:
- get_tendon_length_from_angle: calculate desired (calibrated) tendon lengths
    from a set of joint angles.

Written by Ben Forrai (ben.forrai@mimicrobotics.com) on 29.01.25.
Project reference R0007
"""
# Standard imports

# Third-party
import numpy as np

# Custom
from .finger_kinematics import FingerKinematics


class MCPKinematics(FingerKinematics):
    """Represent the MCP kinematics of the P046 hand.

    A class for representing a simplified version of MCP kinematics of P04
    The simplified version merely takes the mean and the difference of the
    two opposing tendons and uses them to control the MCP flexion and abduction
    respectively.
    """

    def __init__(
        self: 'MCPKinematics', mcp_joint_init_dict: dict, mcp_base_dimension: int = 4
    ) -> None:
        """Create the MCPKinematics instance.

        :param: self: the MCPKinematics instance.
        :type: MCPKinematics
        :param: mcp_joint_init_dict: dictionary of the kinematic parameters
            for the MCP joints.
        :type: dict
        :param: mcp_base_dimension: number of MCP joints. A normal hand has 4,
            the thumb is handled separately.
        :type: int
        :return: None
        """
        super().__init__()
        self._base_dim = mcp_base_dimension
        self._abd_multiplier = mcp_joint_init_dict['abduction_multiplier']
        self._flex_multiplier = mcp_joint_init_dict['flexion_multiplier']
        # get tendon lengths in the center pos of the motors
        self._tendon_lengths_at_zero = np.zeros(mcp_base_dimension * 2)
        self._tendon_lengths_at_zero = self.get_tendon_length_from_angle(
            np.zeros((mcp_base_dimension, 2)),
        )

    def get_tendon_length_from_angle(
        self: 'MCPKinematics',
        angles: np.ndarray,
    ) -> np.ndarray:
        """Derive (calibrated) tendon length from the desired angle.

        Derive tendon length from the desired angle. The np array angles is assumed
        to be of shape (n_joints, 2), with its first column being used for abduction
        angles (psi) and its second column used for flexion angles (omega).
        Both are in randians.

        :param: self: the MCPKinematics instance.
        :type: MCPKinematics
        :param: angles: the desired angles in radians, in shape (n_joints, 2).
        :type: np.ndarray
        :return: the calibrated tendon lengths in meters, in shape (n_joints,).
        :rtype: np.ndarray
        """
        if angles.shape[0] != self._base_dim:
            angle_shape_err_msg = (
                f'The shape of the angles {angles.shape} is incompatible with',
                ' the shape of the transform matrices stack ',
                f' {self._transform_matrices_B_to_T.shape}!',
            )
            raise ValueError(angle_shape_err_msg)
        abd_angles = angles[:, 0]
        flex_angles = angles[:, 1]
        deltas = self._abd_multiplier * abd_angles
        means = self._flex_multiplier * flex_angles
        tendon_lengths = np.zeros_like(self._tendon_lengths_at_zero)
        tendon_lengths[::2] = means - deltas
        tendon_lengths[1::2] = means + deltas
        tendon_lengths -= self._tendon_lengths_at_zero
        return tendon_lengths
