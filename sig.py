import signal
import threading

def signal_handler(sig, frame):
    print(f"Received signal {sig}")

def start_worker_thread():
    # This function represents the entry point for a worker thread
    # It should perform its task and then signal the main thread if necessary
    pass

if __name__ == "__main__":
    # Register signal handler in the main thread
    signal.signal(signal.SIGINT, signal_handler)

    # Start worker thread
    worker_thread = threading.Thread(target=start_worker_thread)
    worker_thread.start()

    # Main thread continues execution
    # You can perform other tasks here
