"""
Contains an abstract class for representing finger kinematics and dynamics.
"""

import numpy as np


class FingerKinematics:
    def __init__(self) -> None:
        pass

    def get_tendon_length_from_angle(self, angles: np.ndarray) -> np.ndarray:
        """
        Calculates the tendon length(s) from the given joint angle(s) along a
        batched dimension.
        """
        return angles

    def get_angle_from_tendon_length(self, tendons: np.ndarray) -> np.ndarray:
        """
        Calculates the joint angle(s) from the given tendon length(s) along a
        batched dimension.
        """
        return tendons
