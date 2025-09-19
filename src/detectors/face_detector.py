import cv2

def create_face_detector():
    """Create and return a Haar cascade face detector."""
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    detector = cv2.CascadeClassifier(cascade_path)
    if detector.empty():
        raise RuntimeError(f'Failed to load cascade from {cascade_path}')
    return detector