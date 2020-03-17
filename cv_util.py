import os
from datetime import datetime
from os.path import dirname

import cv2
import numpy as np

import config as cfg

class UtilCV:
    min_frame_std = 0

    def __init__(self, destiny="", percent=100, can_show=False, can_write=False):
        self.percent = percent
        self.destiny = destiny
        self.can_show = can_show
        self.can_write = can_write

    def rescale_frame(self, frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def join_images(self, img1, img2):
        new_img = np.hstack((img1, img2))
        return new_img

    def normalize_blur(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (25, 25), 0)
        return gray

    def segment_movement_video(self, file_name=0,filename_out="output.avi"):
        current_frame = 0
        num_frames_std = 0
        last_status = None


        if os.path.isfile(file_name) or file_name in (0, 1):
            cap = cv2.VideoCapture(file_name)

            for config in cfg.input['camera_box_config']:
                cap.set(config['id'], config['value'])

            ret, last_frame = cap.read()
            print('print 1 ', ret, last_frame.shape)
            if last_frame is None:
                print('last_frame ', last_frame)
                exit()

            filename_out='{}{}seg{}{}'.format(self.destiny, os.sep, os.sep, filename_out)

            last_frame = self.rescale_frame(last_frame, percent=100)

            last_frame_norm = self.normalize_blur(last_frame)
            status_motion = "STOP"

            frame_height = last_frame.shape[0]
            frame_width = last_frame.shape[1]
            out = cv2.VideoWriter(filename_out, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                                  (frame_width,frame_height))

            while cap.isOpened():
                ret, frame = cap.read()
                if frame is None:
                    break

                frame = self.rescale_frame(frame, percent=100)
                newFrame = self.normalize_blur(frame)
                out.write(frame)

                diff = cv2.absdiff(last_frame_norm, newFrame)

                media_de_cor = diff.mean()
                if media_de_cor < 0.8:
                    status_motion = "STOP"
                    current_frame = current_frame + 1
                    if self.can_write:
                        dateTimeObj = datetime.now()
                        timeStr = dateTimeObj.strftime("%H%M%S")
                        temp_name = str(num_frames_std) + "_" + timeStr
                        cv2.imwrite('{}{}seg{}{}{}'.format(self.destiny, os.sep, os.sep, temp_name, '.png'),
                                    last_frame)
                else:
                    status_motion = "MOTION"
                    if current_frame > self.min_frame_std:
                        num_frames_std = num_frames_std + 1
                        """

                        if self.can_write:
                            dateTimeObj = datetime.now()
                            timeStr = dateTimeObj.strftime("%H%M%S")
                            temp_name = str(num_frames_std) + "_" + timeStr
                            cv2.imwrite('{}{}seg{}{}{}'.format(self.destiny, os.sep, os.sep, temp_name, '.png'),
                                        last_frame)
                        ="""
                            # print("Grava Frame")

                    current_frame = 0

                if last_status != status_motion:
                    last_status = status_motion

                # print("current_frame", current_frame, " status_motion ", status_motion)

                # atualiza frame
                last_frame_norm = newFrame.copy()
                last_frame = frame.copy()
                fps = cap.get(cv2.CAP_PROP_FPS)
                if self.can_show:
                    # escreve msg na tela
                    cv2.putText(frame,
                                "Room Status: {}; Number frames stopped: {} FPS:{}".format(status_motion, num_frames_std,fps),
                                (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

                    motion_detection = self.join_images(newFrame, diff)

                    cv2.imshow('original', frame)
                    cv2.imshow('motion detection', motion_detection)

                if cv2.waitKey(33) == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()
        else:
            print("video não existe")
        return 0


if __name__ == '__main__':
    # path current of projet

    path_project = os.getcwd()
    print(path_project)
    path_project = "{}{}{}{}".format(path_project, os.sep, "data", os.sep)
    print(path_project)
    util = UtilCV(destiny=path_project, can_write=True, can_show=True)
    # video1 = path_project + "kit1.mp4"
    dateTimeObj = datetime.now()
    timeStr = dateTimeObj.strftime("%H%M%S")+".avi"
    util.segment_movement_video(file_name=cfg.input['file_name'],filename_out=timeStr)
