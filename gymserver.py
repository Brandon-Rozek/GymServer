import sys
import gym
from flask import Flask
from flask import request
import pickle
import json


##
# OpenAI Gym State
##
# environment_name = sys.argv[1]
# environment_name = "Acrobot-v1"
environment_name = "Pong-v0"
env = gym.make(environment_name)

# Observations to release to agent
state = env.reset()
reward = 0
score = 0
done = False
info = {}

##
# Helper Functions
##
# [TODO] Evaluate whether pickling is the right option here
def pickle_state():
    global state
    return pickle.dumps(state)



##
# Flask Environment
##
app = Flask(__name__)

@app.route('/environment', methods=['GET'])
def get_env():
    global env, environment_name
    if request.args.get('shape') is not None:
        shape = {}
        shape['observation'] = env.observation_space.shape
        shape['action'] = env.action_space.n
        return json.dumps(shape)
    return environment_name

@app.route('/state', methods=['GET'])
def get_state():
    return pickle_state()

@app.route('/reward', methods=['GET'])
def get_reward():
    global score, reward
    if request.args.get('all') is not None:
        return str(score)
    else:
        return str(reward)

@app.route('/done', methods=['GET'])
def is_done():
    global done
    return str(done)

@app.route('/info', methods=['GET'])
def get_info():
    global info
    return json.dumps(info)

@app.route('/action', methods=['POST'])
def perform_action():
    global state, reward, done, info, score
    action = int(request.form['id'])

    # [TODO] Check to see if 'action' is valid
    state, reward, done, info = env.step(action)
    score += reward

    content = {}
    content['reward'] = reward
    content['done'] = done
    content['info'] = info
    return json.dumps(content)

@app.route('/reset')
def reset_env():
    global env, state, reward, done, info, score
    state = env.reset()
    reward = 0
    done = False
    info = {}
    score = 0
    return pickle_state()

