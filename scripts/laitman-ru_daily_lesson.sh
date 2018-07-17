#!/usr/bin/env bash

set +e
set -x

BASE_DIR="/sites/archive-content-pusher"
TIMESTAMP="$(date '+%Y%m%d%H%M%S')"
LOG_FILE="$BASE_DIR/logs/laitman-ru/daily_lesson_$TIMESTAMP.log"

cd ${BASE_DIR} && source bin/activate && ./wp-autopost.py > ${LOG_FILE} 2>&1

WARNINGS="$(egrep -c "(WARNING|ERROR)" ${LOG_FILE})"

if [ "$WARNINGS" = 0 ];then
        echo "No warnings"
        exit 0
fi

echo "Errors in laitman.ru daily lesson" | mail -s "ERROR: laitman.ru daily lesson" -r "mdb@bbdomain.org" -a ${LOG_FILE} edoshor@gmail.com

find "${BASE_DIR}/logs/laitman-ru" -type f -mtime +7 -exec rm -rf {} \;
