import cv2
import mediapipe as mp


class Hand:
    def __init__(self):
        self.mp_hands = mp.solutions.hands

        # Webcam input
        self.cap = cv2.VideoCapture(0)
        # Webcam output
        self.image = None
    

    def print_image(self, results):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        # To draw the hand annotations on the image.
        self.image.flags.writeable = True
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            results.multi_hand_landmarks[0]

            for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        self.image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(self.image, 1))


    def get_landmarks(self, hands):
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        self.image.flags.writeable = False
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        results = hands.process(self.image)
        return results


    def setup(self):
        with self.mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
            ) as hands:
            
            while self.cap.isOpened():
                _, self.image = self.cap.read()
                
                results = self.get_landmarks(hands)

                self.print_image(results)
               
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self.cap.release()


if __name__ == '__main__':
    hand = Hand()
    hand.setup()