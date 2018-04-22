#!/usr/bin/env bash

# каталог в котором лежит скрипт
DIRECTORY=$(cd $(dirname $0) && pwd)

searchd -c $DIRECTORY/sphinx.conf