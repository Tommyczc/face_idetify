import socket
import cv2
from http import server
import time
PAGE = """\

    <html>

      <head>

        <title>Video Streaming Demonstration</title>

      </head>

      <body>

        <h1>Video Streaming Demonstration</h1>

        <img src="/video_feed">

      </body>

    </html>



"""

# 通过opencv获取实时视频流

video = cv2.VideoCapture(0)
width = 1920  ##360p=480*360 /// 720p=1280*720 /// 480p=854*480
height = 1080  ##
video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def get_frame(v):
    success, image = v.read()

    # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片

    ret, jpeg = cv2.imencode('.jpg', image)

    return jpeg.tobytes()


def gen(camera):
    while True:
        frame = get_frame(camera)

        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg

        yield (b'--frame\r\n'

               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class HTTPHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):  # get数据处理

        if self.path == '/':  # 跳转至默认页面

            self.send_response(301)

            self.send_header('Location', '/index.html')

            self.end_headers()

        elif self.path == '/index.html':

            content = PAGE.encode('utf-8')

            self.send_response(200)

            self.send_header('Content-Type', 'text/html')

            self.send_header('Content-Length', len(content))

            self.end_headers()

            self.wfile.write(content)

        elif self.path == '/video_feed':

            self.send_response(200)

            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')

            self.end_headers()

            while True:
                self.wfile.write(next(cam))  # 必须用next()才能运行生成器

                self.wfile.write(b'\r\n')

        else:

            self.send_error(404)

            self.end_headers()


cam = gen(video)  # 生成器
try:

    print("http server start...")

    address = ('', 8080)

    server = server.HTTPServer(address, HTTPHandler)

    server.serve_forever()

finally:

    print('done')