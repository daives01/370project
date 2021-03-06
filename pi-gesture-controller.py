import socket
import sys
import finger_positions
import cv2
import mediapipe as mp


def main():
    IP = "192.168.0.121"
    PORT = 6900
    # Set up socket
    clientsocket = None
    try:
        HEADERSIZE = 8
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((IP, PORT))
        print("Connecting...")
        s.listen(5)

        while True:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established.")

            msg = "Connection Created!\nGesture Controller starting up..."
            msg = f"{len(msg):<{HEADERSIZE}}"+msg

            clientsocket.send(bytes(msg, "utf-8"))
            try:
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing_styles = mp.solutions.drawing_styles
                mp_hands = mp.solutions.hands

                # For webcam input:3
                # cv2.VideoCapture(0) starts webcam 0
                cap = cv2.VideoCapture(0)
                latest_gesture = "None Detected"
                with mp_hands.Hands(
                        max_num_hands=1,
                        min_detection_confidence=0.8,
                        min_tracking_confidence=0.5) as hands:
                    count = 0
                    delay = 10  # number of frames of delay
                    while cap.isOpened():  # loop for each frame
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
                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:
                                new_gesture = finger_positions.detectPosition(
                                    hand_landmarks, results.multi_handedness[0].classification[0].label)
                                if new_gesture == latest_gesture:
                                    if count > delay:
                                        msg = "none"
                                        msg = f"{len(msg):<{HEADERSIZE}}" + msg 
                                        # SEND MESSAGE OVER SOCKET
                                        clientsocket.send(bytes(msg, "utf-8"))
                                        continue
                                    count += 1
                                    # print(count)
                                    if count == delay:
                                        if latest_gesture != "None Detected":
                                            # add length of text to start of msg
                                            msg = f"{len(latest_gesture):<{HEADERSIZE}}" + \
                                                latest_gesture
                                            # SEND MESSAGE OVER SOCKET
                                            clientsocket.send(bytes(msg, "utf-8"))
                                        print(msg)
                                        count += 1
                                else:
                                    msg = "none"
                                    msg = f"{len(msg):<{HEADERSIZE}}" + msg 
                                    # SEND MESSAGE OVER SOCKET
                                    clientsocket.send(bytes(msg, "utf-8"))
                                    count = 0
                                    latest_gesture = new_gesture
                        elif cv2.waitKey(5) & 0xFF == 27:
                            break
                        else:
                            latest_gesture="None Detected"
                            msg = "none"
                            msg = f"{len(msg):<{HEADERSIZE}}" + msg 
                            # SEND MESSAGE OVER SOCKET
                            clientsocket.send(bytes(msg, "utf-8"))
                            continue

            except:
                print("connection lost, looking for new one...")
                clientsocket.close()
                cap.release()
                continue

    except KeyboardInterrupt:
        print("\nStopping...")
        clientsocket.close()
        cap.release()
        sys.exit()


if __name__ == "__main__":
    main()