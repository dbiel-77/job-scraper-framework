"""
scripts/deploy.sh
-----------------
Shell script to prepare and push scrapers to a remote environment.
May be adapted for GitHub Actions or EC2 automation.
"""

#!/bin/bash
set -e

echo "Starting deployment process..."

# Activate virtual environment
source venv/bin/activate

# Pull latest code
git pull origin main

# Install or update dependencies
pip install -r requirements.txt

# Run quick smoke test
python -c "import modules, scrapers; print('Scraper framework ready.')"

echo "Deployment complete!"
