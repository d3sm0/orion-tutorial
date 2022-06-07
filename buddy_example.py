import experiment_buddy

# we now use wandb sweep. as such the slurm would call
# wandb agent config.yaml with the config as:
"""
lr:
    values: [0.1, 0.2, 0.1, 0.25, 0.35]
"""


# but it can be anything else.
# wandb agent calls the python as python main.py --lr=0.03

def main():
    experiment_buddy.register({
        "lr": 0.01
    })
    experiment_buddy.deploy(host="mila")


if __name__ == '__main__':
    main()
