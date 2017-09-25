import cv2
import dlib

class Camera():
    '''画像関連処理（撮影、顔切り出し）を行う
    '''
    def __init__(self, cascade=None):
        if cascade is not None:
            self.face_detecter = cv2.CascadeClassifier(cascade)
        self.cap =  cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    def get_face(self, isAllFace=False):
        try:
            face_list = []
            ret, frame = self.cap.read()
            if len(frame) == 0:
                return None
            ### open cv で顔を切り出す場合 ###
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # facerect = self.face_detecter.detectMultiScale(img, 1.3, 2)
            # for (x, y, w, h) in facerect:
            #     cliped_img = frame[y:y + h, x:x + w]
            #     # 120 * 120 の画像にリサイズ
            #     cliped_img = cv2.resize(cliped_img, (120, 120), interpolation=cv2.INTER_AREA)
            #     cv2.imwrite(_dir + '/faces/' + name, cliped_img)
            # if len(facerect) > 0:
            #     for (x, y, w, h) in facerect:
            #         cliped_img = frame[y:y + h, x:x + w]
            #         # 120 * 120 の画像にリサイズ
            #         cliped_img = cv2.resize(cliped_img, (120, 120), interpolation=cv2.INTER_AREA)
            #         faces.append(cliped_img)

            ### dlib で顔を切り出す場合 ###
            detector = dlib.get_frontal_face_detector()
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = detector(img_rgb, 1)

            if len(faces) > 0:
                for face in faces:
                    top = face.top()
                    bottom = face.bottom()
                    left = face.left()
                    right = face.right()
                    height, width = frame.shape[:2]
                    # イレギュラーな顔領域は無視
                    if not top < 0 and left < 0 and bottom > height and right > width:
                        break
                    img = frame[top:bottom, left:right]
                    img = cv2.resize(img, (120, 120), interpolation=cv2.INTER_AREA)
                    face_list.append(img)

            if len(face_list) == 0:
                print('None')
                return None

            # 単一の顔画像のみを欲しい時（デフォルト）
            if not isAllFace:
                face_list = face_list[0]

            return face_list
        except Exception as e:
            print(e)
            return None

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    Cam = Camera()
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        face = Cam.get_face()

        if face is not None:
            cv2.imshow('frame', face)
