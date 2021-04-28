import cv2
import numpy as np
import pyautogui


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)

    pre_pos = None
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        #apply median blur, 15 means it's smoothing image 15x15 pixels
        blur = cv2.medianBlur(img,15)

        #convert to hsv
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        #color definition
        color_lower = np.array([70,32,21])
        color_upper = np.array([95,185,131])

        #red color mask (sort of thresholding, actually segmentation)
        mask = cv2.inRange(hsv, color_lower, color_upper)

        connectivity = 4  
        # Perform the operation
        output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)
        # Get the results
        try:
            print('Main coord:', list(output[3][1]))
            pos = [*output[3][1]]
            if pre_pos and cv2.waitKey(1) == 17:
                pyautogui.move(pos[0] - pre_pos[0], pos[1] - pre_pos[1])

            pre_pos = pos
            #pyautogui.moveTo(*list(output[3][1]))
            num_labels = output[0]-1

            centroids = output[3][1:]
        
            #print results
            print ('number of dots, should be 1:', num_labels )
            print ('array of dot center coordinates:', centroids)
        except Exception:
            pass

        cv2.imshow('Green Mask', mask)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()