# CSU CS370 project
### Daniel Ives, Will Daknis, Kenny Hotra
## Required Python Libraries

### [MediaPipe](https://google.github.io/mediapipe/getting_started/python.html)

We're using MediaPipe for AI hand tracking,
`pip install mediapipe`

### [Pynput](https://pynput.readthedocs.io/en/latest/)

We also use pynput on the client side to send keystrokes to the host computer
`pip install pynput`

## How to Run

### Network (router)

 - make sure to give the raspberry pi a static IP address on the network
### Raspberry Pi

 - Install raspbian 10 on the pi (opencv is not compatible with raspian 11)
 - make sure to install dependencies (python/opencv/mediapipe)
 - Go into pi-gesture-controller.py and set the IP address
 - plug in a USB camera and run pi-gesture-controller.py

### Client

 - install python and pynput
 - set the IP address in client.py to the raspberry pi's IP
 - run client.py