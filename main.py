import cv2
from time import sleep
import numpy as np


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        #apply median blur, 15 means it's smoothing image 15x15 pixels
        blur = cv2.medianBlur(img,15)

        #convert to hsv
        #hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        #color definition
        red_lower = np.array([140,190,210])
        red_upper = np.array([255,255,255])

        #red color mask (sort of thresholding, actually segmentation)
        mask = cv2.inRange(blur, red_lower, red_upper)

        connectivity = 4  
        # Perform the operation
        output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)
        # Get the results

        num_labels = output[0]-1

        centroids = output[3][1:]
        #print results
        print ('number of dots, should be 4:',num_labels )
        print ('array of dot center coordinates:',centroids)
        cv2.imshow('my webcam', mask)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
        sleep(0.5)
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()