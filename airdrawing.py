import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Constants
CANVAS_HEIGHT, CANVAS_WIDTH = 480, 640
POINT_RADIUS = 8
ERASER_RADIUS = 25
LINE_WIDTH = 5
FINGER_TIPS = [8, 12, 16, 20]
CIRCLE_POINTS_THRESHOLD = 20
CIRCLE_VARIANCE_THRESHOLD = 50

# Pure, fully saturated colors with maximum density
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]
color_names = ["Red", "Green", "Blue", "Cyan"]
color_index = 0

canvas = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0
points = []

cap = cv2.VideoCapture(0)

def detect_circle(points):
    """Detect if points form a circular pattern"""
    if len(points) < CIRCLE_POINTS_THRESHOLD:
        return False

    pts = np.array(points)
    center = np.mean(pts, axis=0)
    distances = [np.linalg.norm(p - center) for p in pts]
    
    return np.var(distances) < CIRCLE_VARIANCE_THRESHOLD


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            # Extract hand landmarks
            lm_list = []
            h, w, _ = frame.shape
            
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # Detect which fingers are raised
            fingers = []
            for tip in FINGER_TIPS:
                fingers.append(1 if lm_list[tip][1] < lm_list[tip-2][1] else 0)

            x1, y1 = lm_list[8]

            # 🖐️ PAUSE - All fingers raised
            if sum(fingers) >= 4:
                cv2.putText(frame, "PAUSED", (200, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (10, 10, 100), 3)
                prev_x, prev_y = 0, 0

            # 🤟 COLOR CHANGE - 3 fingers raised
            elif fingers == [1, 1, 1, 0]:
                color_index = (color_index + 1) % len(colors)
                cv2.putText(frame, f"Color: {color_names[color_index]}", (150, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors[color_index], 2)
                prev_x, prev_y = 0, 0
                cv2.waitKey(300)

            # ✌️ ERASER - 2 fingers raised
            elif fingers == [1, 1, 0, 0]:
                cv2.circle(frame, (x1, y1), 15, (10, 50, 100), -1)
                cv2.circle(canvas, (x1, y1), ERASER_RADIUS, (0, 0, 0), -1)

                # Check if points form a circle
                if detect_circle(points):
                    pts = np.array(points)
                    center = np.mean(pts, axis=0).astype(int)
                    radius = int(np.mean([np.linalg.norm(p - center) for p in pts]))
                    cv2.circle(canvas, tuple(center), radius, colors[color_index], 3)

                points.clear()
                prev_x, prev_y = 0, 0

            # ✍️ DRAW - 1 finger raised
            elif fingers == [1, 0, 0, 0]:
                cv2.circle(frame, (x1, y1), POINT_RADIUS, colors[color_index], -1)

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x1, y1

                cv2.line(canvas, (prev_x, prev_y), (x1, y1), colors[color_index], LINE_WIDTH)
                prev_x, prev_y = x1, y1
                points.append((x1, y1))

            else:
                prev_x, prev_y = 0, 0

            # Draw hand skeleton
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    else:
        prev_x, prev_y = 0, 0

    # Merge canvas with frame
    frame = cv2.add(frame, canvas)

    # Show current color indicator box
    cv2.rectangle(frame, (10, 10), (60, 60), colors[color_index], -1)
    cv2.rectangle(frame, (10, 10), (60, 60), (255, 255, 255), 2)  # Border
    
    # Display help text
    cv2.putText(frame, "Press ESC to exit | C to clear", (200, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    cv2.imshow("Air Drawing AI - Hand Gesture Control", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break
    elif key == ord('c') or key == ord('C'):
        canvas = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), dtype=np.uint8)

cap.release()
cv2.destroyAllWindows()
cv2.destroyAllWindows()