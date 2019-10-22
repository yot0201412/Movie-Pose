import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, make_response
from werkzeug import secure_filename
import datetime, os
import run


ALLOWED_EXTENSIONS = set(['mp4', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)

env = ''
env = 'DEVELOP'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def api():
    f = request.files['file']
    filename = request.args.get('filename')
    output_path = run_pose(f, filename)
    print(f)
    return output_path
    # return "test"


# postされたファイルとファイル名を受け取って、OpenPose1を実行する
def run_pose(file, filename):
    dt_str = datetime.datetime.now().strftime('%Y%m%d%H%M')
    dir = 'tmp/' + dt_str
    os.makedirs(dir)
    filename = secure_filename(filename)
    file_path = dir + '/' + filename
    output_path = dir + '/' + filename.rsplit('.', 1)[0] + dt_str + '.' +filename.rsplit('.', 1)[1]
    file.save(file_path)
    run.run_pose(file_path, output_path)
    print("run_pose_save")
    # return 'fin_run'
    return output_path


if __name__ == '__main__':
    if env == 'DEVELOP':
        app.debug = True
    app.run()
