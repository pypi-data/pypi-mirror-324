"""
Palm processing script for the Fusion360 SDK python plugin
Reads the parameters describing the finger base transforms wrt. the palm
from the Fusion user-defined parameters. The expected format of the
parameters is the following:
{finger_initial}_{X/Y/Z}_{rot/trans}

Kudos to Ueli Mauer for the original code
Ported from SRL's faive-integration by Ben Forrai (ben.forrai@mimicrobotics.com)
"""

import traceback

import adsk.cam
import adsk.core
import adsk.fusion
import numpy as np
import yaml
from scipy.spatial.transform import Rotation as R


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct

        # Set styles of file dialog.
        fileDlg = ui.createFileDialog()
        fileDlg.title = 'Choose location to save YAML file'
        fileDlg.filter = '*.yaml'

        # Show folder dialog
        dlgResult = fileDlg.showSave()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            filepath = fileDlg.filename
        else:
            return

        # Fusion naming convention is defined here
        fingers = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        cad_finger_naming = {
            'Thumb': 'T',
            'Index': 'I',
            'Middle': 'M',
            'Ring': 'R',
            'Pinky': 'P',
        }
        axes = ['X', 'Y', 'Z']
        moves = ['rot', 'trans']

        # Fusion rotation convention is defined here
        euler_convention = 'ZYX'
        # Init data dict
        data = {}
        # Loop through user parameters and read the euler parameters and translations
        for finger in fingers:
            finger_key = cad_finger_naming[finger]
            for move in moves:
                if move == 'rot':
                    rot_euler = [
                        design.userParameters.itemByName(
                            f'{finger_key}_{axis}_{move}'
                        ).value
                        for axis in euler_convention
                    ]
                    rot_euler = np.asarray(rot_euler)
                    # create scipy rotation object
                    Rot = R.from_euler(
                        euler_convention.lower(), rot_euler, degrees=False
                    )
                elif move == 'trans':
                    translation = [
                        design.userParameters.itemByName(
                            f'{finger}_{axis}_{move}'
                        ).value
                        for axis in axes
                    ]
                    translation = np.asarray(translation)

            data[finger] = {
                'base_rot': Rot.as_quat().tolist(),
                'base_trans': translation.tolist(),
            }

        # Write file to chosen folder
        with open(filepath, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        ui.messageBox('Parameters written to YAML file')

    except:
        if ui:
            ui.messageBox('Failed:/n{}'.format(traceback.format_exc()))
