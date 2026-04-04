#!/usr/bin/python3
# coding=utf8
import sys
import time
import signal
import common.mecanum as mecanum

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

chassis = mecanum.MecanumChassis()
running = True

def stop(signum, frame):
    global running
    running = False
    chassis.set_velocity(0, 0, 0)
    print('Stopped.')

signal.signal(signal.SIGINT, stop)

# set_velocity(speed, direction_angle, rotation)
# direction_angle: 90 = right, 270 = left
# speed: 0-100, rotation: 0 = no spin

if __name__ == '__main__':
    print("Strafing RIGHT for 2 seconds...")
    chassis.set_velocity(50, 90, 0)
    time.sleep(2)

    chassis.set_velocity(0, 0, 0)
    time.sleep(0.3)

    print("Strafing LEFT for 2 seconds...")
    chassis.set_velocity(50, 270, 0)
    time.sleep(2)

    chassis.set_velocity(0, 0, 0)
    print("Strafe test complete!")
