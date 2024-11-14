import cv2
import mediapipe as mp


class Hand:
    def __init__(self):
        self.__mp_hands = mp.solutions.hands

        # Webcam input
        self.__cap = cv2.VideoCapture(0)
        # Webcam output
        self.__image = None

        self.results = None
    

    def __print_image(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        # To draw the hand annotations on the image.
        self.__image.flags.writeable = True
        self.__image = cv2.cvtColor(self.__image, cv2.COLOR_RGB2BGR)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        self.__image,
                        hand_landmarks,
                        self.__mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(self.__image, 1))


    def get_landmarks(self, hands):
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        self.__image.flags.writeable = False
        self.__image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2RGB)
        results = hands.process(self.__image)
        return results


    def setup(self):
        with self.__mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
            ) as hands:
            
            while self.__cap.isOpened():
                _, self.__image = self.__cap.read()
                
                self.results = self.get_landmarks(hands)

                self.__print_image()
               
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self.__cap.release()


if __name__ == '__main__':
    hand = Hand()
    hand.setup()