from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# list of camera accesses
cameras = [2, 0]


def find_camera(list_id):
    return cameras[int(list_id)]


def gen_frames(camera_id):
    # return the camera access link with credentials. Assume 0?
    cam = find_camera(camera_id)
    cap = cv2.VideoCapture(cam)  # capture the video from the live feed

    while True:
        success, frame = cap.read()  # read the camera frame
        if camera_id == "1":
            frame = cv2.flip(frame, -1)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed/<string:list_id>/', methods=["GET"])
def video_feed(list_id):
    return Response(gen_frames(list_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html', camera_list=len(cameras), camera=cameras)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
