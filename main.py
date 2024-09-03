import threading
import time
from agent import ConcreteAgent

def link_agents(agent1, agent2):
    def forward_messages(src, dst):
        while src.running:
            try:
                message = src.outbox.get(timeout=1)
                dst.receive_message(message)
            except queue.Empty:
                continue

    threading.Thread(target=forward_messages, args=(agent1, agent2)).start()
    threading.Thread(target=forward_messages, args=(agent2, agent1)).start()

if __name__ == "__main__":
    agent1 = ConcreteAgent("Agent1")
    agent2 = ConcreteAgent("Agent2")

    link_agents(agent1, agent2)

    agent1.start()
    agent2.start()

    try:
        time.sleep(10)  # Let the agents run for 10 seconds
    finally:
        agent1.stop()
        agent2.stop()