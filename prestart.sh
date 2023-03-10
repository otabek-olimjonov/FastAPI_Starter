#! /usr/bin/env sh

echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"

echo "
#! /usr/bin/env bash

# Let the DB start
# initial migiration
alembic revision --autogenerate -m 'initial'

# Run migrations
alembic upgrade head
"


# alembic revision --autogenerate -m "initial"

alembic upgrade head