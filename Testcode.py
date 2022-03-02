# This file is for testing code snippets before implementing into the main programme

#!/usr/bin/env python3

from traceback import FrameSummary
import cv2
import numpy as np
import glob

images_left = glob.glob('./CalPicsRGB/*.jpg')
print(f"{len(images_left)} pictures added")

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp_left = np.zeros((6*8,3), np.float32)
objp_left[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

objpoints_left = [] # 3d point in real world space
imgpoints_left = [] 

i=1

for fname in images_left[:10:]:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints_left.append(objp_left)
            corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints_left.append(corners)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (8,6), corners2, ret)
            cv2.imshow('img'+str(i), img)
            cv2.waitKey(1000)
            i+=1
ret_left, mtx_left, dist_left, rvecs_left, tvecs_left = cv2.calibrateCamera(objpoints_left, imgpoints_left,gray.shape[::-1], None, None)
img=cv2.imread('CalPicsRGB/CalRgb19.jpg')
h,w=img.shape[:2]
newcameramtx_left,roi_left=cv2.getOptimalNewCameraMatrix(mtx_left,dist_left,(w,h),1,(w,h))
#np.save('./CalData/test_mtx_left.npy',mtx_left)
#np.save('./CalData/test_dist_left.npy',dist_left)
#np.save('./CalData/test_newcameramtx.npy',newcameramtx_left)




cv2.imshow('undistorted',cv2.undistort(img,mtx_left,dist_left,None,newcameramtx_left))
cv2.waitKey(0)