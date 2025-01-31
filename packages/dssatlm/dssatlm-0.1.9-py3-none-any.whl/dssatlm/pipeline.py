import os
import pandas as pd
from langchain_openai import OpenAI
from wandb.integration.openai import autolog
from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts import PipelinePromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.rate_limiters import InMemoryRateLimiter

from dssatlm.envs import (
    SYS_PROMPT_TEMPLATE_AS_PARSER_FPATH,
    USR_PROMPT_TEMPLATE_FOR_PARSER_FPATH,
    SYS_PROMPT_TEMPLATE_AS_INTERPRETER_FPATH,
    USR_PROMPT_TEMPLATE_FOR_INTERPRETER_FPATH,
    DEFINITIONS_BANK_FPATH,
    QUESTIONS_BANK_FPATH,
    SAMPLE_DEFN_N_QUESTIONS_COVERED_FPATH,
    DEFAULT_LLM_PARAMS,
    LLM_IDS_CONSIDERED,
    API_KEYS_REQUIRED,
    DEFAULT_WANDB_PROJECT_PARAMS,
    TMP_DIR,
)

import groq
import openai
import wandb
import getpass
from dssatlm.structured_responses import DssatLMInterpreterResponse, DssatLMParserResponse
from dssatlm.utils import get_current_time, get_schema_dict_from_pydanticmodel, dict_to_json_file
from dssatsim import run_dssat_exp_cli
from rich.markdown import Markdown



LANGCHAIN_RATE_LIMITER = InMemoryRateLimiter(
    requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

REQUIRED_DSSATSIM_OUTPUT_KEYS = {
    'Dates', 'Dry weight, yield and yield components','Nitrogen', 
    'Nitrogen productivity', 'Organic matter', 'Phosphorus','Potassium', 
    'Seasonal environmental data (planting to harvest)', 
    'Water', 'Water productivity'
}

UNWANTED_SUB_KEYS_FROM_SIMULATOR_OUTPUT = {
    "Leaf area index, maximum",
    "By-product removed during harvest (kg [dm]/ha)",
    "Pod/Ear/Panicle weight at maturity (kg [dm]/ha)",
    "CH4EM",
    "Average daylength (hr/d), planting to harvest",
    "Simulation start date",
    "HYEAR",
    "Crop establishment start",
    "Crop establishment end",
    "Crop establishment duration",
    "Vegetative growth start",
    "Vegetative growth end",
    "Vegetative growth duration",
    "Yield formation start",
    "Yield formation end",
    "Yield formation duration",
    "Entire period start",
    "Entire period end",
    "Entire period duration"
}


class LanguageModel:
    def __init__(
            self, 
            model_id, 
            max_tokens=DEFAULT_LLM_PARAMS['max_tokens'], 
            temperature=DEFAULT_LLM_PARAMS['temperature'], 
            top_p=DEFAULT_LLM_PARAMS['top_p'],
            inference_type='api', 
            **kwargs
        ):
        self.model_id = model_id
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.inference_type = inference_type
        self.params = kwargs
        self.model_provider = self.setup_model_provider()
        self.model = self.setup_model()

    def setup_model_provider(self):
        if self.model_id.startswith('llama'):
            return 'groq'
        elif self.model_id.startswith('gpt'):
            return 'openai'
        else:
            return None # it will be infered by langchain automatically

    def setup_model(self):
        if self.inference_type == 'api':
            return self.setup_model_as_api()
        elif self.inference_type == 'local':
            return self.setup_model_as_local()
        else:
            raise ValueError(f"Invalid inference type: {self.inference_type}. Must be either 'api' or 'local'.")

    def setup_model_as_api(self):
        from langchain.chat_models import init_chat_model
        return init_chat_model(
            model = self.model_id, 
            model_provider=self.model_provider,
            max_tokens=self.max_tokens, 
            temperature=self.temperature, top_p=self.top_p, 
            rate_limiter=LANGCHAIN_RATE_LIMITER , 
            **self.params
        )

    def setup_model_as_local(self):
        raise NotImplementedError("Local inference is not yet supported.")

    def __repr__(self):
        return f"LanguageModel(model_id={self.model_id}, max_tokens={self.max_tokens}, temperature={self.temperature}, top_p={self.top_p}, params={self.params})"


class DSSATAnyLMPipeline:
    def __init__(
            self, 
            parser_model_id, 
            interpreter_model_id, 
            parser_params=None, 
            interpreter_params=None, 
            wandb_params=DEFAULT_WANDB_PROJECT_PARAMS
        ):

        self.setup_api_keys()
        self.wandb_run = self.set_up_wandb(wandb_params)

        parser_params = parser_params or {}
        interpreter_params = interpreter_params or {}

        self.parser_model_id = parser_model_id
        self.interpreter_model_id = interpreter_model_id
        self.ensure_llm_ids_are_valid()
        self.set_llm_ids_full()
        self.parser = LanguageModel(self.parser_model_id_full, **parser_params)
        self.interpreter = LanguageModel(self.interpreter_model_id_full, **interpreter_params)
        self.simulator = None

        self.dssatlm_simulator_response = {"simulation_results": "impossible"}
        self.simulation_is_possible = False
        self.missing_value_id = "missing"
        self.default_empty_answer_for_farmer = "Sorry, your answer cannot be answered at the moment."

        self.pipeline_logs, self.execution_errors_list = self.setup_pipeline_logs()
        


    def answer_query(self, farmer_input_query):
        """
        Answer a query using the DSSAT LLM pipeline
        """
        try:
            dssatlm_parser_response = self.parse_querry_to_simulator_structure(farmer_input_query)

            dssatlm_simulator_response = self.run_dssat_simulation(dssat_input_json=dssatlm_parser_response)

            dssatlm_interpreter_response = self.interpret_simulation_results_for_farmer(
                question_statement=dssatlm_parser_response["question_statement"], 
                sim_outputs_json=dssatlm_simulator_response
            )
            
            self.create_formulaic_ground_truth_answer(
                sim_outputs_json=dssatlm_simulator_response, 
                question_statement=dssatlm_interpreter_response["matched_question_found"]
            )


        except Exception as e:
            # because this must be some unaccounted error
            if str(e) not in self.execution_errors_list:
                self.pipeline_logs["pipeline_ran_successfully"] = False
            else:
                print(f"Pipeline ran as expected but some warning : {str(e)}")
        
        self.save_logs()
        self.close_wandb()

        return self.get_logs(subkey="dssatlm_interpreter_response")
        
    
    # ================== PARSER ==================

    def generate_prompt_for_parser(self):
        with open(SYS_PROMPT_TEMPLATE_AS_PARSER_FPATH, 'r') as f:
            sys_prompt_template_as_parser = f.read()

        with open(USR_PROMPT_TEMPLATE_FOR_PARSER_FPATH, 'r') as f:
            user_prompt_template_for_parser = f.read()

        instructions_prompt_template =  ChatPromptTemplate([
            ("system", sys_prompt_template_as_parser),
            ("user", user_prompt_template_for_parser)
        ])

        return instructions_prompt_template


    def parse_querry_to_simulator_structure(self, farmer_input_query):
        
        parser_output_cmd = PydanticOutputParser(pydantic_object=DssatLMParserResponse)
        instructions_prompt_template = self.generate_prompt_for_parser()
        parser_chain = instructions_prompt_template | self.parser.model | parser_output_cmd

        # Format the prompt with the given variables
        formatted_prompt = instructions_prompt_template.format_prompt(
            format_instructions=parser_output_cmd.get_format_instructions(),
            FARMER_INPUT_QUERY=farmer_input_query
        )
        self.pipeline_logs["prompt_provided_to_llm_as_parser"] = formatted_prompt.to_string()

        model_name_as_role = f"{self.parser_model_id}_as_parser"
        error_type = self.execution_errors_list[0]
        try:
            with get_openai_callback() as cb:
                parsed_response = parser_chain.invoke({
                    "format_instructions": parser_output_cmd.get_format_instructions(),
                    "FARMER_INPUT_QUERY": farmer_input_query
                })

                dssatlm_parser_response = self.unpack_parser_output(parsed_response)
                self.pipeline_logs["dssatlm_parser_response"] = dssatlm_parser_response
                self.pipeline_logs["question_statement_parsed"] = dssatlm_parser_response["question_statement"]
                self.pipeline_logs["dssatlm_parser_response_metadata"] = self.record_api_usage(model_name_as_role, cb)
                print("Step 1: Successfully parsed the query to simulator structure.")
                return dssatlm_parser_response
            
        except groq.APIStatusError as e:
            self.handle_groq_api_error(e, error_type, model_name_as_role, "Step 1")

        except openai.error.AuthenticationError as e:
            self.handle_open_api_error()

        except Exception as e:
            self.handle_generic_error(e, error_type, model_name_as_role, "Step 1 (parsing query to simulator structure (question and input.json))")
        

    def unpack_parser_output(self, parsed_response: DssatLMParserResponse = None) -> dict:
        parsed_response = parsed_response if parsed_response else DssatLMParserResponse()
        parser_output = {**get_schema_dict_from_pydanticmodel(parsed_response)}
        return parser_output


    # ================== SIMULATOR ==================

    def is_simulation_possible(self, dssat_input_json):
        self.simulation_is_possible = run_dssat_exp_cli.is_simulation_possible(dssat_input_json)
        self.pipeline_logs["simulation_is_possible"] = self.simulation_is_possible
        return self.simulation_is_possible
    
    def was_simulation_successful(self, dssatlm_simulator_response):
        simulation_is_successful = REQUIRED_DSSATSIM_OUTPUT_KEYS <= set(dssatlm_simulator_response.keys())
        self.pipeline_logs["simulation_is_successful"] = simulation_is_successful
        return simulation_is_successful
    
    def get_primary_simulation_outputs(self, simulator_response):
        primary_outputs = {key: simulator_response[key] for key in REQUIRED_DSSATSIM_OUTPUT_KEYS if key in simulator_response}
        for key in primary_outputs:
            primary_outputs[key] = {sub_key: value for sub_key, value in primary_outputs[key].items() if sub_key not in UNWANTED_SUB_KEYS_FROM_SIMULATOR_OUTPUT}
        
        return primary_outputs

    def run_dssat_simulation(self, dssat_input_json):
        """
        Run DSSAT simulation with the required inputs
        """
        error_type = self.execution_errors_list[1]
        try:

            if not self.is_simulation_possible(dssat_input_json):
                self.pipeline_logs["execution_errors"][error_type] += f"\n At {get_current_time()}: Simulation is not possible due to missing required inputs."
                raise ValueError(error_type)
            
            else:
                _, simulator_response = run_dssat_exp_cli.exec(input_file=dssat_input_json)
                self.dssatlm_simulator_response = self.get_primary_simulation_outputs(simulator_response)

                if not self.was_simulation_successful(self.dssatlm_simulator_response):
                    self.pipeline_logs["execution_errors"][error_type] += f"\n At {get_current_time()}: Simulation run but was not successful. Required SUMMARY.OUT's output keys are missing."
                    raise ValueError(error_type)
                
                self.pipeline_logs["dssatlm_simulator_response"] = self.dssatlm_simulator_response
                print("Step 2: Successfully ran DSSAT simulation")
                return self.dssatlm_simulator_response

        except Exception as e:
            self.pipeline_logs["execution_errors"][error_type] += f"\n At {get_current_time()}: (while running DSSAT simulation): {str(e)}"
            raise ValueError(error_type)
        

    # ================== INTERPRETER ==================

    def generate_prompt_for_interpreter(self):

        with open(SYS_PROMPT_TEMPLATE_AS_INTERPRETER_FPATH, 'r') as f:
            sys_prompt_template_as_interpreter = f.read()

        with open(USR_PROMPT_TEMPLATE_FOR_INTERPRETER_FPATH, 'r') as f:
            user_prompt_template_for_interpreter = f.read()

        instructions_prompt_template =  ChatPromptTemplate([
            ("system", sys_prompt_template_as_interpreter),
            ("user", user_prompt_template_for_interpreter)
        ])

        return instructions_prompt_template
    
    
    def interpret_simulation_results_for_farmer(self, question_statement, sim_outputs_json, definitions_bank=None, questions_bank=None):
        interpreter_output_cmd = PydanticOutputParser(pydantic_object=DssatLMInterpreterResponse)

        if definitions_bank is None:
            with open(DEFINITIONS_BANK_FPATH, 'r') as f: definitions_bank = f.read()
        if questions_bank is None:
            with open(QUESTIONS_BANK_FPATH, 'r') as f: questions_bank = f.read()

        instructions_prompt_template = self.generate_prompt_for_interpreter()
        interpreter_chain = instructions_prompt_template | self.interpreter.model | interpreter_output_cmd

        formatted_prompt = instructions_prompt_template.format_prompt(
            format_instructions=interpreter_output_cmd.get_format_instructions(),
            SIMULATION_OUTCOMES_IN_JSON=sim_outputs_json,
            FARMER_QUESTION_STATEMENT=question_statement,
            DEFINITIONS_BANK=definitions_bank,
            QUESTIONS_BANK=questions_bank
        )
        self.pipeline_logs["prompt_provided_to_llm_as_interpreter"] = formatted_prompt.to_string()
        
        model_name_as_role = f"{self.interpreter_model_id}_as_interpreter"
        error_type = self.execution_errors_list[2]

        try:
            with get_openai_callback() as cb:
                interpreted_response = interpreter_chain.invoke({
                    "format_instructions": interpreter_output_cmd.get_format_instructions(),
                    "SIMULATION_OUTCOMES_IN_JSON": sim_outputs_json,
                    "FARMER_QUESTION_STATEMENT": question_statement,
                    'DEFINITIONS_BANK': definitions_bank,
                    'QUESTIONS_BANK': questions_bank
                })

                self.pipeline_logs["dssatlm_interpreter_response"] = self.unpack_interpreter_output(interpreted_response)
                self.pipeline_logs["dssatlm_interpreter_response_metadata"] = self.record_api_usage(model_name_as_role, cb)
                print("Step 3: Successfully interpreted simulation results for farmer.")


                
                return self.pipeline_logs["dssatlm_interpreter_response"]
            
        except groq.APIStatusError as e:
            self.handle_groq_api_error(e, error_type, model_name_as_role, "Step 3")

        except openai.error.AuthenticationError as e:
            self.handle_open_api_error()
        
        except Exception as e:
            self.handle_generic_error(e, error_type, model_name_as_role, "Step 3 (interpreting simulation results for farmer)")

    def create_formulaic_ground_truth_answer(self, sim_outputs_json, question_statement):
        """
        Create a formulaic ground truth answer for the farmer
        """
        sample_dfn_n_questions_df = pd.read_csv(SAMPLE_DEFN_N_QUESTIONS_COVERED_FPATH)

        if question_statement not in sample_dfn_n_questions_df["QUESTIONS"].values:
            answer_statement =  "not applicable"
        else:
            df_ = sample_dfn_n_questions_df[sample_dfn_n_questions_df["QUESTIONS"] == question_statement]
            category_definition = df_["CATEGORY_DEFINITIONS"].values[0]
            category_type = df_["CATEGORY-TYPE"].values[0]
            category = df_["CATEGORY"].values[0]
            answer_value = sim_outputs_json[category_type][category]
            answer_statement = f"The {category} is {answer_value}. Here is more definition: {category_definition}"

        self.pipeline_logs["dssatlm_simulator_ground_truth_answer"] = answer_statement
        return answer_statement


    def unpack_interpreter_output(self, interpreted_response: DssatLMInterpreterResponse = None) -> dict:
        interpreted_response = interpreted_response if interpreted_response else DssatLMInterpreterResponse()
        interpreted_output = {**get_schema_dict_from_pydanticmodel(interpreted_response)}
        return interpreted_output

   
    # ================== MISC & HELPERS ==================

    def handle_wandb_api_error(self):
        raise ValueError("WandB API key is invalid.")
    
    def handle_open_api_error(self):
        raise ValueError("OpenAI API key is invalid.")
    
    def handle_groq_api_error(self, e, error_type, model_name_as_role, context):
        if e.status_code == 413:
            nice_error_message = f"{context}: Failed because the LLM is unable to process this payload. The input to the LLM is too large (according to the API provider service), and thus must be reduced."
        elif e.status_code == 401:
            nice_error_message = f"{context}: Failed because the API key is invalid."
            raise ValueError("GROQ API key is invalid.")
        else:
            nice_error_message = f"{context}: Failed due to an API status error."

        print(nice_error_message)
        self.pipeline_logs["execution_errors"][error_type] += f"\n At {self.get_current_time()}: {nice_error_message}. More details: {str(e)} | {model_name_as_role}"
        raise ValueError(error_type)

    def handle_generic_error(self, e, error_type, model_name_as_role, context):
        self.pipeline_logs["execution_errors"][error_type] += f"\n At {self.get_current_time()}: (while {context}): {str(e)} | {model_name_as_role}"
        raise ValueError(error_type)

    def record_api_usage(self, model_name_as_role, chain_callback=None) -> dict:
        # see https://python.langchain.com/docs/how_to/llm_token_usage_tracking/
        return {
            f"{model_name_as_role} - Total Tokens" : chain_callback.total_tokens if chain_callback else self.missing_value_id,
            f"{model_name_as_role} - Prompt Tokens": chain_callback.prompt_tokens if chain_callback else self.missing_value_id,
            f"{model_name_as_role} - Completion Tokens": chain_callback.completion_tokens if chain_callback else self.missing_value_id,
            f"{model_name_as_role} - Total Cost (USD)": chain_callback.total_cost if chain_callback else self.missing_value_id,
        }

    def set_up_wandb(self, wandb_params):
        self.wandb_params = wandb_params
        try:
            return wandb.init(**wandb_params)

        except wandb.errors.AuthenticationError as e:
            self.handle_wandb_api_error()
        except Exception as e:
            raise ValueError(f"Error while setting up WandB: {str(e)}")
        

    def close_wandb(self):
        self.wandb_run.finish()

    def setup_pipeline_logs(self):
        log = {
            "simulation_is_possible": self.simulation_is_possible,
            "simulation_is_successful": False,
            "pipeline_ran_successfully": True,
            "question_statement_parsed": None,
            "dssatlm_parser_response": self.unpack_parser_output(parsed_response=None),
            "dssatlm_parser_response_metadata": self.record_api_usage(f"{self.parser_model_id}_as_parser", chain_callback=None),
            "dssatlm_simulator_response": self.dssatlm_simulator_response,
            "dssatlm_simulator_ground_truth_answer": None,
            "dssatlm_interpreter_response": self.unpack_interpreter_output(interpreted_response=None),
            "dssatlm_interpreter_response_metadata": self.record_api_usage(f"{self.interpreter_model_id}_as_interpreter", chain_callback=None),
            "prompt_provided_to_llm_as_parser": None,
            "prompt_provided_to_llm_as_interpreter": None,
            "execution_errors": {
                "Error occured in step 1 (Parsing)": "",
                "Error occured in step 2 (Simulation)": "",
                "Error occured in step 3 (Interpreting)": "",
            },
        }
        execution_errors_list = list(log["execution_errors"].keys())
        return log, execution_errors_list
    
    def get_logs(self, subkey=None):
        if subkey:
            return self.pipeline_logs[subkey] if subkey in self.pipeline_logs else None
        return self.pipeline_logs
    
    def save_logs(self, output_dir=TMP_DIR):
        prefix = "dssatlm_logs"
        if 'name' in self.wandb_params:
            fname = self.wandb_params["name"].replace("run", prefix)
        else:
            fname = f"{prefix}_{get_current_time()}".replace(" ", "_").replace(":", "-")

        file_path = os.path.join(TMP_DIR, f"{fname}.json")

        dict_to_json_file(self.pipeline_logs, file_path)
        self.save_wandb_artifact(file_path, os.path.basename(file_path), "logs")
        print(f"Logs saved at: {file_path}. And also saved as a WandB artifact.")

    def save_wandb_artifact(self,  artifact_file_path, artifact_name, artifact_type='dataset'):
        artifact = wandb.Artifact(artifact_name, type=artifact_type)
        artifact.add_file(artifact_file_path)
        self.wandb_run.log_artifact(artifact)

    
    def setup_api_keys(self):
        for api_key in API_KEYS_REQUIRED:
            if not os.environ.get(api_key):
                raise ValueError(f"{api_key} is required but not found in the environment variables. Please set it before instantiating the pipeline.")

        
    def ensure_llm_ids_are_valid(self):
        if self.parser_model_id not in LLM_IDS_CONSIDERED:
            raise ValueError(f"Parser model ID {self.parser_model_id} is not in the list of considered LLM IDs: {LLM_IDS_CONSIDERED.keys()}")
        if self.interpreter_model_id not in LLM_IDS_CONSIDERED:
            raise ValueError(f"Interpreter model ID {self.interpreter_model_id} is not in the list of considered LLM IDs: {LLM_IDS_CONSIDERED.keys()}")

    def set_llm_ids_full(self):
        self.parser_model_id_full = LLM_IDS_CONSIDERED[self.parser_model_id]
        self.interpreter_model_id_full = LLM_IDS_CONSIDERED[self.interpreter_model_id]

    def __repr__(self):
        return f"DSSATAnyLMPipeline(parser={self.parser}, interpreter={self.interpreter})"
    

