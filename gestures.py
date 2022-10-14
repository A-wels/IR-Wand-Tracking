from enum import Enum
# List of tuples: (theta, scaled distance)

# first distance is always 1, the rest is the factor in comparison to the first
class Gesture(Enum):
    NO_GESTURE_RECOGNIZED = [(0,0)]
    
    ONE = [(-2.3,1), # up left
 (2,2),# Down
 ]