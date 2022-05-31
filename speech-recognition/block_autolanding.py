from tello import Tello
import time

def block_autolanding(Tello_instance):
    while True:
        Tello_instance.send_command("Block autolanding")
        print("Auto-landing blocked")
        time.sleep(5)