import gym
import time

env = gym.make('MountainCar-v0')

print("Upper Bound for Env Observation", env.observation_space.high)
print("Lower Bound for Env Observation", env.observation_space.low)

num_steps = 1500

obs = env.reset()

for step in range(num_steps):
    # Now only random actions
    action = env.action_space.sample()

    obs, reward, done, info = env.step(action)

    env.render()

    time.sleep(0.001)

    if done:
        env.reset()

env.close()