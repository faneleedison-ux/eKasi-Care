import cv2
import numpy as np

def draw_sidebar(frame, metrics, width=220, alpha=0.7):
    """Draw a right-side panel showing icons and metric values."""
    h, w = frame.shape[:2]
    x0 = max(0, w - width)

    overlay = frame.copy()
    cv2.rectangle(overlay, (x0, 0), (w, h), (30, 30, 30), -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    pad_x = 15
    pad_y = 25
    row_h = 80
    icon_radius = 18
    font = cv2.FONT_HERSHEY_SIMPLEX

    labels = [
        ('HR', 'Heart', (0, 100, 255)),
        ('Resp', 'Resp', (200, 150, 0)),
        ('Temp', 'Temp', (0, 200, 200)),
    ]

    for i, (key, short_label, color) in enumerate(labels):
        y = pad_y + i * row_h
        cx = x0 + pad_x + icon_radius

        if key == 'HR':
            left_circle = (cx - 8, y + 18)
            right_circle = (cx + 8, y + 18)
            cv2.circle(frame, left_circle, 8, color, -1)
            cv2.circle(frame, right_circle, 8, color, -1)
            pts = np.array([[cx - 18, y + 18], [cx + 18, y + 18], [cx, y + 38]], np.int32)
            cv2.fillPoly(frame, [pts], color)
        elif key == 'Resp':
            cv2.ellipse(frame, (cx - 8, y + 18), (10, 14), 0, 0, 360, color, -1)
            cv2.ellipse(frame, (cx + 8, y + 18), (10, 14), 0, 0, 360, color, -1)
            cv2.rectangle(frame, (cx - 4, y + 10), (cx + 4, y + 36), (20, 20, 20), -1)
        else:
            bulb_center = (cx, y + 34)
            cv2.circle(frame, bulb_center, 10, color, -1)
            cv2.rectangle(frame, (cx - 4, y + 6), (cx + 4, y + 34), color, -1)

        text_x = x0 + pad_x + icon_radius * 2 + 10
        label_text = f"{short_label}"
        value = metrics.get(key, '--')
        value_text = f"{value}"

        cv2.putText(frame, label_text, (text_x, y + 18), font, 0.55, (230, 230, 230), 1, cv2.LINE_AA)
        cv2.putText(frame, value_text, (text_x, y + 42), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

def draw_exit_button(frame, text='Exit', btn_w=120, btn_h=40, margin=12):
    """Draw an exit button at the bottom-right corner and return its rect."""
    h, w = frame.shape[:2]
    x2 = w - margin
    y2 = h - margin
    x1 = x2 - btn_w
    y1 = y2 - btn_h

    cv2.rectangle(frame, (x1, y1), (x2, y2), (10, 10, 10), -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 50, 50), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(text, font, 0.8, 2)
    tx = x1 + (btn_w - tw) // 2
    ty = y1 + (btn_h + th) // 2 - 4
    cv2.putText(frame, text, (tx, ty), font, 0.8, (230, 230, 230), 2, cv2.LINE_AA)
    return (x1, y1, x2, y2)