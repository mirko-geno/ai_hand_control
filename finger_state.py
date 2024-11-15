# finger_state.py
import math

def calculate_distance(landmark1, landmark2):
    """Calculate Euclidean distance between two landmarks."""
    return math.sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2 + (landmark1.z - landmark2.z)**2)

def calculate_angle(a, b, c):
    """Calculate the angle at point 'b' formed by points 'a' -> 'b' -> 'c'."""
    ba = (a.x - b.x, a.y - b.y, a.z - b.z)
    bc = (c.x - b.x, c.y - b.y, c.z - b.z)
    
    # Dot product and magnitudes
    dot_product = ba[0] * bc[0] + ba[1] * bc[1] + ba[2] * bc[2]
    mag_ba = math.sqrt(ba[0]**2 + ba[1]**2 + ba[2]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2 + bc[2]**2)
    
    if mag_ba * mag_bc == 0:
        return 180  # Avoid division by zero; assume fully extended
    
    # Calculate the angle in degrees
    angle = math.acos(dot_product / (mag_ba * mag_bc)) * (180 / math.pi)
    return angle

def check_finger_states(landmarks, handedness):
    """
    Determines which fingers are open or closed based on multiple checks.

    Parameters:
    landmarks (list): A list of landmarks for a single hand from MediaPipe.
    handedness (str): Either 'Left' or 'Right' indicating which hand is detected.

    Returns:
    dict: A dictionary with each finger as a key, and 'open' or 'closed' as the value.
    """
    
    FINGER_TIPS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
    FINGER_BASES = [2, 6, 10, 14, 18]  # Approximate bases for each finger
    FINGER_PIP = [3, 7, 11, 15, 19]  # PIP joints for angle checks

    finger_states = {
        "Thumb": "closed",
        "Index": "closed",
        "Middle": "closed",
        "Ring": "closed",
        "Pinky": "closed"
    }

    # Threshold distances for detecting "open" states (adjust based on experience)
    MIN_DISTANCE_THRESHOLDS = {
        "Thumb": 0.15,
        "Index": 0.1,
        "Middle": 0.1,
        "Ring": 0.1,
        "Pinky": 0.1
    }
    
    for i, finger in enumerate(finger_states.keys()):
        tip = landmarks[FINGER_TIPS[i]]
        base = landmarks[FINGER_BASES[i]]
        pip = landmarks[FINGER_PIP[i]]  # Proximal interphalangeal joint for angle check

        # Tip-to-Base Check
        if finger == "Thumb":
            # Adjust thumb check based on left or right hand
            if (handedness == "Right" and tip.x < base.x) or (handedness == "Left" and tip.x > base.x):
                finger_states[finger] = "open"
        else:
            if tip.y < base.y:
                finger_states[finger] = "open"

        # Distance Check
        if calculate_distance(tip, base) >= MIN_DISTANCE_THRESHOLDS[finger]:
            finger_states[finger] = "open"

        # Angle Check
        angle = calculate_angle(base, pip, tip)
        if angle < 160:  # Assuming angle below 160 degrees implies a bent finger
            finger_states[finger] = "closed"
    
    return finger_states
