# Bring in mss
from mss import mss
# Bring in opencv for rendering 
import cv2
import numpy as np
import time
import uuid
import os 
# bring in pynput for keypress capture
from pynput.keyboard import Key, Listener 

class GamePlay(): 
    def __init__(self): 
        # Setup the game area 
        self.game_area = {"left": 0, "top": 0, "width": 960, "height": 540}
        self.capture = mss()
        self.current_keys = None 

    def collect_gameplay(self):
        # Listen for keystrokes
        listener = Listener(on_press=self.on_keypress, on_release=self.on_keyrelease) 
        listener.start() 
        
        # Collect the frames
        filename = os.path.join('data', str(uuid.uuid1()))
        gamecap = np.array(self.capture.grab(self.game_area)) 
        cv2.imwrite(f'{filename}.jpg', gamecap)
        if self.current_keys:  
            np.savetxt(f'{filename}.txt', np.array([str(self.current_keys)]), fmt='%s')

    def on_keypress(self, key): 
        if self.current_keys == key:
            print(self.current_keys)
            return self.current_keys
        else: 
            print(self.current_keys)
            self.current_keys = key
            return self.current_keys 

    def on_keyrelease(self, key): 
        self.current_keys = None
        if key == Key.esc: 
            return False
    

if __name__ == '__main__':
    # Sleep for 10 seconds to allow us to get back into the game 
    time.sleep(10)
    game = GamePlay()
    while True: 
        time.sleep(1)
        game.collect_gameplay()
