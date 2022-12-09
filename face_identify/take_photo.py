import cv2
import sys
import time


# from PIL import Image

def CatchUsbVideo(window_name, camera_idx, front_num_photo, profile_num_photo):
    cv2.namedWindow(window_name)
    front_num = 0
    profile_num = 0
    width = 1280  ## 360p=480*360 /// 720p=1280*720 /// 480p=854*480 /// 1080p=1920*1080
    height = 720
    cap = cv2.VideoCapture(camera_idx)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # 告诉OpenCV使用人脸识别分类器
    classfier1 = cv2.CascadeClassifier("C:\\Users\\Tommy\\PycharmProjects\\face_idetify\\face_identify\\model\\haarcascades\\haarcascade_frontalface_alt2.xml")
    classfier2 = cv2.CascadeClassifier("C:\\Users\\Tommy\\PycharmProjects\\face_idetify\\face_identify\\model\\haarcascades\\haarcascade_profileface.xml")

    # 识别出人脸后要画的边框的颜色，RGB格式
    color1 = (0, 0, 255)
    color2 = (0, 255, 0)
    # 存储照片的路径
    # path1='F:\\CV\\didi_photo\\front'
    # path2='F:\\CV\\didi_photo\\profile'
    # path3 = 'F:\\CV\\didi_photo\\other'

    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break

            # 将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects1 = classfier1.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        faceRects2 = classfier2.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

        if len(faceRects1) > 0 and front_num < front_num_photo:  # 大于0则检测到人脸
            for faceRect in faceRects1:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color1, 2)

                # c = cv2.waitKey(10)
                # if c & 0xFF == ord('i'):
                #     img_name = '%s/%d.jpg' % (path1, front_num)
                #     image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                #     cv2.imwrite(img_name, image)
                #     front_num += 1
                #     print('front saved')
                #     # time.sleep(1)

        if len(faceRects2) > 0 and profile_num < profile_num_photo:  # 大于0则检测到人脸
            for faceRect in faceRects2:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color2, 2)

                c = cv2.waitKey(10)
                if c & 0xFF == ord('i'):
                    #     img_name = '%s/%d.jpg' % (path2, profile_num)
                    #     image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                    #     cv2.imwrite(img_name, image)
                    #     profile_num += 1
                    print('profile saved')
                #     #time.sleep(1)

        if len(faceRects2) == 0 and len(
                faceRects1) == 0 and profile_num < profile_num_photo and front_num < front_num_photo:
            c = cv2.waitKey(10)
            if c & 0xFF == ord('i'):
                #     img_name = '%s/%d.jpg' % (path3, profile_num)
                #     cv2.imwrite(img_name, frame)
                #     profile_num += 1
                print('unknowed saved')

        if profile_num >= profile_num_photo and front_num >= front_num_photo:
            # print('reach max')
            break;

        else:
            pass

        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break;
            # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        CatchUsbVideo("Identify", 0, 20, 20)
