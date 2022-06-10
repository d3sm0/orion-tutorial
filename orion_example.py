from __future__ import print_function

import json
import os

import config
import experiment_buddy


def train(writer):
    report_file = os.path.join(config.report_path, "outcome.json")
    outcome = [dict(name="lr", type="objective", value=config.lr)]
    with open(report_file, "w") as f:
        json.dump(outcome, f)


def main():
    experiment_buddy.register_defaults(vars(config))
    writer = experiment_buddy.deploy(host="")
    train(writer)


if __name__ == '__main__':
    main()
