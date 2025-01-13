import agents
from constants import TaskType

import time


def run_task(task_type: TaskType, exp_id=None):
    '''
    Run a specific task in our pipeline. 

    Parameters:
        task_type (TaskType): The type of task to run.
        exp_id (int): The experiment id to name the result folder. None -> generate a new id based on the current date and time
    '''
    exp_id = exp_id or time.strftime(f"%m%d_%H%M%S-{task_type.value}")
    agent_func = agents.agents[task_type]
    task_input = ...  # TODO: sample input for the task
    result = agent_func()


# def run_exp(task_type: TaskType=None, exp_id=None):
#     '''
#     Run experiment for our pipeline. 

#     Parameters:
#         task_type (TaskType): The type of task to run. None -> run the whole pipeline.
#         exp_id (int): The experiment id to name the result folder. None -> generate a new id based on the current date and time
#     '''
#     exp_id = exp_id or time.strftime("exp_%m%d-%H%M%S")
#     if task_type:
#         run_task(task_type, exp_id)
    

