#!/bin/bash
#SBATCH --job-name=spython_ddp   # create a short name for your job
#SBATCH --output=job_output.txt  # write output to this file
#SBATCH --error=job_error.txt    # write error to this file
#SBATCH --time=2-00:00           # total run time limit (HH:MM:SS)
#SBATCH --get-user-env=L         # use your enviroment variables
#SBATCH --partition=long         # use partion long
#SBATCH --nodes=1                # node count
#SBATCH --mem=32G                # total memory per node (4 GB per cpu-core is default)
#SBATCH --cpus-per-task=4        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --ntasks-per-node=1      # total number of tasks per node
#SBATCH --gres=gpu:1             # number of gpus per node

export WORLD_SIZE=$(($SLURM_NNODES * $SLURM_TASKS_PER_NODE))
echo "N_NODES="$SLURM_NNODES
echo "TASKS_PER_NODE="$SLURM_TASKS_PER_NODE
echo "WORLD_SIZE="$WORLD_SIZE

master_addr=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
export MASTER_ADDR=$master_addr
export MASTER_PORT=$(expr 10000 + $(echo -n "$SLURM_JOBID" | tail -c 4))
echo "MASTER_ADDR="$MASTER_ADDR
echo "MASTER_PORT="$MASTER_PORT

source $HOME/venv/bin/activate

export NCCL_DEBUG=INFO
export NCCL_SOCKET_IFNAME="eth0,en,eth,em,bond"

export ORION_DB_ADDRESS=$HOME/scratch/orion_db.pkl
export ORION_DB_TYPE=PickledDB

python -O -u sweep.py $2
python -O -u agent.py $2
