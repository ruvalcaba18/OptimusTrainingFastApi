from enum import Enum


class BreakDuration(int, Enum):
    SHORT = 10
    MEDIUM = 20
    LONG = 30


class BreakCategory(str, Enum):
    STRETCHING = "stretching"                      
    BREATHING = "breathing"                      
    MOBILITY = "mobility"                                
    RELAXATION = "relaxation"                   
    EYE_CARE = "eye_care"                           
    POSTURE = "posture"
