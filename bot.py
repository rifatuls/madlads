import datetime

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[BOT] Running at {now}")

if __name__ == "__main__":
    main()
