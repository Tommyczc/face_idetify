import cv2
import sys
#from PIL import Image


def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)
    width = 1280  ## 360p=480*360 /// 720p=1280*720 /// 480p=854*480 /// 1080p=1920*1080
    height = 720
    cap = cv2.VideoCapture(camera_idx)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # 告诉OpenCV使用人脸识别分类器
    classfier1 = cv2.CascadeClassifier("C:\\CV\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_alt2.xml")

    classfier2 = cv2.CascadeClassifier("C:\\CV\\opencv\\build\\etc\\haarcascades\\haarcascade_profileface.xml")
    # 识别出人脸后要画的边框的颜色，RGB格式
    color1 = (0, 0, 255)
    color2 = (0, 255, 0)
    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break

            # 将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects1 = classfier1.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        faceRects2 = classfier2.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects1) > 0:  # 大于0则检测到人脸
            for faceRect in faceRects1:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color1, 2)

                cv2.putText(frame, 'Front',
                            (x + 30, y + 30),  # 坐标
                            cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                            1,  # 字号
                            (255, 0, 255),  # 颜色
                            2)


        elif len(faceRects2) > 0:  # 大于0则检测到人脸
            for faceRect in faceRects2:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color2, 2)

                cv2.putText(frame, 'side',
                            (x + 30, y + 30),  # 坐标
                            cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                            1,  # 字号
                            (255, 0, 255),  # 颜色
                            2)

        else:pass

        # 显示图像
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

            # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        CatchUsbVideo("Identify", 0)
