import unittest

from agent import QLearningAgent


class QLearningAgentTest(unittest.TestCase):
    def test_init(self):
        agent = QLearningAgent()

    def test_train_once(self):
        agent = QLearningAgent()
        agent.train_auto(1)
        print(agent.q_values)

    def test_train_ten(self):
        agent = QLearningAgent()
        agent.train_auto(10)
        print(agent.episodes)

    def test_train_hundred(self):
        agent = QLearningAgent()
        agent.train_auto(100)
        #print(agent.q_values)

    def test_train_twelve_thousand(self):
        agent = QLearningAgent()
        agent.train_auto(12000)