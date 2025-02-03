import subprocess
import json
import logging
import os

from CertoraProver.certoraContextClass import CertoraContext
from Shared import certoraUtils as Util
from CertoraProver.certoraCollectRunMetadata import RunMetaData


build_script_logger = logging.getLogger("build_script")
def update_metadata(context: CertoraContext, attr_name: str) -> None:
    metadata = RunMetaData.load_file()
    metadata[attr_name] = getattr(context, attr_name)
    RunMetaData.dump_file(metadata)

def add_list_attr_to_context(context: CertoraContext, json_obj: dict, attr_name: str) -> None:
    if not getattr(context, attr_name, None):
        values = json_obj.get(attr_name)
        if isinstance(values, list) and len(values) > 0:
            cwd: str = os.getcwd()
            new_value = []
            for value in values:
                assert isinstance(value, str), (f"expected a string in '{attr_name}', got {value} "
                                                f"of type {type(value).__name__}")
                if os.path.isabs(value):
                    raise Util.CertoraUserInputError(f"Invalid path in '{attr_name}': {value} must be relative")
                abs_path: str = os.path.join(context.rust_project_directory, value)
                new_value.append(os.path.relpath(abs_path, cwd))
            setattr(context, attr_name, new_value)
            update_metadata(context, attr_name)

def run_script_and_parse_json(context: CertoraContext) -> None:
    if not context.build_script:
        return
    try:
        build_script_logger.info(f"Building from script {context.build_script}")
        run_cmd = [context.build_script, '--json']
        if context.cargo_features is not None:
            run_cmd.append('--cargo_features')
            for feature in context.cargo_features.split(' '):
                run_cmd.append(feature)
        result = subprocess.run(run_cmd, capture_output=True, text=True)

        # Check if the script executed successfully
        if result.returncode != 0:
            raise Util.CertoraUserInputError(f"Error running the script {context.build_script}\n{result.stderr}")

        json_obj = json.loads(result.stdout)

        if not json_obj:
            raise Util.CertoraUserInputError(f"No JSON output from build script {context.build_script}")

        if missing_keys := [key for key in ["success", "project_directory", "sources", "executables"] if key not in json_obj]:
            raise Util.CertoraUserInputError(f"Missing required keys in build script response: {', '.join(missing_keys)}")

        if not json_obj.get("success"):
            raise Util.CertoraUserInputError(
                f"Compilation failed using build script: {context.build_script}\n"
                f"Success value in JSON response is False."
            )

        context.rust_project_directory = json_obj.get("project_directory")
        context.rust_sources = json_obj.get("sources")
        context.rust_executables = json_obj.get("executables")
        if json_obj.get("log") is not None:
            context.rust_logs_stdout = json_obj.get("log").get('stdout')
            context.rust_logs_stderr = json_obj.get("log").get('stderr')

        add_list_attr_to_context(context, json_obj, 'solana_inlining')
        add_list_attr_to_context(context, json_obj, 'solana_summaries')

        if context.test == str(Util.TestValue.AFTER_BUILD_RUST):
            raise Util.TestResultsReady(None)

    except Util.TestResultsReady as e:
        raise e
    except FileNotFoundError as e:
        raise Util.CertoraUserInputError(f"File not found: {e}")
    except json.JSONDecodeError as e:
        raise Util.CertoraUserInputError(f"Error decoding JSON: {e}")
    except Exception as e:
        raise Util.CertoraUserInputError(f"An unexpected error occurred: {e}")
