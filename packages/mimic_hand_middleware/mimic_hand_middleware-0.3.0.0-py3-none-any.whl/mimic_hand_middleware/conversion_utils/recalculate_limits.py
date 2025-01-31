"""
The following script recalculates multipliers for simple linear + offset joint
kinematics in case the joint limits are violated.
All limits are in degrees.
"""

# Third-party
import numpy as np


def get_new_limits(
    old_angle_min: float,
    old_angle_max: float,
    new_angle_min: float,
    new_angle_max: float,
    old_angle_offset: float,
    old_angle_multiplier: float,
) -> list:
    """
    Returns the new multiplier and offset that match the same endpoints with the new
    angle commands.
    """
    old_angle_max = np.deg2rad(old_angle_max)
    old_angle_min = np.deg2rad(old_angle_min)
    new_angle_max = np.deg2rad(new_angle_max)
    new_angle_min = np.deg2rad(new_angle_min)
    t_min = old_angle_multiplier * (old_angle_offset + old_angle_min)
    t_max = old_angle_multiplier * (old_angle_offset + old_angle_max)
    new_angle_offset = (t_min * new_angle_max - t_max * new_angle_min) / (t_max - t_min)
    new_angle_multiplier = t_max / (new_angle_max + new_angle_offset)
    return new_angle_multiplier, new_angle_offset


def test_limits(
    old_angle_min: float,
    old_angle_max: float,
    new_angle_min: float,
    new_angle_max: float,
    old_angle_offset: float,
    old_angle_multiplier: float,
    new_angle_offset: float,
    new_angle_multiplier: float,
    epsilon: float = 0.0001,
) -> bool:
    """
    Tests if the tendon cmds are the same at the end stops for the old and new
    multiplier and offset settings
    """
    old_angle_max = np.deg2rad(old_angle_max)
    old_angle_min = np.deg2rad(old_angle_min)
    new_angle_max = np.deg2rad(new_angle_max)
    new_angle_min = np.deg2rad(new_angle_min)
    # old tendon endstop
    t_min_old = old_angle_multiplier * (old_angle_offset + old_angle_min)
    t_max_old = old_angle_multiplier * (old_angle_offset + old_angle_max)
    # new tendon endstop
    t_min_new = new_angle_multiplier * (new_angle_offset + new_angle_min)
    t_max_new = new_angle_multiplier * (new_angle_offset + new_angle_max)
    print('Delta min: ', t_min_new - t_min_old)
    print('Delta max: ', t_max_new - t_max_old)
    return (
        np.abs(t_min_old - t_min_new) < epsilon
        and np.abs(t_max_old - t_max_new) < epsilon
    )


if __name__ == '__main__':
    # get constants
    old_angle_min = float(input('old_angle_min'))
    old_angle_max = float(input('old_angle_max'))
    new_angle_min = float(input('new_angle_min'))
    new_angle_max = float(input('new_angle_max'))
    old_angle_offset = float(input('old_angle_offset'))
    old_angle_multiplier = float(input('old_angle_multiplier'))
    new_angle_multiplier, new_angle_offset = get_new_limits(
        old_angle_min,
        old_angle_max,
        new_angle_min,
        new_angle_max,
        old_angle_offset,
        old_angle_multiplier,
    )
    # test
    conversion_success = test_limits(
        old_angle_min,
        old_angle_max,
        new_angle_min,
        new_angle_max,
        old_angle_offset,
        old_angle_multiplier,
        new_angle_offset,
        new_angle_multiplier,
    )
    print(f'mul: {new_angle_multiplier}, offset: {new_angle_offset}')
    print(f'test success: {conversion_success}')
