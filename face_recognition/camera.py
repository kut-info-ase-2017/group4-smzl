import cv2

class Camera():
    '''画像関連処理（撮影、顔切り出し）を行う
    '''
    def __init__(self, cascade=None):
        if cascade is None:
            raise Exception('required cascade for clipping face from source image.')
        self.face_detecter = cv2.CascadeClassifier(cascade)
        self.cap =  cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    def get_face(self, isAllFace=False):

        ret, frame = self.cap.read()
        facerect = self.face_detecter.detectMultiScale(frame, 1.3, 2)

        faces = []
        if len(facerect) > 0:
            for (x, y, w, h) in facerect:
                cliped_img = frame[y:y + h, x:x + w]
                # 120 * 120 の画像にリサイズ
                cliped_img = cv2.resize(cliped_img, (120, 120), interpolation=cv2.INTER_AREA)
                faces.append(cliped_img)
        else:
            print('None')
            return None

        # 単一の顔画像のみを欲しい時（デフォルト）
        if not isAllFace:
            faces = faces[0]

        return faces

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    cascade = '/Users/hirto/anaconda/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
    Cam = Camera(cascade=cascade)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        face = Cam.get_face()
        if face is not None:
            cv2.imshow('frame', face)
