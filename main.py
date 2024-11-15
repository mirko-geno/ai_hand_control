from recognition import Hand
from finger_state import check_finger_states
from threading import Thread
from time import sleep
from serial import Serial

STARTUP_TIME = 7


def to_array(value):
    if value == 'open':
        value = 1
    else:
        value = 0
    return value


def get_finger_states(last_record, handedness):
    if last_record:
        finger_states = check_finger_states(last_record.landmark, handedness)
        print(f"Finger states: {finger_states}")
    else:
        print("No landmarks detected.")
    
    return finger_states


def main():
    print("Starting program...")
    ser = Serial(port="COM6", baudrate=9600)
    hand = Hand()
    recognizer = Thread(target=hand.setup)
    recognizer.start()
    sleep(STARTUP_TIME)

    print("Reading results...")
    last_record = None

    while True:
        try:
            if hand.results and hand.results.multi_hand_landmarks:
                last_record = hand.results.multi_hand_landmarks[0]
                # Retrieve hand side
                handedness = hand.results.multi_handedness[0].classification[0].label

        except Exception as e:
            print(f"Error accessing landmarks: {e}")

        finger_states = get_finger_states(last_record, handedness)
        finger_states = list(map(to_array, finger_states.values()))
        finger_states_str = ",".join(map(str, finger_states))
        
        ser.write(finger_states_str.encode("utf-8") + b'\n')
        print(f"Sent to Arduino: {finger_states_str}")
        sleep(1)

    ser.close()

main()
