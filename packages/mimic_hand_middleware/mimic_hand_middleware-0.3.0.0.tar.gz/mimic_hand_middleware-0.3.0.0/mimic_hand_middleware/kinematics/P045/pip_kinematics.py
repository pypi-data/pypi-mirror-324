"""
Scripts capturing the tendon-joint angle dynamics of the PIP joint on the P04
hand prototype.
"""

import numpy as np

from .finger_kinematics import FingerKinematics


class PIPKinematics(FingerKinematics):
    """
    Class for representing PIP joint kinematics and dynamics
    """

    def __init__(self, x, y, r, scale=1.0) -> None:
        super().__init__()
        self.x = x  # tendon start points in x axis
        self.y = y  # tendon start points along y axis
        self.r = r  # joint rad
        self.scale = scale
        self.tendon_length_at_zero = 0.0
        self.phi_dash = self._get_phi_dash()
        self.max_tangent_len = self._get_maximal_free_tendon_length()
        self.tendon_length_at_zero = self.get_tendon_length_from_angle(np.array([0.0]))

    def _get_phi_dash(self) -> float:
        """
        Calculate the angle phi_dash, which is the point where the tendon no
        longer is tangent to the joint.
        """
        hypotenuse = np.sqrt((self.y + self.r) ** 2 + self.x**2)
        phi_dash_ = np.arccos(self.r / hypotenuse) + np.arcsin(self.x / hypotenuse)
        phi_dash = np.pi - phi_dash_
        return phi_dash

    def _get_maximal_free_tendon_length(self) -> float:
        """
        Calculate the maximal tangent lenght
        """
        max_free = np.sqrt(
            np.square(self.x - self.r * np.sin(self.phi_dash))
            + np.square(self.y + self.r * (1 + np.cos(self.phi_dash)))
        )
        return max_free

    def _get_tendon_length_from_tangent_angle(self, angles: np.ndarray) -> np.ndarray:
        """
        Get tendon lengths from an angle that is smaller than self.phi_dash
        """
        # get the part of the tendon that is tangent to the joint
        angles = self.phi_dash - angles
        # the "free" tendon length is self.max_tangent_len
        tendon_lengths = angles * self.r + self.max_tangent_len
        return tendon_lengths

    def _get_tendon_length_from_large_angle(self, angles: np.ndarray) -> np.ndarray:
        """
        Get tendon lengths from large angles (>self.phi_dash)
        """
        tendon_length = np.sqrt(
            np.square(self.x - self.r * np.sin(angles))
            + np.square(self.y + self.r * (1 + np.cos(angles)))
        )
        return tendon_length

    def get_tendon_length_from_angle(self, angles: np.ndarray) -> np.ndarray:
        """
        Derive tendon length from the desired angle
        """
        tendon_lengths = np.zeros_like(angles)
        # angles smaller than phi_dash
        tendon_lengths[angles < self.phi_dash] = (
            self._get_tendon_length_from_tangent_angle(angles[angles < self.phi_dash])
        )
        # angles larger or equal to phi_dash
        tendon_lengths[angles >= self.phi_dash] = (
            self._get_tendon_length_from_large_angle(angles[angles >= self.phi_dash])
        )
        # TODO remove ugly scaling later
        tendon_lengths *= self.scale
        # shift so we get a length of 0 for a angle of 0
        tendon_lengths = tendon_lengths - self.tendon_length_at_zero
        return tendon_lengths
