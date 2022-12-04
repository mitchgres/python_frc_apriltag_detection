# $-----------------------------$
#
# File Name: ApriltagDetection.py
# Author: Mitchell M. Gresham
#
# $-----------------------------$

import apriltag
import cv2

import VisionException

class ApriltagDetector:
    
    def __init__(self) -> None:
        """
        When instantiated a video stream will begin and any april tags will be identified in each frame. 
        """
        self.__startDetection(self.__startStream())

    def __startStream(self) -> cv2.VideoCapture:
        """
        Starts the video stream. Goes through a number of various camera indexes until it finds one the works or thrown an exception. 
        """
        for cameraIndex in range(-1, 3):
            videoStream = cv2.VideoCapture(cameraIndex)
            
            if videoStream.isOpened():
                break
            elif cameraIndex == 2:
                raise VisionException.CameraNotFound()
            else:
                continue
    
        return videoStream

    def __createDetector(self) -> apriltag.Detector:
        """
        Creates an apriltag detector that is made for tag36h11 tags and returns it. 
        """
        return apriltag.Detector(apriltag.DetectorOptions(families="tag36h11"))

    def __findDistance(self, objectHeight, objectWidth) -> float:
        """
        Takes the object's height and width in pixels and then calculates distance to the target in mm. Mind that dependent on camera model and target used the constants 
        declared will vary. 
        """
        REAL_OBJECT_HEIGHT_AND_WIDTH_IN = 3.2
        FOCAL_DISTANCE_CONSTANT = 665

        # You'll want to take the larger of the two value as the larger will be the most accurate to the target if it's at an angle. 
        if objectHeight >= objectWidth:
            distance = (REAL_OBJECT_HEIGHT_AND_WIDTH_IN * FOCAL_DISTANCE_CONSTANT) / objectHeight
        else:
            distance = (REAL_OBJECT_HEIGHT_AND_WIDTH_IN * FOCAL_DISTANCE_CONSTANT) / objectWidth

        return distance

    def __whenApriltagDetected(self, apriltagsDetected, image) -> cv2.Mat:
            """
            Function which is called whenever an apriltag is detected. 
            """
            print("[INFO] {} Apriltags Detected.".format(len(apriltagsDetected)))
            return self.__drawAroundApriltags(apriltagsDetected, image)

    def __drawAroundApriltags(self, apriltags, image) -> cv2.Mat:
        """
        When called it puts a bounding box around all the apriltags and write on them their X & Y pixel displacement along with their calculated distance. 
        """
        FONT = cv2.FONT_HERSHEY_SIMPLEX
        for apriltag in apriltags:
         # Identify courners and convert then to integers that represent coordinates based on resolution of camera. 
            (ptA, ptB, ptC, ptD) = apriltag.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))

        # Draws a bounding box around the detected apriltag for visualization. 
            cv2.line(image, ptA, ptB, (0, 255, 0), 2)
            cv2.line(image, ptB, ptC, (0, 255, 0), 2)
            cv2.line(image, ptC, ptD, (0, 255, 0), 2)
            cv2.line(image, ptD, ptA, (0, 255, 0), 2)

            targetSizeX = ptA[0] - ptB[0]
            targetSizeY = ptA[1] - ptD[1]
            targetDistance = self.__findDistance(targetSizeY, targetSizeX)

        # Draws the dimensions of the box on the image along with it's distance to the camera. 
            cv2.putText(image, "X: {}px | Y: {}px | Distance {}in".format(targetSizeX, targetSizeY, round(targetDistance, 2)), (ptA[0], ptA[1] - 15),
		        FONT, 0.5, (0, 255, 0), 2)

        return image

    def __showVideo(self, image) -> None:
        # Opens the window and then waits for a keypress to stop. 
        cv2.imshow("Apriltag Detection", image)


    def __startDetection(self, videoStream) -> None:
        """
        Infinite loop which loops through the frames in the video to find apriltags and then output to console the number found. 
        """
        while(True):
            # Analyze the video stream frame-by-frame. 
            ret, frame = videoStream.read()

            # Assures that the frame has been read correctly. If not then an exception is thrown. 
            if not ret:
                raise VisionException.FrameNotFound()

            # Changes the image to a single-channel (black and white).
            grayedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Outputs the number of apriltags detected. 
            apriltagDetector = self.__createDetector()
            detectedTags = apriltagDetector.detect(grayedFrame)
            numDetected = len(detectedTags)

            if numDetected != 0:
                self.__showVideo(self.__whenApriltagDetected(detectedTags, frame))
            else:
                print("[INFO] No Apriltags Detected")
                self.__showVideo(frame)
            
            # I'll be honest I don't know why this makes it work but it does. Without this the program won't display I think it's a Ubuntu thing. 
            cv2.waitKey(1)


        


            

                        

