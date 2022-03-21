# https://google.github.io/mediapipe/solutions/hands.html for indices

def detectFingers(hand, label): #return an array of 5 booleans, from thumb to pinky, 1 is down, 0 is up
    isThumbClosed = hand.landmark[4].x < hand.landmark[2].x if label == "Left" else hand.landmark[4].x > hand.landmark[2].x #thumb is a little weird, because it's sideways
    isIndexClosed = hand.landmark[8].y > hand.landmark[6].y
    isMiddleClosed = hand.landmark[12].y > hand.landmark[10].y
    isRingClosed = hand.landmark[16].y > hand.landmark[14].y
    isPinkyClosed = hand.landmark[20].y > hand.landmark[18].y
    return [isThumbClosed, isIndexClosed, isMiddleClosed, isRingClosed, isPinkyClosed]
    
