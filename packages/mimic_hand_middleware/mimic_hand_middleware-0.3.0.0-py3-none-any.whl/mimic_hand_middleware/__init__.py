__version__ = '0.1.0'
__author__ = 'Ben Forrai'
__credits__ = 'Mimic Robotics AG'
import mimic_hand_api

from mimic_hand_middleware.calibrate_gripper import update_calibration_with_current_pose
from mimic_hand_middleware.gripper_controller import GripperController
from mimic_hand_middleware.set_motors_to_freerunning_mode import (
    set_motors_to_freerunning_mode,
)
