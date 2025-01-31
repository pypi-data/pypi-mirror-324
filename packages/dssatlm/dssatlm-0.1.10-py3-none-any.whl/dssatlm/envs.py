import os
import uuid

# ABOUT FOLDERS & FILES
TMP_DIR = r'/tmp'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_TEMPLATE_DIR = os.path.join(ROOT_DIR, 'prompt_templates')
TEXTUAL_DB_DIR = os.path.join(ROOT_DIR, 'textual_db')

SYS_PROMPT_TEMPLATE_AS_INTERPRETER_FPATH = os.path.join(PROMPT_TEMPLATE_DIR, 'system_template_as_interpreter.txt')
SYS_PROMPT_TEMPLATE_AS_PARSER_FPATH = os.path.join(PROMPT_TEMPLATE_DIR, 'system_template_as_parser.txt')
USR_PROMPT_TEMPLATE_FOR_INTERPRETER_FPATH = os.path.join(PROMPT_TEMPLATE_DIR, 'user_template_for_interpreter.txt')
USR_PROMPT_TEMPLATE_FOR_PARSER_FPATH = os.path.join(PROMPT_TEMPLATE_DIR, 'user_template_for_parser.txt')
DSSAT_LM_FULL_TEMPLATE_AS_INTERPRETER_FPATH = os.path.join(PROMPT_TEMPLATE_DIR, 'dssatlm_full_template_as_interpreter.txt')

DEFINITIONS_BANK_FPATH = os.path.join(TEXTUAL_DB_DIR, 'bank_of_definitions.txt')
QUESTIONS_BANK_FPATH = os.path.join(TEXTUAL_DB_DIR, 'bank_of_questions.txt')
SAMPLE_DEFN_N_QUESTIONS_COVERED_FPATH = os.path.join(TEXTUAL_DB_DIR, 'sample_dssat_questions.csv')

# ABOUT LLM
DEFAULT_LLM_PARAMS = {
    'temperature': 0.9,
    'max_tokens': 10000,
    'top_p': 0.9,
}


LLM_IDS_CONSIDERED = {
    'llama-3.1-70b': 'llama-3.1-70b-versatile',
    'llama-3.3-70b': 'llama-3.3-70b-versatile',
    'gpt-4o': 'gpt-4o',
}

API_KEYS_REQUIRED = ["GROQ_API_KEY", "OPENAI_API_KEY", "WANDB_API_KEY"]

DEFAULT_WANDB_PROJECT_PARAMS = {
    'project': 'dev-dssatlm-project',
    'job_type': 'dev-dssatlm-QA-pipeline',
    'name': 'run_for_user_' + str(uuid.uuid4())
}

MISSING_OR_NA_REPR = "-99"
WAITING_TIME_FOR_GROQ_FREEMIUM_API_CALL = 5
