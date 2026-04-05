#!/usr/bin/python3
import cv2
import numpy as np
import signal
import common.mecanum as mecanum

LOWER_GREEN = np.array([35, 80, 80])
UPPER_GREEN = np.array([85, 255, 255])

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CENTER_X = FRAME_WIDTH // 2

DEADZONE = 40
SPEED = 40
TARGET_RADIUS = 60

chassis = mecanum.MecanumChassis()
running = True

def stop_handler(signum, frame):
    global running
    running = False
    chassis.set_velocity(0, 0, 0)
    print("Stopped.")

signal.signal(signal.SIGINT, stop_handler)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Camera not found. Stop masterpi.service first.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    print("Egg Tracker running. Press 'q' to quit.")

    try:
        while running:
            ret, frame = cap.read()
            if not ret:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cv2.line(frame, (CENTER_X, 0), (CENTER_X, FRAME_HEIGHT), (255, 255, 0), 1)
            cv2.line(frame, (CENTER_X - DEADZONE, 0), (CENTER_X - DEADZONE, FRAME_HEIGHT), (0, 255, 255), 1)
            cv2.line(frame, (CENTER_X + DEADZONE, 0), (CENTER_X + DEADZONE, FRAME_HEIGHT), (0, 255, 255), 1)

            if contours:
                largest = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest) > 150:
                    ((cx, cy), radius) = cv2.minEnclosingCircle(largest)
                    center = (int(cx), int(cy))
                    cv2.circle(frame, center, int(radius), (0, 0, 255), 2)
                    cv2.circle(frame, center, 5, (0, 255, 0), -1)

                    error_x = int(cx) - CENTER_X

                    if abs(error_x) > DEADZONE:
                        if error_x < 0:
                            action = "STRAFE LEFT"
                            chassis.set_velocity(SPEED, 270, 0)
                        else:
                            action = "STRAFE RIGHT"
                            chassis.set_velocity(SPEED, 90, 0)
                    elif radius < TARGET_RADIUS:
                        action = "MOVE FORWARD"
                        chassis.set_velocity(SPEED, 0, 0)
                    else:
                        action = "CENTERED - STOP"
                        chassis.set_velocity(0, 0, 0)

                    label = f"{action} | cx={int(cx)} | err={error_x:+d} | r={int(radius)}px"
                    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
                else:
                    chassis.set_velocity(0, 0, 0)
                    cv2.putText(frame, "Too small - STOP", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            else:
                chassis.set_velocity(0, 0, 0)
                cv2.putText(frame, "No green - STOP", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

            cv2.imshow("B.R.U.H. Egg Tracker", frame)
            cv2.imshow("Green Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        chassis.set_velocity(0, 0, 0)
        cap.release()
        cv2.destroyAllWindows()
        print("Tracker stopped. Robot halted.")

if __name__ == "__main__":
    main()
