import finger_positions 
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:3
cap = cv2.VideoCapture(1) #cv2.VideoCapture(0) starts webcam 0 
positions = []
with mp_hands.Hands(
  max_num_hands = 1,
  min_detection_confidence=0.8,
  min_tracking_confidence=0.5) as hands:
  latest_gesture = None
  count = 0
  delay = 20 #number of frames of delay
  while cap.isOpened(): #loop for each frame
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        new_gesture = finger_positions.detectFingers(hand_landmarks, results.multi_handedness[0].classification[0].label) #This will eventually be a DetectGesture() function, or something like that
        if (new_gesture == latest_gesture):
          if (count > delay): #needed for option 2 below
            continue
          count += 1
          print(count)
          if (count == delay):
            print(latest_gesture) # Eventually will be ExecuteCommand(), or something like that
            # We have two choices right here:
            # 1. reset the count, if the user holds the same gesture for a given period of time, it'll execute again.
            # count = 0
            # 2. increment the count, it'll never be executed because count > delay, user would have to switch hand positions, then switch back.
            # this approach could allow for a lower delay amount, the user just needs to switch gestures (maybe to a neutral open hand, for example) to reset the gesture
            count += 1 
        else:
          count = 0
          latest_gesture = new_gesture
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
