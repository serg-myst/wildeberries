# API Wildberries integration
## Start project:
- create dir with your project
- git clone '-way to repo-'
- version PYTHON 3.10
- python3 -m venv venv
- pip install -r requirements.txt
- rename file .env_example to .env
- add your parameters to file .env
- create migrations with alembic as needed

## Parameters main.py
- n - insert/update reference information
- o - get new orders
- s - send new orders to email
- os - get/send new orders

## Example
- cd /home/user/your_project && /home/user/your_project/venv/bin/python3 main.py os

## Other:
-cron: https://crontab.guru/examples.html