# Standard imports
from copy import deepcopy

# Third-party
import numpy as np

# Custom
from .finger_kinematics import FingerKinematics


class SimpleMCPKinematics(FingerKinematics):
    """
    A class for representing a simplified version of MCP kinematics of P04
    The simplified version merely takes the mean and the difference of the
    two opposing tendons and uses them to control the MCP flexion and abduction
    respectively.
    """

    def __init__(self, mcp_joint_init_dict: dict, mcp_base_dimension: int = 4) -> None:
        super().__init__()
        self._base_dim = mcp_base_dimension
        self._abd_multiplier = mcp_joint_init_dict['simple']['abduction_multiplier']
        self._flex_multiplier = mcp_joint_init_dict['simple']['flexion_multiplier']
        # get tendon lengths in the center pos of the motors
        self._tendon_lengths_at_zero = np.zeros(mcp_base_dimension * 2)
        self._tendon_lengths_at_zero = self.get_tendon_length_from_angle(
            np.zeros((mcp_base_dimension, 2))
        )

    def get_tendon_length_from_angle(
        self,
        angles: np.ndarray,
        switch_middle_ring: bool = False,
        swap_dir_on_mcp_abd: bool = False,
    ) -> np.ndarray:
        """
        Derive tendon length from the desired angle
        angles is assumed to be of shate (n_joints, 2), with its first column
        being used for abduction angles (psi) and its second column used for
        flexion angles (omega). Both are in randians.
        """
        assert angles.shape[0] == self._base_dim, (
            f'The shape of the angles {angles.shape} is incompatible with'
            + ' the shape of the transform matrices stack '
            + f' {self._transform_matrices_B_to_T.shape}!'
        )
        # switch ring/middle if specified
        if switch_middle_ring:
            switched_angles = deepcopy(angles)
            angles[-2, :] = switched_angles[-3, :]
            angles[-3, :] = switched_angles[-2, :]
        abd_angles = angles[:, 0]
        if swap_dir_on_mcp_abd:
            # invert all abd angles - motor flipped
            abd_angles *= -1
        flex_angles = angles[:, 1]
        deltas = self._abd_multiplier * abd_angles
        means = self._flex_multiplier * flex_angles
        tendon_lengths = np.zeros_like(self._tendon_lengths_at_zero)
        tendon_lengths[::2] = means - deltas
        tendon_lengths[1::2] = means + deltas
        tendon_lengths -= self._tendon_lengths_at_zero
        return tendon_lengths
