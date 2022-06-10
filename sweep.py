import json
import os
from typing import Dict, Any

import git
import orion.client
import sys
import yaml


def agent(train_id):
    experiment = orion.client.build_experiment(train_id)
    while not experiment.is_done:
        try:
            trial = experiment.suggest()
        except Exception as e:
            print(e)
            experiment.close()
            sys.exit(1)
        # TODO: can you replace this  with a subprocess?
        import orion_example
        import config
        config.__dict__.update(trial.params)
        config.hash_params = trial.hash_params
        config.train_id = experiment.name
        report_path = os.path.join(experiment.working_dir, experiment.name, trial.hash_params)
        config.report_path = report_path
        os.makedirs(report_path, exist_ok=True)
        orion_example.main()
        with open(os.path.join(report_path, "outcome.json"), "r") as f:
            outcome = json.load(f)
        experiment.observe(trial, outcome)


def sweep(space: Dict[str, Any], debug=True):
    # TODO: load yaml sweep file
    orion_config = "orion.yaml"  # this should be a constant
    experiment_name = git.Repo(search_parent_directories=True).head.object.hexsha
    with open(orion_config, "r") as f:
        orion_config = yaml.safe_load(f)
    # pymongo.MongoClient(orion_config["storage"]["url"]).admin.command("ping")
    # TODO: assert mongo
    experiment = orion.client.build_experiment(experiment_name,
                                               space=space,
                                               debug=debug,
                                               **orion_config
                                               )
    # TODO: verify experiment exist on mongo
    return experiment.name


if __name__ == '__main__':
    # This should be done locally in experiment_buddy._load_sweep
    with open("sweep.yaml", "r") as f:
        sweep_config = yaml.safe_load(f)
    experiment_id = sweep(sweep_config)
    # this now replace the entry point of srun_python from main.py to agent $experiment_id
    agent(experiment_id)
