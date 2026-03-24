#!/usr/bin/env python3

import time
import random

def main():
    print("🐄 Starting the Funny Message Worker...")
    
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        "Why do Java developers wear glasses? Because they can't C#!",
        "A SQL query walks into a bar, walks up to two tables and asks... 'Can I JOIN you?'",
        "Why did the programmer quit his job? Because he didn't get arrays!"
    ]
    
    selected_joke = random.choice(jokes)
    
    print(f"\n{'='*60}")
    print(f"  {selected_joke}")
    print(f"{'='*60}\n")
    
    print("✅ Worker completed successfully!")
    return 0

if __name__ == "__main__":
    main()
    print("Idling to keep container alive...")
    while True:
        time.sleep(86400)
