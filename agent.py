
import random
import os
import pickle

class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.actions = actions
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def get_state_key(self, state):
        return str(state)  

    def choose_action(self, state):
        state_key = self.get_state_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0 for action in self.actions}

        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        else:
            return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def learn(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0 for action in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0 for action in self.actions}

        best_next_action = max(self.q_table[next_state_key], key=self.q_table[next_state_key].get)
        self.q_table[state_key][action] = (1 - self.learning_rate) * self.q_table[state_key][action] + \
                                          self.learning_rate * (reward + self.discount_factor * self.q_table[next_state_key][best_next_action])

    def decay_exploration(self):
        self.exploration_rate *= self.exploration_decay

    def save_q_table(self, filename='q_table.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename='q_table.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)

    def speed_up_learning(self, factor=2):
        """Ускоряет обучение, изменяя параметры."""
        self.learning_rate *= factor
        self.exploration_decay **= factor
