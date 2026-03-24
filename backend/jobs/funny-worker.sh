#!/bin/bash

echo "Starting the Funny Message Worker..."

jokes=(
    "Why do programmers prefer dark mode? Because light attracts bugs!"
    "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
    "Why do Java developers wear glasses? Because they can't C#!"
    "A SQL query walks into a bar, walks up to two tables and asks... 'Can I JOIN you?'"
    "Why did the programmer quit his job? Because he didn't get arrays!"
)

random_joke=${jokes[$RANDOM % ${#jokes[@]}]}

echo ""
echo "============================================================"
echo "  $random_joke"
echo "============================================================"
echo ""

echo "✅ Worker completed successfully!"
echo "Idling to keep container alive..."
sleep infinity
