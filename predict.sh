#!/bin/bash

# Description: This Bash script runs two Python predict scripts sequentially.
# It ensures proper error handling and logs the results for easier debugging.

# Exit immediately if any command exits with a non-zero status (error)
set -e

# Activate a virtual environment (if required)
# Uncomment the next line if you're using a virtual environment
# source venv/bin/activate

# Run the first predicting script
echo "Starting the first predicting script: predict.py"
python predict.py

# Check if the first script executed successfully
if [ $? -eq 0 ]; then
    echo "predict.py completed successfully!"
else
    echo "Error running predict.py"
    exit 1
fi

# Run the second predicting script
echo "Starting the second predicting script: predict2.py"
python predict2.py

# Check if the second script executed successfully
if [ $? -eq 0 ]; then
    echo "predict2.py completed successfully!"
else
    echo "Error running predict2.py"
    exit 1
fi

# Optional: Deactivate virtual environment (if used)
# deactivate

# Completion message
echo "Both predicting scripts have completed successfully!"