import json
import os
import re
import subprocess as sp
import sys
from typing import Dict, Any

import git
import orion.client
import yaml

import wandb


def get_step(name: str) -> int:
    return int(re.compile(r"(\d+)").findall(name)[0])


def agent(train_id, wandb_path):
    experiment = orion.client.build_experiment(train_id)
    while True:
        try:
            trial = experiment.suggest()
        except Exception as e:
            print(e)
            experiment.close()
            sys.exit(1)
        report_path = os.path.join(experiment.working_dir, experiment.name, trial.hash_params)
        args = ""
        try:
            # this a way to do checkpointing. For what i understood Orion recover the hashes of the breeded params
            # so in order to reboot from where we are, we need to query wandb for the has param, get the checkpoint
            # and pass it as an argument to main
            wandb_run = wandb.Api().runs(wandb_path, filters={"^config.params_hash": trial.hash_params},
                                         order="-created_at")[0]
            args += f"--ckpt_base_run={wandb_run}"
        except IndexError:
            pass
        os.makedirs(report_path, exist_ok=True)
        args += " ".join([f"--{k}={v}" for k, v in trial.params.items()])
        cmd = f"python main.py --report_path {report_path} {args}"
        process = sp.run(cmd, shell=True)
        print(process.returncode)
        with open(os.path.join(report_path, "outcome.json"), "r") as f:
            outcome = json.load(f)
        experiment.observe(trial, outcome)
        if experiment.is_done:
            break


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
    wandb_path = "d3sm0-orion"  # buddy can gives us one of this
    # this now replace the entry point of srun_python from main.py to agent $experiment_id
    agent(experiment_id, wandb_path)
