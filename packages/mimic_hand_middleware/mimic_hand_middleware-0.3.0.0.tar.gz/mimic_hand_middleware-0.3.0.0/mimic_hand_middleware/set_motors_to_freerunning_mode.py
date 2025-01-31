"""Set the motors to freerunning mode for calibration.

Connects to all motors of the mimic hand, turns torque
off, then disconnects. Disconnecting may raise errors
TODO (ben): ignore errors of disconnection
"""

from mimic_hand_api import RP2040API


def set_motors_to_freerunning_mode() -> None:
    """Set the motors to freerunning mode for calibration.

    Uses the mimic_hand_api to communicate with the control
    boards of the motors. Disables torque on all of them,
    then disconnects.
    """
    client = RP2040API()
    client.connect_all_motors()
    client.set_all_motors_to_freerunning_mode()
    # Disconnect motors
    client.disconnect_all_motor_boards()


if __name__ == '__main__':
    set_motors_to_freerunning_mode()
