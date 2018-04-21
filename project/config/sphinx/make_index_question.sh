#!/usr/bin/env bash

# каталог в котором лежит скрипт
DIRECTORY=$(cd $(dirname $0) && pwd)

ps xc|fgrep "searchd" > /dev/null
$DIRECTORY/start.sh

indexer -c $DIRECTORY/sphinx.conf --rotate question

exit 0