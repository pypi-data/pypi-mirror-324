
import os 
import uuid 
import re 
import shutil
from loguru import logger
from equator_qa.equator_classes import EQUATOR_Client


# Configure the logger
logger.add(
    "equator.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",          # Include all messages for detailed debugging
    rotation="50 MB",       # Rotate log file after it reaches 50 MB
    retention="30 days",    # Keep logs for 30 days
)



def extract_model_parts(model_string):
    """
    Splits a model string into its constituent parts based on a predefined pattern.
    
    This function uses a regular expression to extract two parts from the `model_string`,
    separated by a forward slash (`/`). If the string matches the pattern, it returns a tuple
    containing both parts. Otherwise, it returns `(None, None)`.
    
    Args:
        model_string (str):
            The model identifier string to be split. Expected format is "part1/part2",
            where neither part contains a forward slash (`/`) or colon (`:`).
    
    Returns:
        Tuple[Optional[str], Optional[str]]:
            A tuple containing the two extracted parts of the model string. Returns `(None, None)`
            if the input does not match the expected pattern.
    
    Example:
        ```python
        part1, part2 = extract_model_parts("category/model")
        print(part1)  # Output: "category"
        print(part2)  # Output: "model"
        
        part1, part2 = extract_model_parts("invalidmodelstring")
        print(part1)  # Output: None
        print(part2)  # Output: None
        ```
    
    Notes:
        - Ensure that the `model_string` follows the "part1/part2" format to successfully extract both parts.
        - This function does not handle cases where there are multiple slashes or colons in the `model_string`.
    """
    # Define the regex pattern to extract both parts
    pattern = r"^([^/]+)/([^/:]+)"
    # Use re.match to find the model parts
    match = re.match(pattern, model_string)
    if match:
        return match.group(1), match.group(2)
    return None, None


def begin_benchmark(
    VISION, 
    execution_steps,
    student_ollama_models,
    student_groq_models,
    student_openrouter_models,
    OLLAMA_EVALUATOR_MODEL,
    GROQ_EVALUATOR_MODEL,
    vectordb_instance,
    benchmark_name,
    date_now,
    answer_rounds,
):
    """
    Initiates and manages the benchmarking process based on specified execution steps.

    Depending on the `execution_steps`, this function evaluates student models against evaluator models
    using the EQUATOR_Client. It supports various evaluation workflows, including:
    - Ollama to GROQ
    - GROQ to Ollama
    - Ollama to OpenRouter
    - Ollama to Ollama
    - GROQ to OpenRouter

    Args:
        execution_steps (str):
            Specifies the benchmarking workflow to execute (e.g., "ollama_to_groq_evaluate").
        
        student_ollama_models (List[str]):
            List of student models using the Ollama platform.
        
        student_groq_models (List[str]):
            List of student models using the GROQ platform.
        
        student_openrouter_models (List[str]):
            List of student models using the OpenRouter platform.
        
        OLLAMA_EVALUATOR_MODEL (str):
            The evaluator model identifier for Ollama evaluations.
        
        GROQ_EVALUATOR_MODEL (str):
            The evaluator model identifier for GROQ evaluations.
        
        vectordb_instance:
            Instance of the vector database used for storing and retrieving embeddings.
        
        benchmark_name (str):
            Name of the benchmark being executed.
        
        date_now (str):
            Current date in a suitable string format for folder naming.
        
        answer_rounds (int):
            Number of evaluation rounds to perform.

    Returns:
        None

    Example:
        ```python
        begin_benchmark(
            execution_steps="ollama_to_groq_evaluate",
            student_ollama_models=["ollama-model-1", "ollama-model-2"],
            student_groq_models=["groq-model-1"],
            student_openrouter_models=["openrouter-model-1"],
            OLLAMA_EVALUATOR_MODEL="ollama-eval-model",
            GROQ_EVALUATOR_MODEL="groq-eval-model",
            vectordb_instance=vector_db,
            benchmark_name="midterm_benchmark",
            date_now="2025-01-19",
            answer_rounds=5,
        )
        ```

    Notes:
        - Ensure that the `EQUATOR_Client` is correctly implemented and imported.
        - The `extract_model_parts` function should be defined to parse model identifiers.
        - Logging should be properly configured to capture informational and debug messages.
        - Directory paths for saving outputs should have the necessary write permissions.
    """
    logger.info(f"Starting benchmark execution steps -> {execution_steps}")
    logger.info(f"VISION True of False = {VISION}")
    if VISION == True and "ollama_to_groq_evaluate_vision" in execution_steps:

        logger.info(f"VISION == True")
        # TODO: implement VISION-specific logic here
        logger.info(f"ollama_to_groq_evaluate_vision <- execution_steps {execution_steps}" )
        for model in student_groq_models:
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            student_model = model
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"

            if student_model:
                logger.info(f"Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Groq student model ")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} Groq Student model")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller_VISION(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-vision-",
                )

    elif VISION == True and "ollama_to_ollama_evaluate_vision" in execution_steps:
        logger.info("VISION == True and ollama_to_ollama_evaluate_vision")
        print("VISION == True and ollama_to_ollama_evaluate_vision")
        # TODO: implement VISION-specific logic here
        logger.info(f"ollama_to_ollama_evaluate_vision <- execution_steps {execution_steps}" )
        for model in student_ollama_models:
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            student_model = model
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"
            if student_model:
                logger.info(f"Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Ollama Student")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} Ollama Student")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller_VISION(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-vision-",
                )

    elif "ollama_to_groq_evaluate" in execution_steps:
        logger.info(f"ollama_to_groq_evaluate == execution_steps = {execution_steps}")
        for model in student_groq_models:
            student_model = model
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"  # TODO: think about a more generic way of doing this
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")

            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Local Student")
            logger.info("1. GETTING EQUATOR Evaluator ANSWERS -> GROQ Student")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")

                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "groq_to_ollama_evaluate" in execution_steps:
        logger.info(f"groq_to_ollama_evaluate == execution_steps = {execution_steps}")
        for model in student_ollama_models:
            evaluator_model = GROQ_EVALUATOR_MODEL
            student_model = model
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Local Student")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> {student_model} Ollama Student")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "ollama_to_openrouter_evaluate" in execution_steps:
        logger.info(f"ollama_to_openrouter_evaluate <- execution_steps = {execution_steps}")
        for model in student_openrouter_models:
            model_path = model
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            lab, student_model = extract_model_parts(model)
            lab = "eval-"
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            student_models = [student_model]
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            print("1. GETTING EQUATOR LLM Evaluator ANSWERS")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} openrouter Student")
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "ollama_to_ollama_evaluate" in execution_steps:
        logger.info(f"ollama_to_ollama_evaluate <- execution_steps {execution_steps}" )
        for model in student_ollama_models:
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            student_model = model
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"
            if student_model:
                logger.info(f"Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Ollama Student")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} Ollama Student")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "groq_to_openrouter_evaluate" in execution_steps:
        logger.info(f"groq_to_openrouter_evaluate <- execution_steps {execution_steps}" )
        for model in student_openrouter_models:
            model_path = model
            _, student_model = extract_model_parts(model)
            lab = "eval"
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_model = student_model.replace("/", "-")

            student_models = [student_model]

            evaluator_model = GROQ_EVALUATOR_MODEL
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            print("1. GETTING BERNARD LLM Evaluator ANSWERS")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} openrouter Student")
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )



def is_valid_uuid4(uuid_string):
    """
    Validate that a string is a valid UUID4.

    Args:
        uuid_string (str): The string to validate.

    Returns:
        bool: True if valid UUID4, False otherwise.
    """
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return str(val) == uuid_string

def cleanup_chromadb(db_filename="chroma.sqlite3", root_dir="."):
    """
    Clean up the ChromaDB by removing the specified SQLite file and any directories
    in the root directory that have names matching UUIDv4.

    Args:
        db_filename (str): The name of the SQLite database file to remove.
        root_dir (str): The root directory to search for UUIDv4-named directories.
    """
    # Construct the full path for the database file
    db_path = os.path.join(root_dir, db_filename)

    # 1. Remove chromadb.sqlite3 file if it exists
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            logger.info(f"Removed database file: {db_path}")
        except Exception as e:
            logger.error(f"Failed to remove database file '{db_path}': {e}")
    else:
        logger.warning(f"Database file '{db_path}' does not exist.")

    # 2. Remove directories in the root directory that look like UUIDv4
    try:
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path) and is_valid_uuid4(item):
                try:
                    shutil.rmtree(item_path)
                    logger.info(f"Removed UUID-like directory: {item_path}")
                except Exception as e:
                    logger.error(f"Failed to remove directory '{item_path}': {e}")
    except Exception as e:
        logger.error(f"Failed to list directories in '{root_dir}': {e}")
    