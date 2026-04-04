#!/usr/bin/env python3
# coding=utf-8
"""
test_arm.py — Initialize the MasterPi 5DOF arm and perform a wave motion.

Servo map:
  ID 1 — base rotation     (500–2500 µs, 0–180°, center 1500)
  ID 3 — shoulder          (500–2500 µs, 0–180°, center 1500)
  ID 4 — elbow             (500–2500 µs, 0–180°, center 1500)
  ID 5 — wrist pitch       (500–2500 µs, 0–180°, center 1500)
  ID 6 — wrist rotation    (500–2500 µs, 0–180°, center 1500)

Run from any directory:
  python3 /home/pi/MasterPi/test_arm.py
"""

import time
from common.ros_robot_controller_sdk import Board

# --- Constants -----------------------------------------------------------

# Duration (seconds) for each movement segment
MOVE_TIME = 0.6

# Home position: arm upright and centered
HOME = [
    [1, 1500],  # base: center
    [3, 1500],  # shoulder: upright
    [4, 2000],  # elbow: slightly bent
    [5, 1500],  # wrist pitch: level
    [6, 1500],  # wrist rotation: center
]

# Wave sequence: rock the wrist back and forth while the shoulder bobs
WAVE_SEQUENCE = [
    # [base, shoulder, elbow, wrist_pitch, wrist_rotation]
    [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1700]],  # raise & tilt
    [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1300]],  # wave left
    [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1700]],  # wave right
    [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1300]],  # wave left
    [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1700]],  # wave right
    [[1, 1500], [3, 1200], [4, 1800], [5, 1200], [6, 1300]],  # wave left
]


def go_to(board, positions, duration=MOVE_TIME, settle=None):
    """Send a position command and wait for the motion to complete."""
    board.pwm_servo_set_position(duration, positions)
    time.sleep(settle if settle is not None else duration + 0.1)


def main():
    board = Board()
    print("Board initialized.")

    # Move to home position first
    print("Moving to home position...")
    go_to(board, HOME, duration=1.0, settle=1.5)

    # Perform the wave
    print("Waving...")
    for step in WAVE_SEQUENCE:
        go_to(board, step, duration=MOVE_TIME)

    # Return home
    print("Returning to home position...")
    go_to(board, HOME, duration=1.0, settle=1.5)

    print("Done.")


if __name__ == "__main__":
    main()
