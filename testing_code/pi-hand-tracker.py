import finger_positions 
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:3
cap = cv2.VideoCapture(0) #cv2.VideoCapture(0) starts webcam 0 
positions = []
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened(): #loop for each frame
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        oldPos = positions 
        positions = finger_positions.detectFingers(hand_landmarks, results.multi_handedness[0].classification[0].label) #THIS ONLY SUPPORTS 1 HAND AT A TIME
        if (oldPos != positions):
          print(positions)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
