import cv2
import mediapipe as mp
import time
from flask import Flask, render_template, Response, jsonify, redirect, url_for, send_from_directory
import threading
import os

# Change this line to specify the correct path to your static folder
app = Flask(__name__, static_folder='static', static_url_path='/static')

class GestureControlSystem:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Open webcam
        self.cap = None
        self.website_url = "https://techmanthan.bbhegdecollege.com"
        self.gesture_cooldown = 10  # seconds
        self.last_gesture_time = 0
        self.gesture_detected = False

    def redirect_to_countdown(self):
        time.sleep(2)  # Delay for 1 second
        self.stop_camera()
        self.gesture_detected = True

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return False
        return True

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None

    def get_frame(self):
        if not self.cap or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=4),
                    self.mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                )

                # Check for thumbs-up gesture
                if self.is_thumbs_up(hand_landmarks):
                    if time.time() - self.last_gesture_time > self.gesture_cooldown:
                        print("Thumbs up detected! Redirecting to countdown page...")
                        self.last_gesture_time = time.time()  # Update last gesture time
                        threading.Thread(target=self.redirect_to_countdown).start()

        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def is_thumbs_up(self, hand_landmarks):
        # Check if the thumb is extended and other fingers are closed
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Check if thumb is above its IP joint, and the rest of the fingers are lower than the MCP
        thumb_extended = thumb_tip.y < thumb_ip.y
        index_finger_closed = index_tip.y > index_mcp.y
        
        return thumb_extended and index_finger_closed

gcs = GestureControlSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while not gcs.gesture_detected:
            frame = gcs.get_frame()
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera')
def start_camera():
    if gcs.start_camera():
        return jsonify({"status": "started"})
    else:
        return jsonify({"status": "error", "message": "Failed to start camera"}), 500

@app.route('/stop_camera')
def stop_camera():
    gcs.stop_camera()
    return jsonify({"status": "stopped"})

@app.route('/countdown')
def countdown():
    return render_template('countdown.html', website_url=gcs.website_url)

@app.route('/check_browser_opened')
def check_browser_opened():
    return jsonify({"browser_opened": gcs.gesture_detected})

# Add this new route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
