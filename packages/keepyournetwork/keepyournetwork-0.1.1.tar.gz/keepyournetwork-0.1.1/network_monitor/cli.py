from .monitor import NetworkMonitor

def main():
    try:
        monitor = NetworkMonitor()
        monitor.monitor()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main() 