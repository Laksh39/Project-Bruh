#!/usr/bin/python3
# coding=utf8
import sys
import time
import signal
import threading
import common.mecanum as mecanum
from common.ros_robot_controller_sdk import Board

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

chassis = mecanum.MecanumChassis()
board = Board()
running = True

def stop(signum, frame):
    global running
    running = False
    chassis.set_velocity(0, 0, 0)
    print('Stopped.')

signal.signal(signal.SIGINT, stop)

# ?? Arm positions (from your test_arm.py) ?????????????????
HOME = [
    [1, 1500], [3, 1500], [4, 2000], [5, 1500], [6, 1500],
]

WAVE_A = [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1700]]
WAVE_B = [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1300]]

# ?? Arm wave thread ???????????????????????????????????????
def wave_arm(stop_event):
    while not stop_event.is_set():
        board.pwm_servo_set_position(0.5, WAVE_A)
        time.sleep(0.6)
        board.pwm_servo_set_position(0.5, WAVE_B)
        time.sleep(0.6)
    # Return home when done
    board.pwm_servo_set_position(1.0, HOME)
    time.sleep(1.2)

# ?? Victory Dance ?????????????????????????????????????????
if __name__ == '__main__':
    print("Moving arm to home...")
    board.pwm_servo_set_position(1.0, HOME)
    time.sleep(1.5)

    stop_event = threading.Event()
    arm_thread = threading.Thread(target=wave_arm, args=(stop_event,))
    arm_thread.start()

    print("Victory dance! Spinning + waving arm simultaneously...")
    chassis.set_velocity(0, 0, 1)   # spin in place, no translation
    time.sleep(6)

    chassis.set_velocity(0, 0, 0)
    stop_event.set()
    arm_thread.join()

    print("B.R.U.H. protocol: Victory dance complete!")

