import numpy as np

from .finger_kinematics import FingerKinematics


class SimpleThumbKinematics(FingerKinematics):
    """
    A class that represents the simplified kinematics of the thumb joints.
    """

    def __init__(self, thumb_joint_dict) -> None:
        super().__init__()
        # load simple init constants
        self._abd_multiplier = thumb_joint_dict['simple']['abd_multiplier']
        self._cmc_multiplier = thumb_joint_dict['simple']['cmc_multiplier']
        self._pp_multiplier = thumb_joint_dict['simple']['pp_multiplier']
        self._pp_offset = thumb_joint_dict['simple']['pp_offset']
        self._pip_multiplier = thumb_joint_dict['simple']['pip_multiplier']
        self._pip_offset = thumb_joint_dict['simple']['pip_offset']
        self._cmc_offset = thumb_joint_dict['simple']['cmc_offset']
        self._abd_offset = thumb_joint_dict['simple']['abd_offset']

    def get_tendon_length_from_angle(self, angles: np.ndarray) -> np.ndarray:
        """
        Derive tendon length from the desired angle
        angles is assumed to be of shape (n_joints), in radians.
        Returns the desired tendon length change from the zero position, in
        meters.
        """
        angles = angles.reshape((-1,))
        assert angles.shape[0] == 4, (
            'The shape of the commanded thumb'
            + f'array has to be castable to (4,). It is currently {angles.shape}'
        )
        tendon_cmds = np.zeros_like(angles)
        tendon_cmds[0] = (angles[0] + self._cmc_offset) * self._cmc_multiplier
        tendon_cmds[1] = (angles[1] + self._abd_offset) * self._abd_multiplier
        tendon_cmds[2] = (angles[2] + self._pip_offset) * self._pip_multiplier
        tendon_cmds[3] = (angles[3] + self._pp_offset) * self._pp_multiplier
        return tendon_cmds
