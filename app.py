import cv2
import numpy as np
from keras.models import load_model

classifier = load_model('./model.h5')
classifier.load_weights('./weights.h5')

fingers = {0: 'One',
           1: 'Two',
           2: 'Three',
           3: 'Four',
           4: 'Five'}


def camera_start():
    cap = cv2.VideoCapture(1)

    key = ord('a')

    while key != ord('q'):
        ret, frame = cap.read()
        frame = cv2.flip(frame, +1)
        roi = frame.copy()[frame.shape[0] - 400:frame.shape[0] - 220, frame.shape[1] - 200:frame.shape[1] - 20]
        cv2.rectangle(frame, (frame.shape[1] - 200, frame.shape[0] - 400), (frame.shape[1] - 20, frame.shape[0] - 220),
                      (0, 0, 255), 2)

        roi = cv2.resize(roi, (100, 100))

        test = roi*1./255
        test_image = np.expand_dims(test, axis=0)

        result = classifier.predict_classes(test_image)
        text = fingers[result.item(0)]
        cv2.putText(frame, text, (frame.shape[1] - 200, frame.shape[0] - 420), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255), 2, cv2.LINE_AA)
        print(text)
        cv2.imshow('result', frame)
        key = cv2.waitKey(30)

    cap.release()
    cv2.destroyAllWindows()


camera_start()
