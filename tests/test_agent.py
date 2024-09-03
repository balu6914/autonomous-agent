# autonomous_agent/tests/test_agent.py

import unittest
import sys
import os

# agent.py' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import ConcreteAgent

class TestAutonomousAgent(unittest.TestCase):

    def test_message_handling(self):
        agent = ConcreteAgent("TestAgent")
        agent.receive_message("hello world")
        # Expect the message to be printed; tested this manually

    def test_integration_between_two_agents(self):
        agent1 = ConcreteAgent("Agent1")
        agent2 = ConcreteAgent("Agent2")
        agent1.receive_message("hello sun")
        agent2.receive_message("hello moon")
        # Manually inspect to see if messages are handled correctly

if __name__ == "__main__":
    unittest.main()
