"""
Calibrates the gripper and saves the new motor offsets in motor_config.yaml.
"""

# Standard
import argparse

# Custom
import mimic_hand_middleware


def update_calibration_with_current_pose() -> None:
    """
    Updates the calibration file at calibration_path with the current position of the
    finger joints as zero position.
    """
    gripper_controller = mimic_hand_middleware.GripperController(
        calibrate_at_start=True
    )
    gripper_controller.disconnect_motors()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Calibrate the mimic hand's zero position."
    )
    mimic_hand_middleware.set_motors_to_freerunning_mode()
    input('Move motors to the new zero position, then press enter to save')
    update_calibration_with_current_pose()
