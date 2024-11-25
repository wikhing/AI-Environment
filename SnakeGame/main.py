import numpy as np
import torch.nn as nn
import torch
import random
import torch.nn.functional as F
from env import Env
import time




device = 'cuda' if torch.cuda.is_available() else 'cpu'                                               
    


class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(17, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 5)

       
    def forward(self, x):
        
        out = F.tanh(self.fc1(x))
        out = F.tanh(self.fc2(out))
        out = F.softmax(self.fc3(out), dim=-1)
      
        return out
    
    def p(self, obs):
        out = self.forward(obs)
        dist = torch.distributions.Categorical(out)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action, log_prob, dist.entropy()
    

class ValueNet(nn.Module):
    def __init__(self):
        super().__init__()                   

        self.fc1 = nn.Linear(17, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)
 

    def forward(self, x):

        out = F.relu(self.fc1(x))
        out = F.relu(self.fc2(out))
        out = self.fc3(out)
        return out

    def v(self, x):
        out = self.forward(x)
        return out


    
class Memory:
    def __init__(self):
        self.obs_traj = []
        self.act_traj = []
        self.act_prob_traj = []
        self.rew_traj = []
        self.new_obs_traj = []
        self.done_traj = []   
        self.values_traj = []

        self.adv_traj = []


    def shuffle_mem(self):
        combined = list(zip(self.obs_traj, self.act_traj, self.act_prob_traj, self.rew_traj, self.new_obs_traj, self.done_traj, self.values_traj, self.adv_traj))
        random.shuffle(combined)
        obs_traj, act_traj, act_prob_traj, rew_traj, new_obs_traj, done_traj, values_traj, adv_traj = zip(*combined)

        self.obs_traj = list(obs_traj)
        self.act_traj = list(act_traj)
        self.act_prob_traj = list(act_prob_traj)
        self.rew_traj = list(rew_traj)
        self.new_obs_traj = list(new_obs_traj)
        self.done_traj = list(done_traj)    
        self.values_traj = list(values_traj)
        self.adv_traj = list(adv_traj)

    def store_mem(self, obs, act, act_prob, rew, new_obs, done, value):
        self.obs_traj.append(obs)
        self.act_traj.append(act)
        self.act_prob_traj.append(act_prob)
        self.rew_traj.append(rew)
        self.new_obs_traj.append(new_obs)
        self.done_traj.append(done)
        self.values_traj.append(value)

    def clear_mem(self):
        self.obs_traj.clear()
        self.act_traj.clear()
        self.act_prob_traj.clear()
        self.rew_traj.clear()
        self.new_obs_traj.clear()
        self.done_traj.clear()
        self.values_traj.clear()
        self.adv_traj.clear()

    def get_mem(self):
        return torch.stack(self.obs_traj).to(device),  \
                torch.tensor(self.act_traj, dtype=torch.float32).to(device), \
                torch.tensor(self.act_prob_traj, dtype=torch.float32).to(device),  \
                torch.tensor(self.adv_traj, dtype=torch.float32).to(device)





class PPO:
    def __init__(self, gamma=0.99, gae_lambda=0.95, epsilon=0.2, epoch=10, learning_rate=3e-4, batch_size=64, ent_coef=0.00):
        self.policy_net = PolicyNet()
        self.value_net = ValueNet()
        self.memory = Memory()

        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.epsilon = epsilon

        self.epoch = epoch
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.ent_coef = ent_coef

        self.policy_optim = torch.optim.Adam(self.policy_net.parameters(), lr=self.learning_rate)
        self.value_optim = torch.optim.Adam(self.value_net.parameters(), lr=self.learning_rate)
        self.loss_fn = nn.MSELoss()
       
        


    def pred(self, obs):
        action, log_prob, entropy = self.policy_net.p(obs)
        value = self.value_net.v(obs)
        return action, log_prob, value, entropy
    
    def eval_action(self, obs, actions):
        out = self.policy_net.forward(obs)
        dist = torch.distributions.Categorical(out)
        log_prob = dist.log_prob(actions)
        value = self.value_net.v(obs)
        return log_prob, value, dist.entropy()
    
    def calc_advantage(self):
        for i in range(len(self.memory.rew_traj)):
            advantage = 0
            for j in range(i, len(self.memory.rew_traj)):

                delta = self.memory.rew_traj[j] - self.memory.values_traj[j]

                if self.memory.done_traj[j] != 1:
                    delta += self.gamma * self.memory.values_traj[j + 1]
                
                advantage += delta * ((self.gamma * self.gae_lambda) ** (j - i))

                if self.memory.done_traj[j] == 1:
                    break

            self.memory.adv_traj.append(advantage)



    def train(self):
        
        self.policy_net.to(device)
        self.value_net.to(device)

        self.calc_advantage()
        self.memory.shuffle_mem()

        obs, actions, old_log_prob, advantage = self.memory.get_mem()
        
        ret = advantage + torch.tensor(self.memory.values_traj).to(device)
        
                                                                           
        for epoch in range(self.epoch):

            for i in range(int(len(actions) / self.batch_size)):

                chckpoint_from = i * self.batch_size
                chckpoint_to = chckpoint_from + self.batch_size

                adv = advantage[chckpoint_from:chckpoint_to]
                adv = (adv - adv.mean()) / (adv.std() + 1e-8)

                log_prob, value, entropy = self.eval_action(obs[chckpoint_from:chckpoint_to], actions[chckpoint_from:chckpoint_to])
                ratio = torch.exp((log_prob - old_log_prob[chckpoint_from:chckpoint_to]))
                policy_loss_1 = ratio * adv
                policy_loss_2 = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * adv
                policy_loss = -torch.min(policy_loss_1, policy_loss_2).mean()
                self.policy_optim.zero_grad()
                policy_loss.backward()
                self.policy_optim.step()
                                                                                               
                value_loss = self.loss_fn(value.flatten(), ret[chckpoint_from:chckpoint_to]) * 0.5
                self.value_optim.zero_grad()
                value_loss.backward()
                self.value_optim.step()



        self.memory.clear_mem()
        self.policy_net.to('cpu')
        self.value_net.to('cpu')
    
    
    def learn(self):
        env = Env()
        
        try :
            print('loading agent...')
            self.policy_net.load_state_dict (torch.load("policy.pth"))
            self.value_net.load_state_dict(torch.load("value.pth"))
        except Exception as e:
            print("no model found") 


        ep = 0  
        avg_rew = 0 
        total_tp = 0 
        num_of_updates = 0

        print('training starting in...')
        for i in range(5):
            print(5 - i)
            time.sleep(1)

        while True:                                          
            ep += 1
            total_rew = 0
            obs = env.reset() # obs in numpy

            while True:
                action, log_prob, value, _ = self.pred(torch.from_numpy(obs))
                new_obs, rew, done = env.step(action.item())
                # have to store either in pytorch tensor, or python data type format, no numpy
                # the obs and new_obs is in tensor, example : torch.tensor([1, 2 ,3]), stored in a python array
                # the tensors are then stacked up together
                self.memory.store_mem(torch.from_numpy(obs), action.item(), log_prob, rew, torch.from_numpy(new_obs), done, value.item())
                obs = new_obs
                total_rew += rew

                if (done):
                    avg_rew += total_rew
                    break 
                
            if (ep % 10) == 0:
                total_tp += len(self.memory.rew_traj)
                print(f"---------------------------------------------")
                print(f"episode : {ep} | avg reward : {avg_rew/50}")
                print(f"timesteps : {len(self.memory.rew_traj)}")
                print(f"total timesteps : {total_tp/1e6}M")
                print(f"num of updates : {num_of_updates}")
                print(f"---------------------------------------------\n")
                avg_rew = 0


            if (len(self.memory.rew_traj)) >= 2048:
                self.train()
                num_of_updates += 1

                torch.save(self.policy_net.state_dict(), "policy.pth")
                torch.save(self.value_net.state_dict(), "value.pth")


                                                                                        

                                                                                            

agent = PPO()
agent.learn()