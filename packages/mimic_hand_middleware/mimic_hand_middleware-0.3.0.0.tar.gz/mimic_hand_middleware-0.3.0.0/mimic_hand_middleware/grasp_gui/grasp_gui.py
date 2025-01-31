"""
The workhorse of hand development: grasp gui allows motor and joint-level
commands through a simple graphical UI for ease of development.
options: --debug, --calibrate, --sim

A modified version of the P0 grasp GUI from ETH SRL, cleaned up and adapted to
a class-based logic.
"""

import copy
import logging
import tkinter as tk
from tkinter import NORMAL, messagebox, ttk

import numpy as np

from mimic_hand_middleware import GripperController


class GraspGui(tk.Frame):
    """
    A simple graphical UI for commanding joint/motor angles for the P04
    prototype.
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.gui_root = parent
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        self._logger.info('Connecting to hand')
        self.gc = GripperController(max_motor_current=60, use_sim_motors=False)
        self.gc.print_hand_info()
        self.gc.connect_motors()
        self.gc.enable_torque()
        self.gc.init_joints(calibrate=False)
        self.motor_cmd_array = np.zeros((self.gc.num_of_motors))
        self.joint_cmd_array = np.zeros((self.gc.num_of_joints))
        self.gc.command_motor_angles(self.motor_cmd_array)
        self._setup_gui()

    def _setup_gui(self) -> None:
        """
        Starts the GUI application for the Grasp GUI.
        """
        # setup main application
        self.gui_root.geometry('600x550')
        self.gui_root.resizable(True, True)
        self.gui_root.title('Joint-level control & grasping GUI')
        self.gui_root.protocol('WM_DELETE_WINDOW', self._closing_protocol)
        # set up GUI widget by widget
        self._setup_mode_selection_gui(row_idx=0)
        self._setup_action_buttons(row_idx=2)
        self._setup_motor_controller_gui(row_idx=3)

    def _setup_mode_selection_gui(self, row_idx: int = 0) -> None:
        """
        Sets up the mode selection GUI consisting of a list of RadioButtons.
        The following modes can be selected:
            - Motor Control: for the motor-level commands. The user can use
            sliders to give position commands to the motors, each in a custom
            range.
            - Joint Control (TODO):
            - Grasp Control: allows loading recorded arrays of joint commands
            to the robot (TODO)
        """
        # GUI for settings
        self._control_mode_names = [
            'Motor Control',
            'Joint Control',
            'Grasp Control',
        ]
        self._n_control_modes = len(self._control_mode_names)
        self._mode_selection_col_step = 2
        self._mode_selection_col_span = (
            self._n_control_modes * self._mode_selection_col_step
        )
        ttk.Label(self.gui_root, text='Select Control Mode: ').grid(
            row=row_idx, column=1, columnspan=self._mode_selection_col_span
        )
        self._ctrl_mode = tk.IntVar(master=self.gui_root, value=0)
        self._radio_buttons = []
        row_idx += 1
        for mode_idx, mode_name in enumerate(self._control_mode_names):
            self._radio_buttons.append(
                ttk.Radiobutton(
                    self.gui_root,
                    text=mode_name,
                    variable=self._ctrl_mode,
                    value=mode_idx,
                    command=self._change_control_mode,
                )
            )
            self._radio_buttons[-1].grid(
                row=row_idx,
                column=self._mode_selection_col_step * mode_idx,
                columnspan=self._mode_selection_col_step,
            )

    def _setup_action_buttons(self, row_idx: int = 1) -> None:
        """
        Adds buttons that perform simple callbacks (like resetting motors or
        joints) upon being clicked.
        """
        self._action_button_names = ['Reset Motor Init']
        self._action_button_callbacks = [self._update_motor_init]
        self._action_buttons = []
        self._n_action_buttons = len(self._action_button_names)
        self._action_button_col_step = 2
        self._action_button_span = self._n_action_buttons * self._action_button_col_step
        for button_idx, button in enumerate(
            zip(self._action_button_names, self._action_button_callbacks)
        ):
            button_name = button[0]
            button_callback = button[1]
            action_button = ttk.Button(
                self.gui_root,
                text=button_name,
                command=button_callback,
                state=NORMAL,
            )
            action_button.grid(
                row=row_idx,
                column=self._action_button_col_step * button_idx,
                columnspan=self._action_button_span,
            )
            self._action_buttons.append(action_button)

    def _update_motor_init(self) -> None:
        """
        Recalibrates the motor offset for the GripperController
        """
        self.gc.get_new_motor_zero_positions()
        # set sliders back and reset cmd
        for slider_idx in range(len(self.motor_sliders)):
            self.motor_sliders[slider_idx].set(0)
        self.motor_cmd_array = np.zeros_like(self.motor_cmd_array)

    def _change_control_mode(self) -> None:
        """
        Changes the control mode of the grasp GUI between motor, joint and
        grasp control.
        """
        control_mode_display_name = self._control_mode_names[self._ctrl_mode.get()]
        control_mode_method_name = self._get_control_method_name_from_display_name(
            control_mode_display_name
        )
        # Destroy all other displays
        for display_name in self._control_mode_names:
            if display_name != control_mode_display_name:
                method_name = self._get_control_method_name_from_display_name(
                    display_name
                )
                clearup_fcn = getattr(self, f'_clear_{method_name}ler_gui', None)
                if clearup_fcn is not None:
                    clearup_fcn()
        # Create display
        setup_fcn = getattr(self, f'_setup_{control_mode_method_name}ler_gui', None)
        if setup_fcn is not None:
            setup_fcn()

    def _get_control_method_name_from_display_name(self, display_name: str) -> str:
        """
        Returns the name of the control method that is used for class functions
        from the display name of the control method, eg.
        Motor Control -> motor_control
        """
        method_name = display_name.lower().replace(' ', '_')
        return method_name

    def _setup_motor_controller_gui(self, row_idx=3) -> None:
        """
        Creates sliders for all of the motors.
        """
        # GUI for motor angle control
        controller_row_idx = row_idx
        self.motor_sliders = []
        self.motor_status_displays = []
        self.motor_pos_displays = []
        self.motor_cur_displays = []
        self.motor_labels = []
        slid_id = 0
        main_label = ttk.Label(self.gui_root, text='Motor Control:')
        self.motor_labels.append(main_label)
        main_label.grid(row=7, column=1, columnspan=2)
        for motor_idx in range(self.gc.num_of_motors):
            # make labels
            self.motor_labels.append(
                ttk.Label(self.gui_root, text=f'Motor {motor_idx}')
            )
            self.motor_labels[-1].grid(row=controller_row_idx + motor_idx, column=0)
            # make slider
            range_min = self.gc.motors_limit_lower
            range_max = self.gc.motors_limit_higher
            self.motor_sliders.append(
                ttk.Scale(
                    self.gui_root,
                    from_=range_min,
                    to=range_max,
                    command=lambda value,
                    id=slid_id: self._changed_motor_slider_value_callback(id, value),
                    length=300,
                )
            )
            self.motor_sliders[-1].grid(row=row_idx, column=1, columnspan=2)
            slid_id += 1
            # make motor_cmd displays
            self.motor_status_displays.append(ttk.Label(self.gui_root, text='0.'))
            self.motor_status_displays[-1].grid(row=row_idx, column=3)
            # make motor_pos displays
            self.motor_pos_displays.append(ttk.Label(self.gui_root, text='0.'))
            self.motor_pos_displays[-1].grid(row=row_idx, column=4)
            # make motor current displays
            self.motor_cur_displays.append(ttk.Label(self.gui_root, text='0.'))
            self.motor_cur_displays[-1].grid(row=row_idx, column=5)
            row_idx += 1

    def _setup_joint_controller_gui(self, row_idx=3) -> None:
        """
        Creates sliders for all of the joints.
        """
        # GUI for joint control
        controller_row_idx = row_idx
        self.joint_sliders = []
        self.joint_status_displays = []
        self.joint_pos_displays = []
        self.joint_cur_displays = []
        self.joint_labels = []
        slid_id = 0
        main_label = ttk.Label(self.gui_root, text='Joint Control:')
        self.joint_labels.append(main_label)
        main_label.grid(row=7, column=1, columnspan=2)
        for joint_idx in range(self.gc.num_of_joints):
            # make labels
            joint_name = self.gc.joint_names[joint_idx]
            self.joint_labels.append(ttk.Label(self.gui_root, text=joint_name))
            self.joint_labels[-1].grid(row=controller_row_idx + joint_idx, column=0)
            # make slider
            range_min = self.gc.joint_limit_lower[joint_idx]
            range_max = self.gc.joint_limit_higher[joint_idx]
            self.joint_sliders.append(
                ttk.Scale(
                    self.gui_root,
                    from_=range_min,
                    to=range_max,
                    command=lambda value,
                    id=slid_id: self._changed_joint_slider_value_callback(id, value),
                    length=300,
                )
            )
            self.joint_sliders[-1].grid(row=row_idx, column=1, columnspan=2)
            slid_id += 1
            # make motor_cmd displays
            self.joint_status_displays.append(ttk.Label(self.gui_root, text='0.'))
            self.joint_status_displays[-1].grid(row=row_idx, column=3)
            # make motor_pos displays
            self.joint_pos_displays.append(ttk.Label(self.gui_root, text='0.'))
            self.joint_pos_displays[-1].grid(row=row_idx, column=4)
            # make motor current displays
            self.joint_cur_displays.append(ttk.Label(self.gui_root, text='0.'))
            self.joint_cur_displays[-1].grid(row=row_idx, column=5)
            row_idx += 1

    def _clear_motor_controller_gui(self) -> None:
        """
        Clears all widgets that are related to the motor controller
        """
        motor_control_widgets = [
            'motor_sliders',
            'motor_status_displays',
            'motor_pos_displays',
            'motor_cur_displays',
            'motor_labels',
        ]
        for widget_name in motor_control_widgets:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                self._destroy_widget_recursively(widget)

    def _destroy_widget_recursively(self, widget) -> None:
        """
        Destroys a multi-level list of widgets recursively
        """
        if type(widget) is list:
            for subwidget in widget:
                self._destroy_widget_recursively(subwidget)
        else:
            widget.destroy()

    def _map_mcp_delta_mean_to_angles(self, cmd: np.ndarray) -> np.ndarray:
        """
        Maps a motor angle command that represents MCP angles as delta and mean
        values to the conventional API format.
        Both the in- and output commands are represented by numpy arrays of
        shape (self._num_of_motors,)
        """
        backup_cmd = copy.deepcopy(cmd)
        cmd[4] = backup_cmd[4] + 0.5 * backup_cmd[5]
        cmd[5] = backup_cmd[4] - 0.5 * backup_cmd[5]
        # return cmd @ self.gc.motors_mcp_to_mean_delta
        return cmd

    def _changed_motor_slider_value_callback(self, id: int, value: float) -> None:
        """
        Updates the corresponding motor value and sends the motor command
        through the gripper controller interface.
        """
        self.motor_cmd_array[id] = value
        self.gc.command_motor_angles(self.motor_cmd_array)
        motor_status = self.gc.get_motor_pos_vel_cur()
        self._update_motor_pos_displays(motor_pos_array=motor_status[0])
        self._update_motor_cur_displays(motor_cur_array=motor_status[2])

    def _changed_joint_slider_value_callback(self, id: int, value: float) -> None:
        """
        Updates the corresponding joint value and sends the motor command
        through the gripper controller interface.
        """
        self.joint_cmd_array[id] = value
        self.gc.command_joint_angles(self.joint_cmd_array)
        motor_status = self.gc.get_motor_pos_vel_cur()
        self._update_motor_cmd_displays(
            status_displays=self.joint_status_displays,
            status_array=self.joint_cmd_array,
        )
        self._update_motor_pos_displays(
            motor_pos_array=motor_status[0], pos_displays=self.joint_pos_displays
        )
        self._update_motor_cur_displays(
            motor_cur_array=motor_status[2], cur_displays=self.joint_cur_displays
        )

    def _update_motor_cmd_displays(
        self, status_displays=None, status_array=None
    ) -> None:
        """
        Updates the commanded motor angle display widgets
        """
        if status_displays is None:
            status_displays = self.motor_status_displays
        if status_array is None:
            status_array = self.motor_cmd_array
        for idx, display_label in enumerate(status_displays):
            display_label.config(
                text=np.format_float_positional(status_array[idx], precision=2)
            )

    def _update_motor_pos_displays(
        self, motor_pos_array=None, pos_displays=None
    ) -> None:
        """
        Updates the motor angle display widgets with motor_pos_array (either a
        numpy array of shape (self.num_of_motors,) or None)
        """
        if motor_pos_array is None:
            motor_pos_array = self.gc.get_motor_pos_vel_cur()[0]
        if pos_displays is None:
            pos_displays = self.motor_pos_displays
        for idx, display_label in enumerate(pos_displays):
            display_label.config(
                text=np.format_float_positional(motor_pos_array[idx], precision=2)
            )

    def _update_motor_cur_displays(
        self, motor_cur_array=None, cur_displays=None
    ) -> None:
        """
        Updates the motor current display widgets
        """
        if motor_cur_array is None:
            motor_cur_array = self.gc.get_motor_pos_vel_cur()[2]
        if cur_displays is None:
            cur_displays = self.motor_cur_displays
        for idx, display_label in enumerate(cur_displays):
            display_label.config(
                text=np.format_float_positional(motor_cur_array[idx], precision=2)
            )

    def _closing_protocol(self):
        """
        Runs upon closing the grasp GUI.
        - Closes the window
        - Disconnects from the motors
        """
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            self.gui_root.destroy()
            self.gc.disconnect_motors()


if __name__ == '__main__':
    root = tk.Tk()
    GraspGui(root)
    root.mainloop()
