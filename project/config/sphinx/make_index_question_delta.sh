#!/usr/bin/env bash

ps xc|fgrep "searchd" > /dev/null
./start.sh

indexer -c ./sphinx.conf --rotate question_delta

exit 0