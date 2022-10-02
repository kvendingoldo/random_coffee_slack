#!/bin/bash
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null
source vars
errors=$(docker logs bot 2>&1|grep "$(date -d '1 day ago' +%Y-%m-%d)"|grep -i 'ERROR|Exception')
curl -X POST -d "{\"text\": \"${errors}\"}" "${SLACK_WEBHOOK}"
