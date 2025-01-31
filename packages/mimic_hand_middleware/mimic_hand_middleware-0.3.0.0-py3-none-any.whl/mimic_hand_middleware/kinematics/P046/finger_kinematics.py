"""Represent finger kinematics for the prototype P046.

Contains an abstract class for representing finger kinematics and dynamics.
Written by Ben Forrai (ben.forrai@mimicrobotics.com), 29.01.25
"""

import abc

import numpy as np


class FingerKinematics:
    """Implement finger kinematics on an abstract level."""

    def __init__(self: 'FingerKinematics') -> None:
        """Initialize a dummy finger group."""

    @abc.abstractmethod
    def get_tendon_length_from_angle(
        self: 'FingerKinematics', angles: np.ndarray
    ) -> np.ndarray:
        """Calculate tendon lengthes from joint angles.

        Calculates the tendon length(s) from the given joint angle(s) along a
        batched dimension. Abstract method, so it shouldn't be called in itself.

        :param: self
        :type: FingerKinematics
        :param: angles: motor angles in radians
        :type: np.ndarray
        :return: calculated tendon lengths (in meters)
        :rtype: np.ndarray
        """
        return angles

    @abc.abstractmethod
    def get_angle_from_tendon_length(
        self: 'FingerKinematics', tendons: np.ndarray
    ) -> np.ndarray:
        """Calculate joint angles from tendon lengths.

        Calculates the joint angle(s) from the given tendon length(s) along a
        batched dimension. Abstract method, so it shouldn't be called in itself.

        :param: self
        :type: FingerKinematics
        :param: tendons: tendon length array in meters.
        :type: np.ndarray
        :return: calculated motor angles in radians
        :rtype: np.ndarray
        """
        return tendons
