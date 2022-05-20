import pygame

def play_sound(filename):
    pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
    pygame.init()  # turn all of pygame on.
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def takeoff():
    play_sound('./replies/takeoff.ogg')

def land():
    play_sound('./replies/land.ogg')

def move_up():
    play_sound('./replies/move_up.ogg')

def move_down():
    play_sound('./replies/move_down.ogg')
    
def move_forward():
    play_sound('./replies/move_forward.ogg')

def move_backward():
    play_sound('./replies/move_backward.ogg')

def move_right():
    play_sound('./replies/move_right.ogg')

def move_left():
    play_sound('./replies/move_left.ogg')

def rotate_clockwise():
    play_sound('./replies/rotate_clockwise.ogg')

def rotate_counter_clockwise():
    play_sound('./replies/rotate_counter_clockwise.ogg')

def set_speed_maximum():
    play_sound('./replies/set_speed_maximum.ogg')

def set_speed_minimum():
    play_sound('./replies/set_speed_minimum.ogg')

def set_speed_moderate():
    play_sound('./replies/set_speed_moderate.ogg')

def wrong_command():
    play_sound('./replies/wrong_command.ogg')