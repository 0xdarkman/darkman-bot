from dataclasses import dataclass


@dataclass
class Logger:
    def log(self, msg):
        print(msg)
