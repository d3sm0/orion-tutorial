#!/usr/bin/env bash

orion hunt --config orion.yaml -n $1 python mnist.py --config sweep.yaml
