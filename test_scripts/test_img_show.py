import cv2
import numpy

img = cv2.imread('/home/brynamo/Documents/w251/bryan_working/test_img.jpg', cv2.IMREAD_UNCHANGED)


cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
