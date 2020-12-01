#!/bin/bash

set -o allexport
source env.TAG
source test/env.docker
set +o allexport

docker-compose --env-file ./test/env.docker -f docker-compose.yml -f test/docker-compose.yml up --build -V --exit-code-from pdspi-guidance-demo-doac-test
