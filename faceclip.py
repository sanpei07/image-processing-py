from turtle import right
import cv2;
import matplotlib.pyplot as plt

# 定数
CASCADE_FILE_PATH = "lbpcascade_animeface.xml"

# カスケードファイル読み込み
cascade = cv2.CascadeClassifier(CASCADE_FILE_PATH)

# 顔切り取り
def face_clip(img,resize_width = 128, resize_height = 128):
    print("face_clip")
    image_raw = img
    image_ret = image_raw.copy()
    height, width, channels = image_raw.shape[:3]

    # 画像を読み込んでグレースケール
    image_gray = image_raw.copy()
    image_gray = cv2.cvtColor(image_gray, cv2.COLOR_RGB2GRAY)

    # 顔認識を開始
    face_list = cascade.detectMultiScale(image_gray, minSize=(256,256))
    # 失敗したら終了
    if len(face_list) == 0:
        print("顔認識失敗")
        ret = []
        return ret

    # 成功したら切り取り
    for (x, y, w, h) in face_list:
        print("顔の座標 = ", x, y, w, h)

    top = y
    bottom = y + h
    left = x
    right = x + w
    image_ret = image_raw[top:bottom,left:right]
    ret = cv2.resize(image_ret,dsize = (resize_width,resize_height))

    return ret



# 顔切り取り全身
def face_clip_full_length(read_path,resize_width = 1024, resize_height = 1024):
    print("face_clip")
    image_raw = cv2.imread(read_path)
    image_ret = image_raw.copy()
    height, width, channels = image_raw.shape[:3]

    # 画像を読み込んでグレースケール
    image_gray = image_raw.copy()
    image_gray = cv2.cvtColor(image_gray, cv2.COLOR_RGB2GRAY)

    # 顔認識を開始
    face_list = cascade.detectMultiScale(image_gray, minSize=(150,150))
    # 失敗したら終了
    if len(face_list) == 0:
        print("顔認識失敗")
        return None
    # 成功したら枠を描画
    for (x, y, w, h) in face_list:
            print("顔の座標 = ", x, y, w, h)
            center = x + w/2
            center = int(center)
            center_h = y + h/2
            if center < (resize_width/2):
                center = resize_width/2
            if center > width -(resize_width/2):
                center = width -(resize_width/2)
            print(center)
            #top = int(height - (resize_height + ((height - resize_height)/2)))
            #bottom = top + resize_height
            top = int(center_h  - (resize_height/2))
            bottom = top + resize_height
            left  = int(center  - (resize_width/2))
            right = left + resize_width

    image_ret = image_raw[top:bottom,left:right]
    return image_ret
    # プロットに画像を表示
    # plt.imshow(cv2.cvtColor(image_ret, cv2.COLOR_BGR2RGB))
    # plt.show()
    

if __name__ == "main":
    print("start")