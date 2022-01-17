from myorawfast_collect import MyoMain
from myo_collect import *

def emg_buffer_handler(emg_buffer, *args):
    print(None)

if __name__ == "__main__":
    window = MyGame()
    window.setup()
    arcade.run()
    # ID = input('Please enter subject ID: ')
    # mm = MyoMain(ID)
    # # mm.add_emg_buffer_handler(emg_buffer_handler)

    # mm.connect()
    # mm.no_sleep()
    # mm.start_collect()