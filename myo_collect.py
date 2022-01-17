# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 21:12:28 2021

@author: haopi
"""

import arcade
import random
import numpy as np
from myorawfast_collect import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Myo_Gesture_Collection"


class MyGame(arcade.Window):
    """ Our custom Window Class"""
        
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        ID = input('Please enter subject ID: ')
        self.side = input('Please enter which side is wearing the armband (left / right): ')
        self.mm = MyoMain(ID)
        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.current_idx = 0
        self.length = 0
        self.label = 'Rest'
        self.status = 'Perform the gesture when the timer turns green'
        self.trainingSide = 'False'
        self.color = arcade.color.WHITE
        self.total_time = 0.0
        self.output = "00:00:00"
        self.magnitude = list(np.zeros(8))
        arcade.set_background_color(arcade.color.AMAZON)
        
        self.isInitialize = False
        self.isRecord = False
        self.isEnd = False
        self.isReconnect = False
        
        self.gesture_list = ['Rest', 'Cylinder Grasp', 'Spherical Grasp','Lateral Pinch', 'Opposition']\
            
        self.trial_num_dict = dict(zip(['Rest', 'Cylinder Grasp', 'Spherical Grasp', 'Lateral Pinch', 'Opposition'], [1, 1, 1, 1, 1]))
        self.trial_num = 1


    def setup(self):
        """ Set up the game and initialize the variables. """
        self.length = 0
        self.label = 'Rest'
        self.trainingSide = 'False'
        self.total_time = 0.0
        self.color = arcade.color.WHITE
        


    def on_draw(self):
        """ Draw everything """
        arcade.start_render()

        # Output the timer text.
        if (self.isRecord):
            arcade.draw_text(self.output,
                             SCREEN_WIDTH /2, 25,
                             arcade.color.GREEN, 20,
                             anchor_x="center")
        else:
            arcade.draw_text(self.output,
                             SCREEN_WIDTH /2, 25,
                             arcade.color.RED, 20,
                             anchor_x="center")

        # Status
        arcade.draw_text(self.status,
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT* 0.15 + 10,
                         arcade.color.WHITE, 20,
                         anchor_x="center")
        
        # Tooltips      
        arcade.draw_text("Up: Connect Myo",
                         20, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 15,
                         anchor_x="left")
        
        arcade.draw_text("Space: Start timer for each trial (3 secs prep. / 5 secs record)",
                         20, SCREEN_HEIGHT - 55,
                         arcade.color.WHITE, 15,
                         anchor_x="left")
        
        arcade.draw_text("Right: Next Gesture",
                         20, SCREEN_HEIGHT - 80,
                         arcade.color.WHITE, 15,
                         anchor_x="left")
        
        arcade.draw_text("Left: Last Gesture",
                         20, SCREEN_HEIGHT - 105,
                         arcade.color.WHITE, 15,
                         anchor_x="left")
        
        arcade.draw_text("Esc: Disconnect Myo and save data",
                         20, SCREEN_HEIGHT - 130,
                         arcade.color.WHITE, 15,
                         anchor_x="left")
        
        # Label
        
        arcade.draw_lrtb_rectangle_outline(SCREEN_WIDTH / 2 - 200, SCREEN_WIDTH / 2 + 200, SCREEN_HEIGHT* 0.10 + 30,
                                           SCREEN_HEIGHT* 0.15 - 40, arcade.color.WHITE, border_width=3)
        
        if (self.isRecord):

            arcade.draw_lrtb_rectangle_filled(SCREEN_WIDTH / 2 - 200,
                                              SCREEN_WIDTH / 2 -200 + (self.total_time % 5.2) / 5.2 * 400,
                                              SCREEN_HEIGHT* 0.10 + 29,
                                              SCREEN_HEIGHT* 0.15 - 39,
                                              arcade.color.BRIGHT_GREEN)
            
        arcade.draw_text(f"{self.label} ({self.trial_num})", SCREEN_WIDTH / 2, SCREEN_HEIGHT* 0.10,
                         arcade.color.WHITE, 20, anchor_x="center")


        # draw channel bars
        for channel in range(0, 8):
            arcade.draw_lrtb_rectangle_outline(100 + 75*channel, 150 + 75*channel, 450,
                                               150, arcade.color.WHITE, border_width=2)

            arcade.draw_lrtb_rectangle_filled(102 + 75*channel, 149 + 75*channel, 
                                              150 + (self.magnitude[channel] / 128)*300, 
                                              150, arcade.color.BRIGHT_GREEN)


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        if (self.isInitialize):
            
            
            self.total_time -= delta_time
            if (self.isRecord and self.total_time < 0):
                self.isInitialize = False
                self.total_time = 0
                self.isRecord = False
                self.trial_num_dict[self.gesture_list[self.current_idx]] +=1
                self.trial_num = self.trial_num_dict[self.gesture_list[self.current_idx]]
                
            if (~self.isRecord and self.total_time < 0):
                self.total_time = 5.2
                self.isRecord = True
                    
                
            # Calculate minutes
            minutes = int(self.total_time) // 60
    
            # Calculate seconds by using a modulus (remainder)
            seconds = int(self.total_time) % 60
    
            # Calculate 100s of a second
            seconds_100s = int((self.total_time - seconds) * 100)
                        
            self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"
            
        # Change the value in MyoRaw
        self.mm.mr.label = self.label
        self.mm.mr.mask = self.isRecord
        self.mm.mr.trial_num = self.trial_num
        self.mm.mr.Side = self.side
        
        # Read the magnitude from MyoRaw
        self.magnitude = self.mm.mr.magnitude

        
    def on_key_release(self, key, modifiers):
        
        ## Change gestures    
        if (key == arcade.key.RIGHT):
            if (self.current_idx < 4):
                self.current_idx+=1
                self.trial_num = self.trial_num_dict[self.gesture_list[self.current_idx]]
                self.label = self.gesture_list[self.current_idx]
                
            else:
                self.trial_num = 0
                self.label = "End"
                
        if (key == arcade.key.LEFT):
            if (self.current_idx > 0):
                self.current_idx-=1
                self.trial_num = self.trial_num_dict[self.gesture_list[self.current_idx]]
                self.label = self.gesture_list[self.current_idx]
                
            else:
                self.label = "Rest"
                    
        ## Start recording
        if (key == arcade.key.SPACE):
            self.isInitialize = True
            self.total_time = 3.2
            self.isRecord = False        
            
        ## Connects
        if (key == arcade.key.UP):
            self.mm.connect()
            self.mm.no_sleep()
            self.mm.start_collect()    
            
        ## Disconnects
        if (key == arcade.key.ESCAPE):
            self.mm.disconnect()
            arcade.close_window()
            

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()