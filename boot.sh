#!/bin/bash
# code used from microblog [Miguel Grinberg]
# this script is used to boot a Docker container
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :80 --access-logfile - --error-logfile - microblog:app
