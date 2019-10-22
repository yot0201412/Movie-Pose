import tf_pose
from tf_pose import common
import cv2
import matplotlib.pyplot as plt

IMG_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])
MOVIE_EXTENSIONS = set(['mp4'])


# 画像処理用
def get_image(img_path, output_path):
    img = common.read_imgfile(img_path, None, None)
    e = tf_pose.get_estimator(model="mobilenet_thin")
    humans = e.inference(img, upsample_size=4.0)
    image = e.draw_humans(img, humans, imgcopy=False)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    cv2.imwrite(output_path, image)
    print('fin')


# 動画保存用
def get_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    e = tf_pose.get_estimator(model="mobilenet_thin")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)

    # フレームレート(1フレームの時間単位はミリ秒)の取得
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    # ライター作成
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(output_path, fmt, frame_rate, size)

    if cap.isOpened() is False:
        print("Error opening video stream or file")
    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            humans = e.inference(image, upsample_size=4.0)
            image = e.draw_humans(image, humans, imgcopy=False)
            writer.write(image)
        else:
            break

    writer.release()
    cap.release()
    cv2.destroyAllWindows()


def run_pose(input_path, output_path):
    if input_path.rsplit('.', 1)[1] in IMG_EXTENSIONS:
        get_image(input_path, output_path)
    elif input_path.rsplit('.', 1)[1] in MOVIE_EXTENSIONS:
        get_video(input_path, output_path)
