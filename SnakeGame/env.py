import json
import numpy as np
import keyboard


class Env:
    def __init__(self):

        self.data_path = "snake_data.json"
        self.data = []

        self.prev_score = 0

    def update_data(self):
        while True:
            try:
                with open(self.data_path, "r") as file:
                    self.data = json.load(file)
            except Exception as e:
                continue
            break

    def get_done(self):
        return self.data['State']

    def get_obs(self):

        self.update_data()

        obs = np.zeros((25, 25), dtype=np.float32)
        for y in range(25):
            for x in range(25):
                obs[y][x] = self.data['Arrays'][y][x]['value']

        return obs


    def get_rew(self):
        rew = 0
        if self.data['Score'] > self.prev_score:
            rew = 1    
        self.prev_score = self.data['Score']
        return rew

    def reset(self):
        keyboard.press_and_release('space')
        return self.get_obs()

    def step(self, action):
        pass



env = Env()
while True:
    obs = env.get_obs()
    rew = env.get_rew()

    print(env.get_done())
  