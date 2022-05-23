from tello import Tello
from speech_to_text import speech_to_text
import replies
import time
from Levenshtein import distance as lev
import threading
from block_autolanding import block_autolanding

tello = Tello("", 8889)  # instanciation of the Tello class and connection to the drone

# Disable auto-landing
sending_command_thread = threading.Thread(target=block_autolanding, args=[tello,])
sending_command_thread.daemon = True
sending_command_thread.start()

commands = ["takeoff", "land", "upward", "downward", "forward", "backward", "right", "left", "clockwise", "counterclockwise"]
THRESHOLD = 5
again = True
while again:
    command = speech_to_text().replace(' ', '').lower()
    print(command)
    best_distance = 1000000000
    best_string = command
    for string in commands:
        distance = lev(command, string)
        print(distance, string)
        if distance < best_distance:
            best_distance = distance
            best_string = string
    
    if ( (command != '') and (best_distance <= THRESHOLD) ):
        if (best_string == "takeoff"):
            # TAKE OFF
            replies.takeoff()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.takeoff()
        
        elif (best_string == "land"):
            # LAND
            replies.land()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself
            tello.land()
        
        elif (best_string == "upward"):
            # MOVE UP by a distance between 0.2 metres and 5 metres
            replies.move_up()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.move_up(0.4)
        
        elif (best_string == "downward"):
            # MOVE DOWN by a distance between 0.2 metres and 5 metres
            replies.move_down()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself
            tello.move_down(0.4)

        elif (best_string == "forward"):
            # MOVE FORWARD by a distance between 0.2 metres and 5 metres
            replies.move_forward()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.move_forward(0.4)

        elif (best_string == "backward"):
            # MOVE BACKWARD by a distance between 0.2 metres and 5 metres
            replies.move_backward()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.move_backward(0.4)

        elif (best_string == "right"):
            # MOVE RIGHT by a distance between 0.2 metres and 5 metres
            replies.move_right()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.move_right(0.4)

        elif (best_string == "left"):
            # MOVE LEFT by a distance between 0.2 metres and 5 metres
            replies.move_left()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.move_left(0.4)

        elif (best_string == "clockwise"):  
            # ROTATE CLOCKWISE by a number of degrees between 1 and 360
            replies.rotate_clockwise()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.rotate_cw(360)

        elif (best_string == "counterclockwise"):  
            # ROTATE COUNTER-CLOCKWISE by a number of degrees between 1 and 360
            replies.rotate_counter_clockwise()  # the system communicates the command under execution
            time.sleep(4)  # latency between the communication of the command under execution and the execution itself        
            tello.rotate_ccw(360)

    else:
        # WRONG COMMAND
        replies.wrong_command()  # the system communicates the command under execution
    
    choice = input("Insert y to continue, n to stop. ")
    if (choice == 'n'):
        again = False

'''
def takeoff(self):
    # Take off
    return self.send_command('takeoff')

def land(self):
    # Land
    return self.send_command('land')

def move_forward(self, distance):
    # Moves forward for a distance in metres
    return self.move('forward', distance)

def move_backward(self, distance):
    # Moves backward for a distance in metres
    return self.move('back', distance)

def move_up(self, distance):
    # Moves up for a distance in metres
    return self.move('up', distance)

def move_down(self, distance):
    # Moves down for a distance in metres
    return self.move('down', distance)

def move_right(self, distance):
    # Moves right for a distance in metres
    return self.move('right', distance)

def move_left(self, distance):
    # Moves left for a distance in metres
    return self.move('left', distance)

def rotate_cw(self, degrees):
    # Rotates clockwise by a number of degrees between 1 and 360
    return self.send_command('cw %s' % degrees)

def rotate_ccw(self, degrees):
    # Rotates counter-clockwise by a number of degrees between 1 and 360
    return self.send_command('ccw %s' % degrees)

def get_battery(self):
    """Returns percent battery life remaining.

    Returns:
        int: Percent battery life remaining.

    """
    
    battery = self.send_command('battery?')

    try:
        battery = int(battery)
    except:
        pass

    return battery

def get_height(self):
    """Returns height(dm) of tello.

Returns:
    int: Height(dm) of tello.

    """
    height = self.send_command('height?')
    height = str(height)
    height = list(filter(str.isdigit, height))
    try:
        height = int(height)
        self.last_height = height
    except:
        height = self.last_height
        pass
    return height

def get_flight_time(self):
    """Returns the number of seconds elapsed during flight.

    Returns:
        int: Seconds elapsed during flight.

    """

    flight_time = self.send_command('time?')

    try:
        flight_time = int(flight_time)
    except:
        pass

    return flight_time

def get_speed(self):
    """Returns the current speed.

    Returns:
        int: Current speed in KPH or MPH.

    """

    speed = self.send_command('speed?')

    try:
        speed = float(speed)

        if self.imperial is True:
            speed = round((speed / 44.704), 1)
        else:
            speed = round((speed / 27.7778), 1)
    except:
        pass

    return speed
'''