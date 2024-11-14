from threading import Thread
from recognition import Hand
from time import sleep


def print_first_landmark(last_record):
    if last_record:
        # Print only the first landmark's x, y, z coordinates
        first_landmark = last_record.landmark[0]
        print(f"First landmark - x: {first_landmark.x}, y: {first_landmark.y}, z: {first_landmark.z}")
    else:
        print("No landmarks detected.")


def main():
    print("Iniciando programa...")
    hand = Hand()
    recognizer = Thread(target=hand.setup)
    recognizer.start()
    sleep(7)

    print("Leyendo resultados...")
    last_record = None

    while True:
        try:
            if hand.results and hand.results.multi_hand_landmarks:
                last_record = hand.results.multi_hand_landmarks[0]
                
        except Exception as e:
            print(f"Error accessing landmarks: {e}")

        print_first_landmark(last_record)
        sleep(1)


main()
