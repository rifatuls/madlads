import os
import json
import datetime

def main():
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Prepare JSON data
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "bot": "FPL Bot",
        "status": "success",
        "timestamp": now,
        "message": "Bot ran successfully and saved output."
    }

    # Save as .txt (JSON formatted)
    filename = f"output/run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[BOT] Output saved to {filename}")

if __name__ == "__main__":
    main()
