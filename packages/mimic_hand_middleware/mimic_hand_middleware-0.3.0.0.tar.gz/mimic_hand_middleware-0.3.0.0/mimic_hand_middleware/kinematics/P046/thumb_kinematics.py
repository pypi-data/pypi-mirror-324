"""Class for representing the thumb kinematics of the P046 hand.

Implements the simplified thumb kinematics of the P046 hand where each joint
is controlled independently with a simple linear scaling + offset between the
desired joint and the commanded tendon length. It is assumed that the thumb has 4
joints (cmc, abd, pip, pp). The class has the following public
functions:
- get_tendon_length_from_angle: calculate desired (calibrated) tendon lengths
    from a set of joint angles.

Written by Ben Forrai (ben.forrai@mimicrobotics.com) on 29.01.25.
Project reference R0007
"""

# Third-party
import numpy as np

# Custom
from .finger_kinematics import FingerKinematics

NUM_OF_THUMB_JOINTS = 4
CMC_JOINT_IDX = 0
ABD_JOINT_IDX = 1
PIP_JOINT_IDX = 2
PP_JOINT_IDX = 3


class ThumbKinematics(FingerKinematics):
    """Represent the simplified kinematics of the thumb joints."""

    def __init__(self: 'ThumbKinematics', thumb_joint_dict: dict) -> None:
        """Create the ThumbKinematics instance.

        :param: thumb_joint_dict: dictionary of the kinematic parameters for the
            thumb joints.
        :type: dict
        :return: None
        """
        super().__init__()
        # load simple init constants
        self._cmc_joint_rolling_radius = thumb_joint_dict['cmc_joint_rolling_radius']
        self._abd_joint_rolling_radius = thumb_joint_dict['abd_joint_rolling_radius']
        self._pulley_rolling_radius = thumb_joint_dict['pulley_rolling_radius']
        self._pip_joint_rolling_radius = thumb_joint_dict['pip_joint_rolling_radius']
        self._pp_joint_rolling_radius = thumb_joint_dict['pp_joint_rolling_radius']

    def get_tendon_length_from_angle(
        self: 'ThumbKinematics',
        angles: np.ndarray,
    ) -> np.ndarray:
        """Derive a calibrated tendon length (m) from the desired angle (rad).

        Derive tendon length from the desired angle. The np array angles is assumed
        to be of shape (4,) and in radians.

        :param: self: the ThumbKinematics instance.
        :type: ThumbKinematics
        :param: angles: the desired angles in radians, in shape (4,).
        :type: np.ndarray
        :return: the calibrated tendon lengths in meters, in shape (4,).
        :rtype: np.ndarray
        """
        angles = angles.reshape((-1,))
        if angles.shape[0] != NUM_OF_THUMB_JOINTS:
            shape_err_msg = (
                'The shape of the commanded thumb',
                'angles has to be castable to (4,). It is currently',
                f'{angles.shape}',
            )
            raise ValueError(shape_err_msg)
        tendon_cmds = np.zeros_like(angles)
        tendon_cmds[CMC_JOINT_IDX] = (
            -angles[CMC_JOINT_IDX] * self._cmc_joint_rolling_radius
        )
        tendon_cmds[ABD_JOINT_IDX] = -(
            angles[ABD_JOINT_IDX] * self._abd_joint_rolling_radius
            + angles[CMC_JOINT_IDX] * self._pulley_rolling_radius
        )
        tendon_cmds[PIP_JOINT_IDX] = (
            angles[PIP_JOINT_IDX] * self._pip_joint_rolling_radius
            + (-angles[CMC_JOINT_IDX] + angles[ABD_JOINT_IDX])
            * self._pulley_rolling_radius
        )
        tendon_cmds[PP_JOINT_IDX] = (
            angles[PP_JOINT_IDX] * self._pp_joint_rolling_radius
            + (-angles[CMC_JOINT_IDX] + angles[ABD_JOINT_IDX] + angles[PIP_JOINT_IDX])
            * self._pulley_rolling_radius
        )
        return tendon_cmds
