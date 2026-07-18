from datetime import datetime
from config import *

class AutoScaler:

    def __init__(self):
        self.last_scaled_time = None
        self.high_cpu_count = 0
        self.low_cpu_count = 0

    def in_cooldown(self):
        if self.last_scaled_time is None:
            return False

        elapsed = (datetime.now() - self.last_scaled_time).total_seconds()
        return elapsed < COOLDOWN

    def should_scale(self, metrics):
        cpu = metrics["cpu"]
        replicas = int(metrics["replicas"])

        if self.in_cooldown():
            print("Cooldown active.")
            return None

        if cpu > TARGET_CPU:
            self.high_cpu_count += 1
            self.low_cpu_count = 0

            if (self.high_cpu_count >= SCALE_CONFIRMATION_COUNT
                and replicas < MAX_REPLICAS):

                self.high_cpu_count = 0
                self.last_scaled_time = datetime.now()

                return {
                    "action": "scale_out",
                    "target_replicas": replicas + 1
                }
    
        else:

            optimal_replicas = replicas
            for candidate in range(MIN_REPLICAS, replicas):
                expected_cpu = cpu * replicas / candidate
                if expected_cpu <= TARGET_CPU:
                    optimal_replicas = candidate
                    break

            if optimal_replicas < replicas:
                self.low_cpu_count += 1
                self.high_cpu_count = 0

                if self.low_cpu_count >= SCALE_CONFIRMATION_COUNT:
                    self.low_cpu_count = 0
                    self.last_scaled_time = datetime.now()

                    return {
                        "action": "scale_in",
                        "target_replicas": optimal_replicas
                    }

            else:
                self.low_cpu_count = 0
                self.high_cpu_count = 0

        return None