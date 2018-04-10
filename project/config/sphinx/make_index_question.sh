#!/usr/bin/env bash

ps xc|fgrep "searchd" > /dev/null
./start.sh

indexer -c ./sphinx.conf --rotate question

exit 0