import argparse


if __name__ == '__main__':

    # ----------
    # Argument Parser
    # ----------

    parser = argparse.ArgumentParser("Periodic Task Service")
    group = parser.add_mutually_exclusive_group()

    # Run Mode
    group.add_argument("--worker", action = "store_true", help = "Run periodic worker")
    group.add_argument("--beat", action = "store_true", help = "Run Celery Beat scheduler")

    options = parser.parse_args()

    if options.beat:
        from src.run_beat import main as start_beat_main
        print("Starting Celery Beat scheduler...")
        start_beat_main()
    else:
        from src.run_periodic_worker import main as start_worker_main
        print("Starting Periodic Tasks Worker...")
        start_worker_main()
        