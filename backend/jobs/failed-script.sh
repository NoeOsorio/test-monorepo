#!/bin/bash

echo "Starting important process..."
echo "Checking prerequisites..."

if [ -f "/this/file/does/not/exist.txt" ]; then
    echo "All good!"
else
    echo "ERROR: Required configuration file not found!"
    exit 1
fi

echo "This line will never be reached"
