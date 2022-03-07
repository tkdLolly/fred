from random import Random

from database import pc_mode_load_q_values, pc_mode_save_q_values
from fumen import Fumen
from game import PCMode


class Agent:
    def get_next_field(self, game):
        """Return a Field as an action given GAME."""
        pass


def roll(random, p):
    r = random.random()
    return r < p


class QLearningAgent(Agent):
    def __init__(self, alpha = 1.0, epsilon=0.99, gamma=0.9, game_seed=None):
        self.alpha = alpha          # learning rate
        self.epsilon = epsilon      # exploration rate
        self.gamma = gamma          # discount
        self.game_seed = game_seed
        self.random = Random()
        self.q_values = dict()      # Key: (state, Field) tuple; Value: Q-value
        self.episodes = []

    #################
    # Value storage #
    #################

    def get_q_value(self, state, next_field):
        return self.q_values.setdefault((state, next_field), 0)

    def set_q_value(self, state, next_field, value):
        self.q_values[(state, next_field)] = value

    def load_q_values(self):
        self.q_values = pc_mode_load_q_values()

    def save_q_values(self):
        pc_mode_save_q_values(self.q_values)

    def get_next_field(self, game):
        """Choose randomly with probability of my EPSILON."""
        next_fields = game.get_possible_next_fields()
        if not next_fields:
            return None

        if roll(self.random, self.epsilon):
            return self.random.choice(list(next_fields))
        return self.compute_next_field_from_q_values(game)

    def compute_value_from_q_values(self, game):
        next_fields = game.get_possible_next_fields()
        if not next_fields:
            return 0
        return max([self.get_q_value(game.get_state_representation(), next_field) for next_field in next_fields])

    def compute_next_field_from_q_values(self, game):
        next_fields = game.get_possible_next_fields()
        if not next_fields:
            return 0
        return max([(self.get_q_value(game.get_state_representation(), field), field) for field in next_fields],
                   key=lambda pair: pair[0])[1]

    def train_auto(self, num_episodes):
        self.q_values = pc_mode_load_q_values()
        self.episodes = []

        def observe_transition(state, next_field, next_state, reward):
            next_fields = game.get_possible_next_fields()
            if next_fields:
                reward += self.gamma * max([self.get_q_value(next_state, field) for field in next_fields])
            q_value = (1 - self.alpha) * self.get_q_value(state, next_field) + self.alpha * reward
            self.set_q_value(state, next_field, q_value)

        accumulated_rewards = 0
        for _ in range(num_episodes):
            episode_rewards = 0
            game = PCMode(self.game_seed)

            while not game.has_game_ended:
                state = game.get_state_representation()
                curr_num_pcs = game.num_pcs

                next_field = self.get_next_field(game)

                game.advance_to_field(next_field)
                next_state = game.get_state_representation()

                next_num_pcs = game.num_pcs
                reward = next_num_pcs - curr_num_pcs
                observe_transition(state, next_field, next_state, reward)
                episode_rewards += reward

            accumulated_rewards += episode_rewards
            self.episodes.append(Fumen.encode(game.history))

        self.q_values = {k: v for k, v in self.q_values.items() if v != 0}
        pc_mode_save_q_values(self.q_values)

    def train_manual(self):
        pass