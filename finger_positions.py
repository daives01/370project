# https://google.github.io/mediapipe/solutions/hands.html for indices
from math import sqrt, atan, pi


def calcDistance(start, finish):
    base = abs(start.x - finish.x)
    height = abs(start.y - finish.y)
    return sqrt(base ** 2 + height ** 2)


def calcAngle(start, finish):
    base = abs(start.x - finish.x)
    height = abs(start.y - finish.y)
    return atan(base / height)


def detectFingers(hand):  # return an array of 4 booleans, from index finger to pinky, 1 is down, 0 is up
    # Thumb detection is too unstable in many positions to detect when it is closed
    isIndexClosed = calcDistance(hand.landmark[8], hand.landmark[0]) < calcDistance(hand.landmark[6], hand.landmark[0])
    isMiddleClosed = calcDistance(hand.landmark[12], hand.landmark[0]) < calcDistance(hand.landmark[10],
                                                                                      hand.landmark[0])
    isRingClosed = calcDistance(hand.landmark[16], hand.landmark[0]) < calcDistance(hand.landmark[14], hand.landmark[0])
    isPinkyClosed = calcDistance(hand.landmark[20], hand.landmark[0]) < calcDistance(hand.landmark[18],
                                                                                     hand.landmark[0])
    return [isIndexClosed, isMiddleClosed, isRingClosed, isPinkyClosed]


def detectOpenHand(hand):  # position exists if all fingers are open and pointed up
    fingersClosed = detectFingers(hand)
    fingersPointedUp = [hand.landmark[4].y < hand.landmark[3].y < hand.landmark[2].y,
                        hand.landmark[8].y < hand.landmark[7].y < hand.landmark[6].y,
                        hand.landmark[12].y < hand.landmark[11].y < hand.landmark[10].y,
                        hand.landmark[16].y < hand.landmark[15].y < hand.landmark[14].y,
                        hand.landmark[20].y < hand.landmark[19].y < hand.landmark[18].y]
    return not any(fingersClosed) and all(fingersPointedUp)


def detectFist(hand):  # position exists if fingers are in fist position (Thumb placement is not considered)
    fingersClosed = detectFingers(hand)
    fingersPointedDown = [hand.landmark[8].y > hand.landmark[7].y > hand.landmark[6].y,
                          hand.landmark[12].y > hand.landmark[11].y > hand.landmark[10].y,
                          hand.landmark[16].y > hand.landmark[15].y > hand.landmark[14].y,
                          hand.landmark[20].y > hand.landmark[19].y > hand.landmark[18].y]
    goodKnuckleAngle = calcAngle(hand.landmark[5], hand.landmark[17]) > (pi / 3)
    return all(fingersClosed) and all(fingersPointedDown) and goodKnuckleAngle


def detectThumbsUp(hand):  # position exists if thumb is pointing up and other fingers are closed
    isThumbUp = hand.landmark[4].y < hand.landmark[3].y < hand.landmark[5].y < hand.landmark[0].y
    fingersClosed = detectFingers(hand)
    return isThumbUp and all(fingersClosed)


def detectThumbsDown(hand):  # position exists if thumb is pointing down and other fingers are closed
    isThumbDown = hand.landmark[4].y > hand.landmark[3].y > hand.landmark[5].y > hand.landmark[0].y
    fingersClosed = detectFingers(hand)
    return isThumbDown and all(fingersClosed)


def detectPosition(hand, label):
    if detectOpenHand(hand):
        return "Open Hand"
    elif detectFist(hand):
        return "Fist"
    elif detectThumbsUp(hand):
        return "Thumbs Up"
    elif detectThumbsDown(hand):
        return "Thumbs Down"
    else:
        return "None Detected"
