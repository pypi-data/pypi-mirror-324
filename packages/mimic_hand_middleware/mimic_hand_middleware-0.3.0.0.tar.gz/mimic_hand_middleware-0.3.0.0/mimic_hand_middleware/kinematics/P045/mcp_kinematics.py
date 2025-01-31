import numpy as np

from .finger_kinematics import FingerKinematics


class MCPKinematics(FingerKinematics):
    """
    A class for representing MCP kinematics of P04
    """

    def __init__(self, mcp_joint_init_dict: dict, mcp_base_dimension: int = 4) -> None:
        super().__init__()
        self._h_1 = mcp_joint_init_dict['h_1']
        self._h_2 = mcp_joint_init_dict['h_2']
        tendon_position_names = [
            'sfr',
            'sfl',
            'sbr',
            'sbl',
            'mbr',
            'mbl',
            'efr',
            'efl',
            'ebr',
            'ebl',
        ]
        # initialize tendon end and beginning local coords
        for tendon_pos_name in tendon_position_names:
            current_vector = np.array(
                [
                    mcp_joint_init_dict[f'r_{tendon_pos_name}']['x'],
                    mcp_joint_init_dict[f'r_{tendon_pos_name}']['y'],
                    mcp_joint_init_dict[f'r_{tendon_pos_name}']['z'],
                    1.0,
                ]
            ).reshape((1, -1, 1))
            current_vector = np.tile(current_vector, (mcp_base_dimension, 1, 1))
            setattr(self, f'_r_{tendon_pos_name}', current_vector)
        # initialize tendon legnths
        self._front_right_tendon_lengths = np.zeros((mcp_base_dimension, 4))
        self._front_left_tendon_lengths = np.zeros((mcp_base_dimension, 4))
        self._back_right_tendon_lengths_s1 = np.zeros((mcp_base_dimension, 4))
        self._back_left_tendon_lengths_s1 = np.zeros((mcp_base_dimension, 4))
        self._back_right_tendon_lengths_s2 = np.zeros((mcp_base_dimension, 4))
        self._back_left_tendon_lengths_s2 = np.zeros((mcp_base_dimension, 4))
        # initialize transform matrices
        self._transform_matrices_B_to_M = np.zeros((mcp_base_dimension, 4, 4))
        self._transform_matrices_M_to_T = np.zeros((mcp_base_dimension, 4, 4))
        self._transform_matrices_B_to_T = np.zeros((mcp_base_dimension, 4, 4))
        # get tendon lengths in the center pos of the motors
        self._tendon_lengths_at_zero = np.zeros(mcp_base_dimension * 2)
        self._tendon_lengths_at_zero = self.get_tendon_length_from_angle(
            np.zeros((mcp_base_dimension, 2))
        )

    def get_tendon_length_from_angle(self, angles: np.ndarray) -> np.ndarray:
        """
        Derive tendon length from the desired angle
        angles is assumed to be of shate (n_joints, 2), with its first column
        being used for abduction angles (psi) and its second column used for
        flexion angles (omega). Both are in randians.
        """
        assert angles.shape[0] == self._transform_matrices_B_to_T.shape[0], (
            f'The shape of the angles {angles.shape} is incompatible with'
            + ' the shape of the transform matrices stack '
            + f' {self._transform_matrices_B_to_T.shape}!'
        )
        psis = angles[:, 0]
        omegas = angles[:, 1]
        # Initialize transform matrices
        self._update_base_to_middle_tf_from_angle(psis=psis)
        self._update_middle_to_top_tf_from_angle(omegas=omegas)
        self._update_base_to_top_tf_from_subtransforms()
        # Calculate front tendons (modeled as a single line)
        self._front_right_tendon_lengths = (
            self._r_sfr - self._transform_matrices_B_to_T @ self._r_efr
        )
        self._front_left_tendon_lengths = (
            self._r_sfl - self._transform_matrices_B_to_T @ self._r_efl
        )
        # Calculate the back tendons (modeled in two segments)
        # right
        self._back_right_tendon_lengths_s1 = (
            self._r_sbr - self._transform_matrices_B_to_M @ self._r_mbr
        )
        self._back_right_tendon_lengths_s2 = (
            self._transform_matrices_B_to_M @ self._r_mbr
            - self._transform_matrices_M_to_T @ self._r_ebr
        )
        # left
        self._back_left_tendon_lengths_s1 = (
            self._r_sbl - self._transform_matrices_B_to_M @ self._r_mbl
        )
        self._back_left_tendon_lengths_s2 = (
            self._transform_matrices_B_to_M @ self._r_mbl
            - self._transform_matrices_M_to_T @ self._r_ebl
        )
        self._back_left_tendon_lengths_s2 = self._back_right_tendon_lengths_s2.reshape(
            -1, 4, 1
        )
        # calculate lengths and return
        front_right_tendon_lenghts = np.linalg.norm(
            self._front_right_tendon_lengths, axis=1
        )
        front_left_tendon_lenghts = np.linalg.norm(
            self._front_left_tendon_lengths, axis=1
        )
        back_right_tendon_lengths = np.linalg.norm(
            self._back_right_tendon_lengths_s1, axis=1
        ) + np.linalg.norm(self._back_right_tendon_lengths_s2, axis=1)
        back_left_tendon_lengths = np.linalg.norm(
            self._back_left_tendon_lengths_s1, axis=1
        ) + np.linalg.norm(self._back_left_tendon_lengths_s2, axis=1)
        tendon_lengths = self._get_differential_tendon_lengths(
            front_right_tendon_lenghts,
            back_right_tendon_lengths,
            front_left_tendon_lenghts,
            back_left_tendon_lengths,
        )
        tendon_lengths -= self._tendon_lengths_at_zero
        return tendon_lengths

    def _get_differential_tendon_lengths(
        self,
        front_right_tendon_lengths: np.ndarray,
        back_right_tendon_lengths: np.ndarray,
        front_left_tendon_lengths: np.ndarray,
        back_left_tendon_lengths: np.ndarray,
        merge_mode: str = 'alternating',
    ) -> np.ndarray:
        """
        Calculate the sum of the opposing tendons to get the commanded tendon
        legths.
        """
        right_tendons = front_right_tendon_lengths + back_left_tendon_lengths
        left_tendons = front_left_tendon_lengths + back_right_tendon_lengths
        if merge_mode == 'alternating':
            tendon_lengths = np.zeros((2 * right_tendons.shape[0]))
            tendon_lengths[::2] = right_tendons.reshape((-1,))
            tendon_lengths[1::2] = left_tendons.reshape((-1,))
        else:
            raise NotImplementedError
        return tendon_lengths

    def _update_base_to_middle_tf_from_angle(self, psis: np.ndarray):
        """
        Calculates the stacked transform matrices that take the tendon from
        the base to the middle
        """
        self._transform_matrices_B_to_M[:, 0, 0] = 1.0
        self._transform_matrices_B_to_M[:, 0, 1:] = 0.0
        self._transform_matrices_B_to_M[:, 1, 1] = np.cos(psis)
        self._transform_matrices_B_to_M[:, 1, 2] = -np.sin(psis)
        self._transform_matrices_B_to_M[:, 1, 3] = 0.0
        self._transform_matrices_B_to_M[:, 2, 1] = np.sin(psis)
        self._transform_matrices_B_to_M[:, 2, 2] = np.cos(psis)
        self._transform_matrices_B_to_M[:, 2, 3] = self._h_1
        self._transform_matrices_B_to_M[:, 3, :] = 0.0
        self._transform_matrices_B_to_M[:, 3, 3] = 1.0

    def _update_middle_to_top_tf_from_angle(self, omegas: np.ndarray):
        """
        Calculates the stacked transform matrices that take the tendon from
        the middle to the top of the MCP joint
        """
        self._transform_matrices_M_to_T[:, 0, 0] = np.cos(omegas)
        self._transform_matrices_M_to_T[:, 0, 1] = 0.0
        self._transform_matrices_M_to_T[:, 0, 2] = np.sin(omegas)
        self._transform_matrices_M_to_T[:, 0, 3] = 0.0
        self._transform_matrices_M_to_T[:, 1, :] = 0.0
        self._transform_matrices_M_to_T[:, 1, 1] = 1.0
        self._transform_matrices_M_to_T[:, 2, 0] = -np.sin(omegas)
        self._transform_matrices_M_to_T[:, 2, 1] = 0.0
        self._transform_matrices_M_to_T[:, 2, 2] = np.cos(omegas)
        self._transform_matrices_M_to_T[:, 2, 3] = self._h_2
        self._transform_matrices_M_to_T[:, 3, :] = 0.0
        self._transform_matrices_M_to_T[:, 3, 3] = 1.0

    def _update_base_to_top_tf_from_subtransforms(self):
        """
        Calculates the stacked end-to-end transform by combining the two sub-
        transforms (base-to-middle and middle-to-base)
        """
        self._transform_matrices_B_to_T = (
            self._transform_matrices_B_to_M @ self._transform_matrices_M_to_T
        )

    def _get_base_to_top_tf_from_angles(self, psis: np.ndarray, omegas: np.ndarray):
        """
        Calculates the stacked end-to-end transform using the given angles
        Only for checking/debug
        """
        _transform_matrices_B_to_T = np.zeros(
            (self._transform_matrices_B_to_M.shape[0], 4, 4)
        )
        _transform_matrices_B_to_T[:, 0, 0] = np.cos(omegas)
        _transform_matrices_B_to_T[:, 0, 1] = 0.0
        _transform_matrices_B_to_T[:, 0, 2] = np.sin(omegas)
        _transform_matrices_B_to_T[:, 0, 3] = 0.0
        _transform_matrices_B_to_T[:, 1, 0] = np.sin(psis) * np.sin(omegas)
        _transform_matrices_B_to_T[:, 1, 1] = np.cos(psis)
        _transform_matrices_B_to_T[:, 1, 2] = -np.sin(psis) * np.cos(omegas)
        _transform_matrices_B_to_T[:, 1, 3] = -np.sin(psis) * self._h_1
        _transform_matrices_B_to_T[:, 2, 0] = -np.cos(psis) * np.sin(omegas)
        _transform_matrices_B_to_T[:, 2, 1] = np.sin(psis)
        _transform_matrices_B_to_T[:, 2, 2] = np.cos(psis) * np.cos(omegas)
        _transform_matrices_B_to_T[:, 2, 3] = np.cos(psis) * self._h_2 + self._h_1
        _transform_matrices_B_to_T[:, 3, :] = 0.0
        _transform_matrices_B_to_T[:, 3, 3] = 1.0
        return _transform_matrices_B_to_T
