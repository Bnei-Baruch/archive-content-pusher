#!/usr/bin/env sh

set +e
set -x

BASE_DIR="/app"
TIMESTAMP="$(date '+%Y%m%d%H%M%S')"
LOG_FILE="/tmp/laitman-ru/daily_lesson_$TIMESTAMP.log"

cleanup() {
  find "/tmp/laitman-ru" -type f -mtime +7 -exec rm -rf {} \;
}

cd ${BASE_DIR} && python wp-autopost.py > ${LOG_FILE} 2>&1

WARNINGS="$(grep -Ec "(warning|error)" ${LOG_FILE})"

if [ "$WARNINGS" = 0 ];then
  echo "No warnings"
  cleanup
  exit 0
fi

(uuencode "${LOG_FILE}" wp-autopost.log;) | mail -s "ERROR: laitman.ru daily lesson" -r "mdb@bbdomain.org" edoshor@gmail.com
cleanup
exit 1

