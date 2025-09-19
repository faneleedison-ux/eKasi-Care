import cv2
import logging
from src.components.draw import draw_sidebar, draw_exit_button
from src.utils.estimators import estimate_heart_rate, estimate_temperature, estimate_respiratory_rate
from src.detectors.face_detector import create_face_detector

class UIState:
    def __init__(self):
        self.exit_rect = None
        self.should_exit = False
        self.confirm_exit = False
        self.confirm_yes_rect = None
        self.confirm_no_rect = None
        self.window_name = None
        self.last_frame_size = None
        self.ppg_buf = []
        self.ppg_ts = []
        self.buf_maxlen = 180

    def push_ppg(self, value, ts):
        self.ppg_buf.append(float(value))
        self.ppg_ts.append(float(ts))
        if len(self.ppg_buf) > self.buf_maxlen:
            self.ppg_buf.pop(0)
            self.ppg_ts.pop(0)

def process_stream(cap, face_detector, window_name='Face Scan - HR & Temp'):
    """Process video stream for face detection and metrics overlay."""
    ui_state = UIState()
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, _mouse_callback, ui_state)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.info('End of stream or cannot read frame.')
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray_eq = clahe.apply(gray)

            min_size = max(30, int(frame.shape[0] * 0.08))
            faces = face_detector.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=4, minSize=(min_size, min_size))
            if len(faces) == 0:
                faces = face_detector.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5)

            primary = None
            max_area = 0
            for (x, y, w, h) in faces:
                area = w * h
                if area > max_area:
                    max_area = area
                    primary = (x, y, w, h)

            metrics = {'HR': '--', 'Resp': '--', 'Temp': '--'}
            for (x, y, w, h) in faces:
                color = (150, 150, 150)
                thickness = 1
                if primary and (x, y, w, h) == primary:
                    color = (255, 0, 0)
                    thickness = 2
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

            if primary is not None:
                x, y, w, h = primary
                face_roi = frame[y:y + h, x:x + w]
                heart_rate = estimate_heart_rate(face_roi)
                temperature = estimate_temperature(face_roi)
                resp_rate = estimate_respiratory_rate(face_roi)

                metrics = {
                    'HR': f'{heart_rate} bpm',
                    'Resp': f'{resp_rate} rpm',
                    'Temp': f'{temperature} C',
                }

            draw_sidebar(frame, metrics)
            ui_state.exit_rect = draw_exit_button(frame)

            if ui_state.confirm_exit:
                draw_exit_confirmation(frame, ui_state)
            else:
                ui_state.confirm_yes_rect = None
                ui_state.confirm_no_rect = None

            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or ui_state.should_exit:
                logging.info('Exiting stream processing.')
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def _mouse_callback(event, x, y, flags, param):
    """Mouse callback to detect clicks on the Exit button."""
    ui_state = param
    if event == cv2.EVENT_LBUTTONUP:
        # Check if confirmation dialog is active
        if ui_state.confirm_exit:
            if ui_state.confirm_yes_rect:
                x1, y1, x2, y2 = ui_state.confirm_yes_rect
                if x1 <= x <= x2 and y1 <= y <= y2:
                    ui_state.should_exit = True
                    return
            if ui_state.confirm_no_rect:
                x1, y1, x2, y2 = ui_state.confirm_no_rect
                if x1 <= x <= x2 and y1 <= y <= y2:
                    ui_state.confirm_exit = False
                    return

        # Check main exit button
        if ui_state.exit_rect:
            x1, y1, x2, y2 = ui_state.exit_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                ui_state.confirm_exit = True

def draw_exit_confirmation(frame, ui_state):
    """Draw a confirmation dialog with Yes and No buttons."""
    h, w = frame.shape[:2]
    dialog_w, dialog_h = 300, 150
    x1 = (w - dialog_w) // 2
    y1 = (h - dialog_h) // 2
    x2 = x1 + dialog_w
    y2 = y1 + dialog_h

    # Draw dialog background
    cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 50), -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 2)

    # Draw Yes and No buttons
    btn_w, btn_h = 100, 40
    yes_x1, yes_y1 = x1 + 30, y2 - 60
    yes_x2, yes_y2 = yes_x1 + btn_w, yes_y1 + btn_h
    no_x1, no_y1 = x2 - 30 - btn_w, y2 - 60
    no_x2, no_y2 = no_x1 + btn_w, no_y1 + btn_h

    cv2.rectangle(frame, (yes_x1, yes_y1), (yes_x2, yes_y2), (0, 200, 0), -1)
    cv2.rectangle(frame, (no_x1, no_y1), (no_x2, no_y2), (0, 0, 200), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Yes', (yes_x1 + 25, yes_y1 + 25), font, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, 'No', (no_x1 + 30, no_y1 + 25), font, 0.8, (255, 255, 255), 2)

    # Draw confirmation message
    msg = 'Are you sure you want to exit?'
    (text_w, text_h), _ = cv2.getTextSize(msg, font, 0.7, 2)
    text_x = x1 + (dialog_w - text_w) // 2
    text_y = y1 + 50
    cv2.putText(frame, msg, (text_x, text_y), font, 0.7, (255, 255, 255), 2)

    # Update UI state with button rectangles
    ui_state.confirm_yes_rect = (yes_x1, yes_y1, yes_x2, yes_y2)
    ui_state.confirm_no_rect = (no_x1, no_y1, no_x2, no_y2)