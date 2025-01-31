"""
Joint-to-motor conversion utilities for the P04 prototype (first one out of
Mimic).
"""

# Standard
import os
from enum import Enum
from typing import Dict

import defusedxml.ElementTree as ET

# Third-party
import numpy as np

# Custom
from mimic_hand_middleware.conversion_utils import hand_utils

PROTOTYPE_SERIES = 'p45'
URDF_PATH = hand_utils.get_urdf_path(PROTOTYPE_SERIES)
JOINT_NAMES_MODEL_P04 = hand_utils.parse_urdf(urdf_path=URDF_PATH)
assert len(JOINT_NAMES_MODEL_P04) == 20  # added dp joints on each finger
JOINT_NAMES_NORMAL_P04 = []
for joint_name in JOINT_NAMES_MODEL_P04:
    if not joint_name.endswith('dp') and not joint_name.endswith('offset'):
        JOINT_NAMES_NORMAL_P04.append(joint_name)
assert len(JOINT_NAMES_NORMAL_P04) == 16
print(JOINT_NAMES_NORMAL_P04)

MP2DP_FACTOR = 1.0
GC_TENDONS = {
    'thumb_base2cmc': {},
    'thumb_cmc2mcp': {},
    'thumb_mcp2pp': {},
    'thumb_pp2dpA': {},
    'index_base2mcp': {},
    'index_mcp2pp': {},
    'index_pp2mp': {},
    'index_mp2dp': {'index_mcp2pp': MP2DP_FACTOR},
    'middle_base2mcp': {},
    'middle_mcp2pp': {},
    'middle_pp2mp': {},
    'middle_mp2dp': {'middle_mcp2pp': MP2DP_FACTOR},
    'ring_base2mcp': {},
    'ring_mcp2pp': {},
    'ring_pp2mp': {},
    'ring_mp2dp': {'ring_mcp2pp': MP2DP_FACTOR},
    'pinky_base2mcp': {},
    'pinky_mcp2pp': {},
    'pinky_pp2mp': {},
    'pinky_mp2dp': {'pinky_mcp2pp': MP2DP_FACTOR},
}

ACTUATED_GC_TENDON_NAMES = []
for tendon_name in GC_TENDONS.keys():
    if not tendon_name.endswith('dp'):
        ACTUATED_GC_TENDON_NAMES.append(tendon_name)

THUMB_TENDON_IDXES = []
FINGER_PIP_IDXES = []
FINGER_MCP_RIGHT_IDXES = []
FINGER_MCP_LEFT_IDXES = []
THUMB_TENDON_NAMES = []
FINGER_PIP_NAMES = []
FINGER_MCP_RIGHT_NAMES = []
FINGER_MCP_LEFT_NAMES = []

for idx, tendon_name in enumerate(ACTUATED_GC_TENDON_NAMES):
    if tendon_name.startswith('thumb'):
        THUMB_TENDON_NAMES.append(tendon_name)
        THUMB_TENDON_IDXES.append(idx + 1)
    else:
        if tendon_name.endswith('mcp'):
            FINGER_MCP_RIGHT_IDXES.append(idx + 1)
            FINGER_MCP_RIGHT_NAMES.append(tendon_name)
        if tendon_name.endswith('pp'):
            FINGER_MCP_LEFT_IDXES.append(idx + 1)
            FINGER_MCP_LEFT_NAMES.append(tendon_name)
        if tendon_name.endswith('mp'):
            FINGER_PIP_IDXES.append(idx + 1)
            FINGER_PIP_NAMES.append(tendon_name)

FINGER_TO_TIP: Dict[str, str] = {
    'thumb': 'thumb_fingertip',
    'index': 'index_fingertip',
    'middle': 'middle_fingertip',
    'ring': 'ring_fingertip',
    'pinky': 'pinky_fingertip',
}

FINGER_TO_BASE = {
    'thumb': 'thumb_cmc_v3_1',
    'index': 'index_mcp_v1_1',
    'middle': 'middle_mcp_v1_1',
    'ring': 'ring_mcp_v1_1',
    'pinky': 'pinky_mcp_v1_1',
}

# TRACKER-SPECIFIC CONSTANTS
# Sensoryx glove
SENSORYX_PALM_OFFSET_ARRAY = [-0.015, 0.015, 0.097]
SENSORYX_PALM_RVIZ_OFFSET_ARRAY = [-0.03, 0.03, 0.194]
SENSORYX_ROTATION_OFFSET_ARRAY_RAD = [-1.57, -0.58, -0.15]
SENSORYX_FLIP_AXIS = [False, False, False]

# Manus glove
MANUS_PALM_OFFSET_ARRAY = [-0.015, 0.015, 0.097]
MANUS_PALM_RVIZ_OFFSET_ARRAY = [-0.03, 0.03, 0.194]
MANUS_ROTATION_OFFSET_ARRAY_RAD = [-1.57, -0.58, -0.25]
MANUS_FLIP_AXIS = [False, False, False]
MANUS_SCALE_X = 1.0
MANUS_SCALE_Y = 1.0
MANUS_SCALE_Z = 0.9

# Mano model
MANO_PALM_OFFSET_ARRAY = [-0.015, 0.015, 0.097]
MANO_PALM_RVIZ_OFFSET_ARRAY = [-0.03, 0.03, 0.194]
# TODO (fbenedek) - change this to automatic, using similar method to normal2model_mat
JOINT_MAP_NDARRAY = np.array(
    [
        [1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
        ],
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
        ],
    ]
).astype(np.float32)
# the mean-delta representation for MCP angles is simpler to steer when using
# motor-level control, so we're providing utility matrices for it here
MCP_TO_MEAN_DELTA = np.eye(16)
for i in range(4):
    MCP_TO_MEAN_DELTA[3 * i + 4 : 3 * i + 6, 3 * i + 4 : 3 * i + 6] = np.array(
        [[0.5, 0.5], [1.0, -1.0]]
    )

MCP_FROM_MEAN_DELTA = np.eye(16)
for i in range(4):
    MCP_FROM_MEAN_DELTA[3 * i + 4 : 3 * i + 6, 3 * i + 4 : 3 * i + 6] = np.array(
        [[1.0, 0.5], [1.0, -0.5]]
    )


ROBOT_INIT_ANGLE_DEGREES = 0.5
MOTOR_LIMIT_LOWER = -180
MOTOR_LIMIT_HIGHER = 180
MCP_ABD_JOINT_IDXES = [4, 7, 10, 13]
MCP_FLEX_JOINT_IDXES = [5, 8, 11, 14]
MCP_JOINT_IDX_PAIRS = [
    [abd, flex] for (abd, flex) in zip(MCP_ABD_JOINT_IDXES, MCP_FLEX_JOINT_IDXES)
]
MCP_JOINT_IDXES = []
for mcp_pair in MCP_JOINT_IDX_PAIRS:
    MCP_JOINT_IDXES.append(mcp_pair[0])
    MCP_JOINT_IDXES.append(mcp_pair[1])
PIP_JOINT_IDXES = [6, 9, 12, 15]
THUMB_JOINT_IDXES = [0, 1, 2, 3]

# PIP limits by default
# Hardware allows the lower limit to be around -15 deg
# but it looks off so we're clipping it
GC_LIMITS_LOWER = [0] * len(JOINT_NAMES_NORMAL_P04)
GC_LIMITS_UPPER = [95] * len(JOINT_NAMES_NORMAL_P04)
# MCP ABDUCTION limits
for mcp_abd_idx in MCP_ABD_JOINT_IDXES:
    GC_LIMITS_LOWER[mcp_abd_idx] = -15.0
    GC_LIMITS_UPPER[mcp_abd_idx] = 15.0
# MCP limits
for mcp_idx in MCP_FLEX_JOINT_IDXES:
    GC_LIMITS_LOWER[mcp_idx] = -5.0
    GC_LIMITS_UPPER[mcp_idx] = 90.0
# Thumb limits
THUMB_LIMITS_LOWER = [-30, -55, -40, -50]
THUMB_LIMITS_UPPER = [100, 55, 30, 40.0]
for thumb_idx, full_idx in enumerate(THUMB_JOINT_IDXES):
    GC_LIMITS_LOWER[full_idx] = THUMB_LIMITS_LOWER[thumb_idx]
    GC_LIMITS_UPPER[full_idx] = THUMB_LIMITS_UPPER[thumb_idx]


JOINT_NAMES_NORMAL = []
JOINT_NAMES_MODEL = []
jointname2id_dict_model = {}
jointname2id_dict_normal = {}

MOTOR_NAMES = [str(i) for i in range(16)]


def init_matrices():
    global \
        JOINT_NAMES_MODEL, \
        JOINT_NAMES_NORMAL, \
        jointname2id_dict_model, \
        jointname2id_dict_normal, \
        model2normal_mat, \
        normal2model_mat
    JOINT_NAMES_NORMAL = JOINT_NAMES_NORMAL_P04
    JOINT_NAMES_MODEL = JOINT_NAMES_MODEL_P04
    # construct a dict mapping from joint name to joint id, for fast lookup
    for i, joint_name in enumerate(JOINT_NAMES_MODEL):
        jointname2id_dict_model[joint_name] = i
    for i, joint_name in enumerate(JOINT_NAMES_NORMAL):
        jointname2id_dict_normal[joint_name] = i
    # construct matrix that maps between joint conventions
    model2normal_mat = np.zeros((len(JOINT_NAMES_NORMAL), len(JOINT_NAMES_MODEL)))
    # since P04 only uses pin joints, model->normal convention is 1 everywhere
    for i_model, joint_name_model in enumerate(JOINT_NAMES_MODEL):
        if joint_name_model in JOINT_NAMES_NORMAL:
            model2normal_mat[jointname2id_dict_normal[joint_name_model], i_model] = 1.0
    # for the other direction, we'll set the dp joints to 0.5
    normal2model_mat = np.zeros((len(JOINT_NAMES_MODEL), len(JOINT_NAMES_NORMAL)))
    for i_normal, joint_name_normal in enumerate(JOINT_NAMES_NORMAL):
        if joint_name_normal in JOINT_NAMES_MODEL:
            normal2model_mat[jointname2id_dict_model[joint_name_normal], i_normal] = 1.0
        if joint_name_normal.endswith('mp'):
            # if this is the pp2mp joint,
            # the linked mp2dp joint should also be updated
            mp2dp_factor = MP2DP_FACTOR
            dp_joint_name = joint_name_normal.replace('pp2mp', 'mp2dp')
            normal2model_mat[jointname2id_dict_model[dp_joint_name], i_normal] = (
                mp2dp_factor
            )
