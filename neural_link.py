#!/usr/bin/python3
import sys
sys.path.append('/home/pi/MasterPi')
import time
import signal
import common.sonar as Sonar
import common.mecanum as mecanum

THRESHOLD = 15.0
FORWARD_SPEED = 70
BACKUP_SPEED = 50
TURN_TIME = 0.65

car = mecanum.MecanumChassis()
sonar = Sonar.Sonar()
running = True

def stop_handler(signum, frame):
    global running
    running = False
    car.set_velocity(0, 0, 0)
    print('Neural Link disengaged.')

signal.signal(signal.SIGINT, stop_handler)

def get_distance():
    readings = []
    for _ in range(7):
        d = sonar.getDistance() / 10.0
        if 2.0 < d < 400.0:
            readings.append(d)
        time.sleep(0.01)
    if not readings:
        return 999.0
    readings.sort()
    return readings[len(readings) // 2]

def stop():
    car.set_velocity(0, 0, 0)

print('B.R.U.H. NEURAL LINK - Autonomous Mode')
print('Threshold: 15cm | Power: 70%')
print('Press Ctrl+C to stop')
time.sleep(1)

try:
    while running:
        dist = get_distance()
        print('Distance: %.1fcm' % dist, end='')
        if dist > THRESHOLD:
            print(' -> FORWARD')
            car.set_velocity(FORWARD_SPEED, 0, 0)
        else:
            print(' -> OBSTACLE')
            stop()
            time.sleep(0.3)
            print('  -> Backing up...')
            car.set_velocity(BACKUP_SPEED, 180, 0)
            time.sleep(1.0)
            stop()
            time.sleep(0.3)
            print('  -> Turning 90 degrees...')
            car.set_velocity(0, 90, 0.5)
            time.sleep(TURN_TIME)
            stop()
            time.sleep(0.3)
        time.sleep(0.05)
finally:
    stop()
    print('Neural Link shutdown complete.')
