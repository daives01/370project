from math import sqrt, atan, pi
# https://google.github.io/mediapipe/solutions/hands.html for indices


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


def detectOpenHand(hand, fingers):  # position exists if all fingers are open and pointed up
    fingersPointedUp = [hand.landmark[4].y < hand.landmark[3].y < hand.landmark[2].y,
                        hand.landmark[8].y < hand.landmark[7].y < hand.landmark[6].y,
                        hand.landmark[12].y < hand.landmark[11].y < hand.landmark[10].y,
                        hand.landmark[16].y < hand.landmark[15].y < hand.landmark[14].y,
                        hand.landmark[20].y < hand.landmark[19].y < hand.landmark[18].y]
    return not any(fingers) and all(fingersPointedUp)


def detectFist(hand, fingers):  # position exists if fingers are in fist position (Thumb placement is not considered)
    fingersPointedDown = [hand.landmark[8].y > hand.landmark[7].y > hand.landmark[6].y,
                          hand.landmark[12].y > hand.landmark[11].y > hand.landmark[10].y,
                          hand.landmark[16].y > hand.landmark[15].y > hand.landmark[14].y,
                          hand.landmark[20].y > hand.landmark[19].y > hand.landmark[18].y]
    goodKnuckleAngle = calcAngle(hand.landmark[5], hand.landmark[17]) > (pi / 4)
    return all(fingers) and all(fingersPointedDown) and goodKnuckleAngle


def detectThumbsUp(hand, fingers):  # position exists if thumb is pointing up and other fingers are closed
    isThumbUp = hand.landmark[4].y < hand.landmark[3].y < hand.landmark[5].y < hand.landmark[0].y
    goodKnuckleAngle = calcAngle(hand.landmark[5], hand.landmark[17]) < (pi / 4)
    return isThumbUp and all(fingers) and goodKnuckleAngle


def detectThumbsDown(hand, fingers):  # position exists if thumb is pointing down and other fingers are closed
    isThumbDown = hand.landmark[4].y > hand.landmark[3].y > hand.landmark[5].y > hand.landmark[0].y
    goodKnuckleAngle = calcAngle(hand.landmark[5], hand.landmark[17]) < (pi / 4)
    return isThumbDown and all(fingers) and goodKnuckleAngle


def detectPointUp(hand, fingers):  # position exists if index points straight up and other fingers are closed
    indexPointingUp = hand.landmark[8].y < hand.landmark[7].y < hand.landmark[6].y \
                        < hand.landmark[5].y < hand.landmark[0].y
    straightIndex = calcAngle(hand.landmark[6], hand.landmark[8]) < (pi / 6)
    return indexPointingUp and straightIndex and fingers[1] and fingers[2] and fingers[3]


def detectPointDown(hand, fingers):  # position exists if index points straight down and other fingers are closed
    indexPointingDown = hand.landmark[8].y > hand.landmark[7].y > hand.landmark[6].y \
                        > hand.landmark[5].y > hand.landmark[0].y
    straightIndex = calcAngle(hand.landmark[6], hand.landmark[8]) < (pi / 6)
    return indexPointingDown and straightIndex and fingers[1] and fingers[2] and fingers[3]


def detectPointLeft(hand, fingers):  # position exists if index points straight to the left and other fingers are closed
    indexPointingLeft = hand.landmark[8].x > hand.landmark[7].x > hand.landmark[6].x \
                        > hand.landmark[5].x > hand.landmark[0].x
    straightIndex = calcAngle(hand.landmark[6], hand.landmark[8]) > (pi / 3)
    return indexPointingLeft and straightIndex and fingers[1] and fingers[2] and fingers[3]


def detectPointRight(hand, fingers):  # position exists if index points straight to the right and other fingers are closed
    indexPointingRight = hand.landmark[8].x < hand.landmark[7].x < hand.landmark[6].x \
                        < hand.landmark[5].x < hand.landmark[0].x
    straightIndex = calcAngle(hand.landmark[6], hand.landmark[8]) > (pi / 3)
    return indexPointingRight and straightIndex and fingers[1] and fingers[2] and fingers[3]


def detectPosition(hand, label):    # change position to first detected position
    fingersClosed = detectFingers(hand)
    if detectOpenHand(hand, fingersClosed):
        return "Open Hand"
    elif detectFist(hand, fingersClosed):
        return "Fist"
    elif detectThumbsUp(hand, fingersClosed):
        return "Thumbs Up"
    elif detectThumbsDown(hand, fingersClosed):
        return "Thumbs Down"
    elif detectPointUp(hand, fingersClosed):
        return "Point Up"
    elif detectPointDown(hand, fingersClosed):
        return "Point Down"
    elif detectPointLeft(hand, fingersClosed):
        return "Point Left"
    elif detectPointRight(hand, fingersClosed):
        return "Point Right"
    else:
        return "None Detected"

