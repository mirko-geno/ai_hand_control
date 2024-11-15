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
    ser = Serial(port="/dev/ttyUSB0", baudrate=9600)
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

        # Get finger states and convert to binary (5 bits)
        finger_states = get_finger_states(last_record, handedness)
        finger_states = list(map(to_array, finger_states.values()))

        # Create a 5-bit integer by shifting each bit into place
        finger_byte = 0
        for i, state in enumerate(finger_states):
            finger_byte |= (state << i)  # Set the i-th bit to the finger state (0 or 1)

        # Make sure to send the byte with 3 additional zeros as the higher bits
        # finger_byte is a 5-bit number, we need to shift it to fit into a full byte (8 bits)
        finger_byte = finger_byte & 0x1F  # Mask to ensure only the lower 5 bits are used (0x1F = 31)

        # Send the byte over the serial connection
        ser.write(bytes([finger_byte]))
        print(f"Sent to Arduino: {finger_byte:08b}")  # Print the byte in binary for confirmation
        
        sleep(1)

    ser.close()

main()
