import threading
import queue
import time
import random
import logging

class AutonomousAgent:
    def __init__(self, name):
        self.name = name
        self.inbox = queue.Queue()
        self.outbox = queue.Queue()
        self.handlers = {}
        self.behaviors = []
        self.running = False

    def start(self):
        self.running = True
        logging.debug(f"{self.name}: Starting threads.")
        threading.Thread(target=self._consume_messages, daemon=True).start()
        threading.Thread(target=self._run_behaviors, daemon=True).start()

    def stop(self):
        logging.debug(f"{self.name}: Stopping threads.")
        self.running = False

    def _consume_messages(self):
        logging.debug(f"{self.name}: Starting message consumption.")
        while self.running:
            try:
                message = self.inbox.get(timeout=1)
                logging.debug(f"{self.name}: Received message: {message}")
                self._handle_message(message)
            except queue.Empty:
                logging.debug(f"{self.name}: Inbox is empty.")
                continue
            except Exception as e:
                logging.error(f"{self.name}: Error in message consumption: {e}")

    def _handle_message(self, message):
        logging.debug(f"{self.name}: Handling message: {message}")
        for keyword, handler in self.handlers.items():
            if keyword in message:
                logging.debug(f"{self.name}: Triggering handler for keyword: {keyword}")
                handler(message)

    def _run_behaviors(self):
        logging.debug(f"{self.name}: Starting behaviors.")
        while self.running:
            for behavior in self.behaviors:
                logging.debug(f"{self.name}: Executing behavior.")
                try:
                    behavior()
                    time.sleep(0.1)  # Add a small delay after each behavior execution
                except Exception as e:
                    logging.error(f"{self.name}: Error in behavior execution: {e}")
            time.sleep(1)  # Wait a second before checking behaviors again

    def register_handler(self, keyword, handler):
        logging.debug(f"{self.name}: Registering handler for keyword: {keyword}")
        self.handlers[keyword] = handler

    def register_behavior(self, behavior):
        logging.debug(f"{self.name}: Registering a new behavior.")
        self.behaviors.append(behavior)

    def send_message(self, message):
        logging.debug(f"{self.name}: Sending message: {message}")
        self.outbox.put(message)

    def receive_message(self, message):
        logging.debug(f"{self.name}: Receiving message: {message}")
        self.inbox.put(message)
        logging.debug(f"{self.name}: Message added to inbox: {message}")

class ConcreteAgent(AutonomousAgent):
    def __init__(self, name):
        super().__init__(name)
        logging.debug(f"{self.name}: Initializing ConcreteAgent.")
        self.register_handler("hello", self.print_message)
        self.register_behavior(self.generate_random_message)

    def print_message(self, message):
        logging.debug(f"{self.name}: Handling message with 'hello' keyword.")
        print(f"[{self.name}] Received: {message}")

    def generate_random_message(self):
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
        message = " ".join(random.sample(words, 2))
        logging.debug(f"{self.name}: Generated message: {message}")
        self.send_message(message)
