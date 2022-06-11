import os
from typing import Dict, Any

import git
import orion.client
import yaml


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
                                               storage={
                                                   "type": os.environ["ORION_DB_TYPE"],
                                                   "host": os.environ["ORION_DB_ADDRESS"]
                                               },
                                               algorithms=orion_config["algorithms"]
                                               )
    # TODO: verify experiment exist on mongo
    return experiment.name


if __name__ == '__main__':
    # This should be done locally in experiment_buddy._load_sweep
    with open("sweep.yaml", "r") as f:
        sweep_config = yaml.safe_load(f)
    experiment_id = sweep(sweep_config)
