from enum import Enum

class TaskType(Enum):
    TASK_DECOMP = {
        "name": "0_task_decomposition",
        "in": "txt",
        "out": "yaml"
    }
    COMP_SYNTH = {
        "name": "1_component_synthesis",
        "in": "yaml",
        "out": "py"
    }
    PROC_SYNTH = "1_procedural_synthesis"
    VIS_FEEDBACK = "1_visual_feedback"
    ONE_ISSUE = "1_one_issue"
    VISUAL_CODE = "1_visual_code"
    # COMP_JUDGE = "1_component_judgement"
    SHAPE_IMPROVEMENT = "1_shape_improvement"
    SHAPE_EVALUATION = "1_shape_evaluation"
    HIGH_AGGRE = "2_high_level_aggregation"
    CODE_AGGRE = "2_code_level_aggregation"
    FUNC_EXTRA = "3_function_extraction"
    # Experiments:
    EXP_FULL_TASK = {
        "name": "exp_full_task",
        "in": "txt",
        "out": "py"
    }
