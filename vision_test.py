#!/usr/bin/env python3
"""
vision_test.py - Project B.R.U.H. Day 4: Optic Nerve Phase
Opens live camera feed and highlights bright green objects with a red circle.
Run from: ~/MasterPi/
"""

import cv2
import numpy as np

# HSV = Hue, Saturation, Value
# Hue: the actual color (0-179 in OpenCV). Green lives around 35-85.
# Saturation: how "pure" the color is (0=grey, 255=vivid).
# Value: brightness (0=black, 255=bright).
# We filter by HSV instead of RGB because lighting changes RGB values
# dramatically, but HSV stays much more stable under different lighting.

# Tune these if your green isn't being detected:
LOWER_GREEN = np.array([35, 80, 80])
UPPER_GREEN = np.array([85, 255, 255])

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open camera. Check connection.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Vision test running. Press 'q' to quit.")
    print("HSV = Hue (color), Saturation (purity), Value (brightness)")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to grab frame.")
            break

        # Convert BGR (OpenCV default) to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask: white where green is detected, black everywhere else
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

        # Clean up the mask (remove noise)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours (outlines of detected green blobs)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Pick the largest green blob
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area > 500:  # Ignore tiny specks
                ((cx, cy), radius) = cv2.minEnclosingCircle(largest)
                center = (int(cx), int(cy))

                # Draw red circle around detected object
                cv2.circle(frame, center, int(radius), (0, 0, 255), 2)
                # Draw green dot at center
                cv2.circle(frame, center, 5, (0, 255, 0), -1)

                label = f"GREEN LOCKED | Center: ({int(cx)}, {int(cy)}) | Radius: {int(radius)}px"
                cv2.putText(frame, label, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Green detected (too small)", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "No green detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        # Show both windows: the live feed AND the mask (for debugging)
        cv2.imshow("B.R.U.H. Vision Feed", frame)
        cv2.imshow("Green Mask (Debug)", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
