import threading
import time
import logging
from agent import ConcreteAgent

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def link_agents(agent1, agent2):
    def forward_messages(src, dst):
        logging.debug(f"Starting message forwarding thread from {src.name} to {dst.name}.")
        while src.running:
            try:
                # Continuously check for messages in src's outbox
                message = src.outbox.get(timeout=1)
                logging.debug(f"{src.name} retrieved message: {message}")
                # Put the message into dst's inbox
                dst.receive_message(message)
                logging.debug(f"{dst.name} received message: {message}")
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error in forwarding messages from {src.name} to {dst.name}: {e}")

    # Start forwarding threads for both agents
    threading.Thread(target=forward_messages, args=(agent1, agent2), daemon=True).start()
    threading.Thread(target=forward_messages, args=(agent2, agent1), daemon=True).start()

if __name__ == "__main__":
    logging.debug("Starting the autonomous agent program.")

    agent1 = ConcreteAgent("Agent1")
    agent2 = ConcreteAgent("Agent2")

    link_agents(agent1, agent2)

    logging.debug("Starting Agent1 and Agent2.")
    agent1.start()
    agent2.start()

    try:
        time.sleep(10)  # Let the agents run for 10 seconds
    except KeyboardInterrupt:
        logging.debug("Program interrupted by user.")
    finally:
        logging.debug("Stopping Agent1 and Agent2.")
        agent1.stop()
        agent2.stop()

    logging.debug("Autonomous agent program has completed.")
