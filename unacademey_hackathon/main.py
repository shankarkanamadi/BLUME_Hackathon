from flask import Flask, render_template, Response
from pkg.video1 import RecordedVideo

global_frame = None
path = "small.mp4"
video_recorded = RecordedVideo(path)
app = Flask(__name__)


def video_stream():
    global global_frame

    while video_recorded is not None:

        #frame = video_camera.get_frame()
        frame = video_recorded.get_frame()
        # print('cam_release ',cam_release)
        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@app.route('/')
def index():
    global video_recorded
    video_recorded = RecordedVideo(path,"tt.jpg")
    return render_template("index.html")

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
