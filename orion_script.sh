#!/usr/bin/env bash

export ORION_DB_ADDRESS=tmp/orion_db.pkl
export ORION_DB_TYPE=PickledDB

orion hunt -n $1 python mnist.py --config sweep.json
