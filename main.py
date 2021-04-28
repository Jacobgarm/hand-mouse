import cv2
import numpy as np
import pyautogui
import keyboard

def track_mouse(mirror=False):
    cam = cv2.VideoCapture(0)

    sensitivity = 3
    pre_pos = None
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)

        img = cv2.flip(img, 0)

        blur = cv2.medianBlur(img,15)

        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        color_lower = np.array([65,30,20])
        color_upper = np.array([100,190,135])

        mask = cv2.inRange(hsv, color_lower, color_upper)

        connectivity = 2  
        output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)

        if len(output[3]) > 1:
            pos = [*output[3][1]]
            #print('Position:', pos)

            if pre_pos and not keyboard.is_pressed('ctrl'):
                pyautogui.move((pos[0] - pre_pos[0]) * sensitivity, (pos[1] - pre_pos[1]) * sensitivity)

            pre_pos = pos

        cv2.imshow('Green Mask', mask)

        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    track_mouse(mirror=True)


if __name__ == '__main__':
    main()