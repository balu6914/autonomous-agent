import threading
import queue
import time
import random

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
        threading.Thread(target=self._consume_messages, daemon=True).start()
        threading.Thread(target=self._run_behaviors, daemon=True).start()

    def stop(self):
        self.running = False

    def _consume_messages(self):
        while self.running:
            try:
                message = self.inbox.get(timeout=1)
                self._handle_message(message)
            except queue.Empty:
                continue

    def _handle_message(self, message):
        for keyword, handler in self.handlers.items():
            if keyword in message:
                handler(message)

    def _run_behaviors(self):
        while self.running:
            for behavior in self.behaviors:
                behavior()
            time.sleep(1)  # Wait a second before checking behaviors again

    def register_handler(self, keyword, handler):
        self.handlers[keyword] = handler

    def register_behavior(self, behavior):
        self.behaviors.append(behavior)

    def send_message(self, message):
        self.outbox.put(message)

    def receive_message(self, message):
        self.inbox.put(message)


class ConcreteAgent(AutonomousAgent):
    def __init__(self, name):
        super().__init__(name)
        self.register_handler("hello", self.print_message)
        self.register_behavior(self.generate_random_message)

    def print_message(self, message):
        print(f"[{self.name}] Received: {message}")

    def generate_random_message(self):
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
        message = " ".join(random.sample(words, 2))
        self.send_message(message)