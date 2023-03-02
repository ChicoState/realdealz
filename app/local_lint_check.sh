#! /bin/ash
cd /app
pylint --errors-only $(find . -type f -name "*.py")