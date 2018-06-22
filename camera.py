import cv2
import os
import datetime
import time

FPSTEST_FCOUNT = 100  # FPS-test frame count

vobj = cv2.VideoCapture() # camera object basically
vobj.open(0)  # open first camera (only camera as far as I'm concerned :] )


# VIDEO WRITING VARS:

video_width, video_height = vobj.get(cv2.CAP_PROP_FRAME_WIDTH), vobj.get(cv2.CAP_PROP_FRAME_HEIGHT)
# these two should really be constants

frame_size = int(video_width), int(video_height)
fps = 7.5
# fps is specific to your camera and computer. Run a FPS test and change this variable manually
# to best fit your needs

vw_fourcc = cv2.VideoWriter.fourcc(*'MJPG')
# something cv2 needs. Don't change unless you know what you're doing

vw = None
# vw will be the video object, at the start no video is being recorded so we just say it's None


cv2.namedWindow("view")
# Makes a window with the name of "view"

recstatus = False
# a bool which stores if we're currently recording a video

fpstfc = -1  # FPS-test frame count, this "controls" FPS-test
start_time = None  # start time of FPS-test

while True:
    # main loop of program. Every iteration is a frame

    if fpstfc == 0:
        # if we reached the end of FPS-test, we calculate results and output them
        fin_time = time.time()  # finishing time

        time_diff = fin_time - start_time  # time taken to record FPSTEST_FCOUNT

        fps_est = FPSTEST_FCOUNT / time_diff  # FPS estimate

        print("FPS estimate: {}".format(fps_est))
        # to be honest I didn't expect this to work on python 2
        
        fpstfc -= 1  # decrement this for the last time in this test, stopping it

    elif fpstfc > 0:
        # while FPS-test is running, we just decrement the frame counter
        fpstfc -= 1

    __, image = vobj.read()  # reads image from the camera
    cv2.imshow("view", image)  # show on screen

    if recstatus: vw.write(image)  # if we're recording, write frame to file
    
    key = cv2.waitKey(1)  # get key, if it's pressed (in 1 milisecond)
    
    if key != -1:
        
        if key == 114:  # R key

            if recstatus:
                # if we're reconrding, stop
                recstatus = False
                print("Recording finished")
                vw.release()  # finish writing to file
                vw = None

            else:
                # if we're not recording, start
                recstatus = True
                print("Recording started")

                vw = cv2.VideoWriter()

                date_and_time = datetime.datetime.now().strftime("rec_%d_%m_%Y__%H_%M_%S")

                fname = os.getcwd() + '/' + date_and_time + '.avi'
                vw.open(
                    filename=fname,
                    fourcc=vw_fourcc,
                    fps=fps,
                    frameSize=frame_size,
                    isColor=True,
                    apiPreference=0
                )

                if not vw.isOpened():
                    # if we can't open the file, don't record
                    print("Unable to open file. Not recording.")
                    recstatus = False
                    vw = None

        elif key == 113:  # Q key
            break
        
        elif key == 102:  # F key
            if fpstfc != -1:
                print("A FPS test is already running! Be patient.")
            else:
                fpstfc = FPSTEST_FCOUNT
                start_time = time.time()
                print("Started FPS test")

        else:
            print("Key not reckognised: {}".format(key))

# stop recording if we quit before stopping manually
if vw is not None: vw.release()

