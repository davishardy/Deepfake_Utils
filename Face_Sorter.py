# Face Sorter
# Created by Davis Hardy
# Created on 2022-06-22

import cv2
import os
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Warning message
print("\n")
print("Warning!!!\n"*5)
print("By continuing you understand that files in your specified directory that do not meet your criteria will be DELETED!\n")

whole_frame_dir = input("Enter the directory where your whole frames are stored")
height_px_min = int(input("What is the minimum height of the face in pixels? (Just type a number then hit enter)"))
width_px_min = int(input("What is the minimum width of the face in pixels? (Just type a number then hit enter)"))


def main(file_path, height_px_min, width_px_min):

    os.chdir(file_path)
    print(f"Pre-pop file list:\t{os.listdir(file_path)}")  # For debug

    imgs = os.listdir(file_path)  # List of images in directory
    imgs.pop(0)  # Get rid .DS_Store (May be a macos only file)

    print(f"Post-pop file list:\t{imgs}")  # For debug

    failure_imgs = []

    def sorting(height_px_min, width_px_min):
        with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
            # Using the sub 2 meter model right now. Change model_selection to 1 to search for faces farther away
            for img in imgs:
                cat_path = file_path+"/"+img  # This would need to change to "\" on Windows (Developed on Mac)
                img_in = cv2.imread(cat_path)
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection
                results = face_detection.process(cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB))

                if not results.detections:
                    # Add images with failed detections to a fail list
                    failure_imgs.append(img)  # Only stored img string to save space and increase speed
                    continue

                for detection in results.detections:
                    '''
                    print('Left Eye:')
                    # print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EYE))
                    print('Right Eye:')
                    print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE))
                    '''
                    print(img)
                    rect_data = detection.location_data
                    rect = rect_data.relative_bounding_box

                    rect_width = rect.width
                    rect_height = rect.height

                    # rect.xmin, rect.ymin, rect.width, rect.height
                    height_img_in = img_in.shape[0]
                    width_img_in = img_in.shape[1]

                    face_width_px = round(rect_width * width_img_in)
                    face_height_px = round(rect_height * height_img_in)

                    if face_width_px < width_px_min:
                        failure_imgs.append(img)

                    if face_height_px < height_px_min:
                        if img not in failure_imgs:
                            failure_imgs.append(img)

                    # Delete failures
                    for failure in failure_imgs:
                        fail_cat_path = file_path+"/"+failure  # Reverse slash if on Windows
                        os.remove(fail_cat_path)

    sorting(height_px_min, width_px_min)


main(whole_frame_dir, height_px_min, width_px_min)
