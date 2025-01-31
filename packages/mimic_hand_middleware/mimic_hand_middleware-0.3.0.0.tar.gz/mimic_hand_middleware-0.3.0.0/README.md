# mimic_hand_middleware
Repository for the joint-to-motor level control of mimic's robotic hands.
## System specifications
We support the following platforms:
- x86 architecture
- Ubuntu Jammy (22.04)
- 2 USB-A ports
## Install
To install the hand API, clone the this repo and run its install script:
```bash
mkdir ~/git && cd ~/git
git clone git@github.com:mimicrobotics/mimic_hand_middleware.git
./scripts/install.sh
```
Since the script installs new udev rules for the hand, when prompted, you'll need to enter a sudo password. The new python environment will be installed in `$HOME/python_venvs/mimic_hand`, so when opening a new terminal, make sure to activate this environment by running:
```bash
source ~/python_venvs/mimic_hand/bin/activate
```
When connecting the hand's USB board to your PC, Ubuntu will set the latency timer of the async buffer to 16 ms. This is too slow for our purposes, so we override it by running:
```bash
./scripts/connect_mimic_hand.sh
```
Optionally, you can paste the lines above into your `~/.bashrc` file - this will source your environment and modify the latency timers every time you open a new terminal.

## Run
First, you can run a test sequence on all of the joints by running:
```bash
source ~/python_venvs/mimic_hand/bin/activate
python tests/test_joint_cmd.py
```
You can also move the hand around yourself in a simple GUI:
```bash
source ~/python_venvs/mimic_hand/bin/activate
python python tests/grasp_gui.py
```

## Using our API
The main interface to our hands is the `GripperController` class. You can initialize it as follows:
```python
from mimic_hand_middleware import GripperController
gc = GripperController()
gc.connect_motors() # connect, set maximum current and operation mode (current-limited position control)
gc.init_joints(calibrate=False) # enable torques on the motors
```
### Sending joint commands to the hands
Motor commands are sent to all motors at once, as a numpy array of shape (16,). Commands are sent in degrees. To have a look at the zero positions, you can start up the `grasp_gui`, and select joint control mode to home all joints to 0.
```python
# commanding joint angles in degrees
gc.command_motor_angles(motor_cmd_array)
```
The numbering of joints follows a simple convention: idx `0` starts from the base of the thumb, then indexes increase with the distance from the finger base until `3` on the thumb, then on the index etc.
### Reading motor angles, speeds and currents from the hands
You can read the current motor angles, speeds and currents as follows:
```python
motor_status = self.gc.get_motor_pos_vel_cur()
```
Where `motor_status` is a list of length of 3, containing numpy arrays for motor positions (rad) speeds (rad/s) and currents (mA).
