# SocialDice
[![Build Status](https://travis-ci.org/SWE-AGGERS/SocialDice.svg?branch=reactions)](https://travis-ci.org/SWE-AGGERS/SocialDice)
### Get Started
* python3 -m venv venv
* . ./venv/bin/activate
* pip3 install -r requirements.txt
* sh ./start_redis.sh
* python3 -m celery worker -A monolith.background.celery -E --loglevel=info

