import json
import numpy as np
import keyboard
import time


class Env:
    def __init__(self):

        self.data_path = "snake_data.json"
        self.data = []

        self.prev_score = 0
        self.prev_x = 0
        self.prev_y = 0

    def update_data(self):
        while True:
            try:
                with open(self.data_path, "r") as file:
                    self.data = json.load(file)
            except Exception as e:
                continue
            break

    def get_done(self):
        self.update_data()
        return 1 - self.data['State']

    def get_obs(self):

        time.sleep(0.05)

        self.update_data()

        snake_x = 0
        snake_y = 0
        apple_x = 0
        apple_y = 0

        for y in range(25):
            for x in range(25):
                if self.data['Arrays'][y][x]['value'] == 2:
                    snake_x = x
                    snake_y = y

                if self.data['Arrays'][y][x]['value'] == 3:
                    apple_x = x
                    apple_y = y

        distance = (np.abs(apple_y - snake_y) + np.abs(apple_x - snake_x)) / 48.0

        on_right = apple_x > snake_x
        on_left = apple_x < snake_x
        on_up = apple_y < snake_y
        on_down = apple_y > snake_y

        on_right_edge = (snake_x == 24) 
        on_left_edge = (snake_x == 0)
        on_up_edge = (snake_y == 0)
        on_down_edge = (snake_y == 24)

        if on_right_edge == 0:
            on_right_edge = (self.data['Arrays'][snake_y][snake_x + 1] == 1)
        
        if on_left_edge == 0:
            on_left_edge = (self.data['Arrays'][snake_y][snake_x - 1] == 1)

        if on_up_edge == 0:
            on_up_edge = (self.data['Arrays'][snake_y - 1][snake_x] == 1)

        if on_down_edge == 0:
            on_down_edge = (self.data['Arrays'][snake_y + 1][snake_x] == 1)

        
        if self.prev_x == -1:
            self.prev_x = snake_x
        if self.prev_y == -1:
            self.prev_y = snake_y

        is_up = snake_y < self.prev_y 
        is_down = snake_y > self.prev_y
        is_right = snake_x > self.prev_x
        is_left = snake_x < self.prev_x


        obs = np.array([snake_x/24.0, snake_y/24.0, apple_x/24.0, apple_y/24.0, \
                        distance, \
                        on_up, on_down, on_left, on_right, \
                        on_up_edge, on_down_edge, on_right_edge, on_left_edge, \
                        is_up, is_down, is_left, is_right]).astype(np.float32)
        
        self.prev_x = snake_x
        self.prev_y = snake_y

        return obs


    def get_rew(self):

        self.update_data()

        rew = 0

        if self.get_done():
            rew = -10
        

        if self.data['Score'] > self.prev_score:
            rew = 10  

        self.prev_score = self.data['Score']

        return rew

    def reset(self):

        self.prev_score = 0
        self.prev_x = -1
        self.prev_y = -1

        self.update_data()

        keyboard.press_and_release('space')
        return self.get_obs()

    def step(self, action):
        
        self.update_data()

        if action == 0:
            keyboard.press_and_release('up')
        if action == 1:
            keyboard.press_and_release('down')
        if action == 2:
            keyboard.press_and_release('left')
        if action == 3:
            keyboard.press_and_release('right')
        
        obs = self.get_obs()
        rew = self.get_rew()
        done = self.get_done()

        return obs, rew, done






