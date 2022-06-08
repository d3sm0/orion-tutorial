from __future__ import print_function

import argparse
import json

from orion.client import report_objective

# Training settings
parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
# This is just a placeholder  the actual config comes from *.conf file produced by orion
parser.add_argument('--config', action='config', default=False)
parser.add_argument('--lr', action='lr', default=1.0)


def main():
    import experiment_buddy
    args, remaining = parser.parse_known_args()
    # if not remaning we are running a local script to deploy on the cluster
    # if there are remaining arguments it is because we called `orion hunt -d main.py --config config.json
    # see buddy_scripts/slurm/run_sweep.sh
    if not remaining:
        orion_params = remaining[0]
        with open(orion_params, 'r') as f:
            orion_params = json.load(f)
        print(args.lr)
        # if there are remainngs we update the config, int his case coming from parse args
        args.__dict__.update(orion_params)
    print(args.lr)  # this should be the default lr if run locally but the one provided by Orion if run on the cluster
    # update the param to wandb
    experiment_buddy.register_defaults(dict(args.__dict__))
    # buddy knows its host. If its running on the cluster, returns a simple WandbWrapper
    experiment_buddy.deploy(host="mila", sweep_definition="sweep.json")
    print(f"args: {args.lr}")
    # end of the experiment
    report_objective(0.1)


if __name__ == '__main__':
    main()
