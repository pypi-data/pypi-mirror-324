import time
import os

class Animate:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def speed(value: float) -> float:
        return value

    @classmethod
    def horizontal(cls, text: str, speed: float = 0.1):
        lines = text.split('\n')
        max_length = max(len(line) for line in lines)
        
        for i in range(max_length):
            cls.clear()
            for line in lines:
                print(line[:i+1])
            time.sleep(speed)