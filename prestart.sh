#! /usr/bin/env bash

# Let the DB start
pip install alembic

sleep 3;
# Run migrations
alembic upgrade head