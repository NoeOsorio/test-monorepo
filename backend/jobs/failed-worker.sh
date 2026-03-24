#!/bin/bash

echo "Starting Database Migration Worker..."
echo "Checking database connection..."

required_env="CRITICAL_DATABASE_URL"

if [ -z "${!required_env}" ]; then
    echo "❌ ERROR: Missing required environment variable: $required_env"
    echo "Worker cannot proceed without database configuration."
    echo "Worker failed but will idle to keep container alive..."
    sleep infinity
fi

echo "This line will never be reached"
