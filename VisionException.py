# $-----------------------------$
#
# File Name: VisionException.py
# Author: Mitchell M. Gresham
#
# $-----------------------------$

class CameraNotFound(Exception):
    """
    When no camera can be found for a video stream exception is thrown. 
    """
    def __init__(self) -> None:
        self.message = "No Camera Found for Video Stream."
        super().__init__(self.message)

class FrameNotFound(Exception):
    """
    When either the video stream has ended or the program cannot find the next frame from the video stream exception is thrown. 
    """
    def __init__(self) -> None:
        self.message = "The Next Frame from Video Stream Cannot Be Found. Has The Stream Ended?"
        super().__init__(self.message)