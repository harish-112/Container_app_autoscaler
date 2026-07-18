import time

from monitor_cli import get_metrics
from scaler import AutoScaler
from azure_scale import update_replicas
from config import CHECK_INTERVAL
from replica import get_current_replicas

def main():
    autoscaler = AutoScaler()
    try:
        while True:
            metrics = get_metrics()
            metrics["replicas"] = get_current_replicas()
            print(f"Metrics: {metrics}")
            decision = autoscaler.should_scale(metrics)

            if decision:
                print(f"Scaling to {decision['target_replicas']} replicas")
                update_replicas(decision["target_replicas"])
            else:
                print("No scaling action required.")
                
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("Autoscaler stopped by user.")

if __name__ == "__main__":
        main()