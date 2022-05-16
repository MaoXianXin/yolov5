import cv2
import os


source = '/home/mao/Downloads/岚的瞬间.mp4'
save_dir = '/home/mao/Pictures/extracted_frames'
cap = cv2.VideoCapture(source)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)  # warning: may return 0 or nan
frame_count = max(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 0)

cnt = 1
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    if cnt % 30 == 0:
        cv2.imwrite(os.path.join(save_dir, str(cnt)+'.jpg'), frame)
    cnt += 1
print(1)