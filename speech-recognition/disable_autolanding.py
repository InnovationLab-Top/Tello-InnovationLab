from tello import Tello
import time

stop_event = False
def disable_autolanding(tello):
    while True:
        global stop_event
        print(stop_event)
        if not stop_event:
            print(f"Battery level: {tello.get_battery()}")
            time.sleep(5)
        else:
            break
