#!/bin/bash

# Description: This Bash script runs two Python training scripts sequentially.
# It ensures proper error handling and logs the results for easier debugging.

# Exit immediately if any command exits with a non-zero status (error)
set -e

# Activate a virtual environment (if required)
# Uncomment the next line if you're using a virtual environment
# source venv/bin/activate

# Run the first training script
echo "Starting the first training script: train.py"
python train.py

# Check if the first script executed successfully
if [ $? -eq 0 ]; then
    echo "train.py completed successfully!"
else
    echo "Error running train.py"
    exit 1
fi

# Run the second training script
echo "Starting the second training script: train2.py"
python train2.py

# Check if the second script executed successfully
if [ $? -eq 0 ]; then
    echo "train2.py completed successfully!"
else
    echo "Error running train2.py"
    exit 1
fi

# Optional: Deactivate virtual environment (if used)
# deactivate

# Completion message
echo "Both training scripts have completed successfully!"