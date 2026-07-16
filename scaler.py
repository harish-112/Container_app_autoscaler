from datetime import datetime

from config import (
    CPU_SCALE_OUT,
    CPU_SCALE_IN,
    MAX_REPLICAS,
    MIN_REPLICAS,
    COOLDOWN,
    SCALE_CONFIRMATION_COUNT
)

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
        cpu = metrics["CpuPercentage"]
        replicas = int(metrics["Replicas"])

        if self.in_cooldown():
            return None

        if cpu > CPU_SCALE_OUT:
            self.high_cpu_count += 1
            self.low_cpu_count = 0

        elif cpu < CPU_SCALE_IN:
            self.low_cpu_count += 1
            self.high_cpu_count = 0

        else:
            self.high_cpu_count = 0
            self.low_cpu_count = 0
            return None

        if (self.high_cpu_count >= SCALE_CONFIRMATION_COUNT
            and replicas < MAX_REPLICAS):

            self.high_cpu_count = 0
            self.last_scaled_time = datetime.now()

            return {
                "action": "scale_out",
                "target_replicas": replicas + 1
            }

        if (self.low_cpu_count >= SCALE_CONFIRMATION_COUNT
            and replicas > MIN_REPLICAS):
            
            self.low_cpu_count = 0
            self.last_scaled_time = datetime.now()

            return {
                "action": "scale_in",
                "target_replicas": replicas - 1
            }

        return None