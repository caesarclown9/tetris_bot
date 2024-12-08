
import time
import pyautogui
import subprocess
import os
import numpy as np
import cv2

from game_state import get_game_state
from agent import QLearningAgent
from reward import get_reward, is_game_over

def open_game():
    """Запускает игру Tetris."""
    venv_python = os.path.join('env', 'Scripts', 'python.exe')
    try:
        subprocess.Popen([venv_python, 'tetris.py'])
    except FileNotFoundError:
        print("Не удалось найти tetris.py или python.exe в виртуальном окружении.")
        return

def close_game():
    """Закрывает игру Tetris."""

    try:
        pyautogui.hotkey("alt", "f4")
        time.sleep(1)
    except Exception as e:
        print(f"Ошибка при закрытии игры: {e}")

def game_loop(agent):
    try:
        state = get_game_state("game_template.png")
    except ValueError as e:
        print(e)
        return

    while True:
        action = agent.choose_action(state)
        print(f"Chosen action: {action}")  

        pyautogui.press(action)
        time.sleep(0.1)  

        try:
            new_state = get_game_state("game_template.png")
        except ValueError as e:
            print(e)
            return

        state_difference = np.sum(state != new_state)
        print(f"State difference: {state_difference}")  


        reward = get_reward(state, new_state)
        print(f"Reward: {reward}")  

        if is_game_over(state, new_state):
            print("Game Over!")
            print(f"Last state saved as 'last_state.png'")

            cv2.imwrite("last_state.png", new_state)
            agent.save_q_table()
            break

        agent.learn(state, action, reward, new_state)
        agent.decay_exploration()
        state = new_state

if __name__ == "__main__":
    actions = ['left', 'right', 'down', 'up']
    agent = QLearningAgent(actions)


    agent.load_q_table()


    agent.speed_up_learning(factor=3)

    open_game()
    time.sleep(2)  

    while True:
        game_loop(agent)
        close_game()
        open_game()
        time.sleep(2)  
