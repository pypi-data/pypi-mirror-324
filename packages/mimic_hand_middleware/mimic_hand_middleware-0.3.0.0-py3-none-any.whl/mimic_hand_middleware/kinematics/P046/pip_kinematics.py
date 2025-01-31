"""Class for representing the PIP joint kinematics of the P046 hand.

A class for representing the PIP joint kinematics of the P046 hand. Its
public functions are:
- get_tendon_length_from_angle: calculate desired (calibrated) tendon lengths
    from a set of joint angles.

Written by Ben Forrai (ben.forrai@mimicrobotics.com) on 29.01.25.
Project reference R0007
"""

import numpy as np

from .finger_kinematics import FingerKinematics


class PIPKinematics(FingerKinematics):
    """Represent the PIP joint kinematics and dynamics of the P046 hand."""

    def __init__(self: 'PIPKinematics', pip_joint_dict: dict) -> None:
        """Create the PIPKinematics instance.

        :param: pip_joint_dict: dictionary of the kinematic parameters for the PIP
            joints.
        :type: dict
        :return: None
        """
        super().__init__()
        self._pip_joint_rolling_radius = pip_joint_dict['pip_joint_rolling_radius']
        self._mcp_pulley_rolling_radius = pip_joint_dict['mcp_pulley_rolling_radius']
        self.tendon_length_at_zero = 0.0
        self.tendon_length_at_zero = self.get_tendon_length_from_angle(np.array([0.0]))

    def get_tendon_length_from_angle(
        self: 'PIPKinematics',
        angles: np.ndarray,
        mcp_flex_angles: np.ndarray = None,
    ) -> np.ndarray:
        """Derive tendon stroke length [m] from the desired angle [rad]."""
        # initialize empty lengths
        tendon_lengths = np.zeros_like(angles)
        # convert length from desired angle and the radius of the rolling
        # surface the tendon rolls over
        tendon_lengths = angles * self._pip_joint_rolling_radius
        # if mcp_flex_angles are given, correct for them
        if mcp_flex_angles is not None:
            tendon_lengths = (
                tendon_lengths - mcp_flex_angles * self._mcp_pulley_rolling_radius
            )
        # shift so we get a length of 0 for a angle of 0
        return tendon_lengths - self.tendon_length_at_zero
