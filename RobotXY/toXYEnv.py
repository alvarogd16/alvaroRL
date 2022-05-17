import gym
from gym import Env, spaces
import random

from numpy import float16

# Tenemos un robot en un espacio bidimensional
# Este espacio es de 1*1 (float)
# Dado un punto (x,y) -> donde x,y son float entre 0 y 1
# El rango de acciones son:
#   eje-x: nada, izquierda, derecha
#   eje-y: nada, arriba, abajo

class Robot():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

        self.movement = 0.01

    def move(self, action):
        # First move x. With -1 nomalice the value into (-1, 0 or 1)
        x = self.x + (action[0]-1) * self.movement

        if x > 1:
            self.x = 1
        elif x < 0:
            self.x = 0
        else:
            self.x = x

        # Second move y
        y = self.y + (action[1]-1) * self.movement

        if y > 1:
            self.y = 1
        elif y < 0:
            self.y = 0
        else:
            self.y = y

    def getPosition(self):
        return (self.x, self.y)

    def reset(self):
        self.x = 0.0
        self.y = 0.0

class ToXYEnv(Env):
    def __init__(self):
        super(ToXYEnv, self).__init__()

        #    0.0    ...      1.0
        # 0.0 ┌───────────────┐
        #     │               │
        #     │               │
        #     │   ◉ <- (x,y)  │
        #     │               │
        # 1.0 └───────────────┘
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=float16)


        # ejeX -> Discrete [0] - LEFT[0], NOOP[1], RIGHT[2]
        # ejeY -> Discrete [1] - DOWN[0], NOOP[1], UP[2]
        self.action_space = spaces.MultiDiscrete([3, 3])

        self.target = (random.random(), random.random())

        self.robot = Robot()

    def checkObservation(self, obs):
        # If distance between two points its clone enough return true
        error = 0.01
        return abs(obs[0] - self.target[0]) <= error and abs(obs[1] - self.target[1]) <= error

    def getReward(self, obs):
        # Cuanto más cerca más reward
        multiplier = 32
        return multiplier / (pow(obs[0] - self.target[0], 2) + pow(obs[1] - self.target[1], 2))

    def reset(self):
        # Reset the robot
        self.robot.reset()

        # Reset the target
        self.target = (random.random(), random.random())

    def step(self, action):
        # Primero comprobamos que la acción es correcta
        assert self.action_space.contains(action), "Invalid action"

        self.robot.move(action)

        # Get the observation
        obs = self.robot.getPosition()

        # If robot is close enough to the target mark as done
        done = False
        if(self.checkObservation(obs)):
            done = True

        reward = self.getReward(obs)

        return obs, reward, done, []


env = ToXYEnv()
obs = env.reset()

step = 0
while True:
    # Now use random actions
    action = env.action_space.sample()
    print("Action {}".format(action))

    obs, reward, done, info = env.step(action)
    print("Observation {} Reward {}".format(obs, reward))

    if done == True:
        break

    step += 1

print(step, env.target)
env.close()