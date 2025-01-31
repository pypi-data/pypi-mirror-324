import os
import re 
import sqlite3
import json
import json as jn
from loguru import logger
from prompts import get_evaluator_system_prompt, get_student_prompt
from prompts_vision import (
    get_evaluator_system_prompt_vision, get_student_prompt_vision
)
from equator_qa.llmscalls import (
    call_ollama_evaluator_api,
    call_groq_evaluator_api,
    call_openrouter_student_api,
    call_groq_student_api,
    call_ollama_student_docker,
    call_lava_student_api_vision,
    call_groq_student_api_vision,

)




def sanitize_string(value):
    """
    Escapes curly braces in strings to prevent issues with format specifiers in logging.
    """
    if isinstance(value, str):
        return value.replace("{", "{{").replace("}", "}}")
    return value

def extract_score_from_string(response_string):
    """
    Extracts a numerical score from a response string using predefined patterns.
    
    This function searches the input `response_string` for various patterns that indicate a score.
    It uses regular expressions to match different formats and returns the first found score as an integer.
    If no score pattern is matched, it returns `None`.
    
    Args:
        response_string (str):
            The string containing the evaluator's response from which to extract the score.
    
    Returns:
        Optional[int]:
            The extracted score as an integer if a pattern is matched; otherwise, `None`.
    
    Example:
        ```python
        response = "The score assigned is 85%."
        score = extract_score_from_string(response)
        print(score)  # Output: 85
        ```
    
    Notes:
        - The function is case-insensitive and handles multiple score formats.
        - Ensure that the response strings follow one of the predefined patterns for accurate extraction.
    """
    # Regular expressions to match different patterns that indicate a score
    patterns = [
        r"\"score\"\s*:\s*(\d+)",  # JSON-like: "score": 0 or "score":0
        r"'score':\s*(\d+)",       # Python dict-like: {'score': 0}
        r"'grade':\s*(\d+)",       # Python dict-like: {'grade': 0}
        r"Grade:\s*(\d+)",          # Grade without ratio, e.g., Grade: 0
        r"Grade:\s*{'score':\s*(\d+)}",  # Grade followed by Python dict, e.g., Grade: {'score': 0}
        r"Score:\s*{'score':\s*(\d+)}",  # Score followed by Python dict, e.g., Score: {'score': 0}
        r"\*\*Score:\*\*\s*{'score':\s*(\d+)}",  # Markdown Score followed by Python dict, e.g., **Score:** {'score': 20}
        r"\*\*Grade:\*\*\s*{'score':\s*(\d+)}",  # Markdown Grade followed by Python dict, e.g., **Grade:** {'score': 0}
        r"score\s*is\s*(\d+)%",               # Plain text: score is 0%
        r"score\s*of\s*\*\*(\d+)%\*\*",       # Markdown: score of **0%**
        r"the\s*score\s*assigned\s*is\s*(\d+)%",  # Assigned score: the score assigned is 0%
        r"Grade:\s*A\s*\(\s*(\d+)%\)",        # Grade with percentage, e.g., Grade: A (100%)
        r"Grade:\s*[F]\s*\(\s*(\d+)/\d+\)",   # Grade F with ratio, e.g., Grade: F (0/10)
        r"Grade:\s*(\d+)/\d+",                # Ratio format, e.g., Grade: 0/10
        r"\*\*Grade:\*\*\s*(\d+)/\d+",        # Markdown style: **Grade:** 0/10
        r"\*\*Grade:\*\*\s*F\s*\(\s*(\d+)/\d+\)",  # Markdown style with grade F: **Grade:** F (0/100)
        r"Grade:\s*\*\*(\d+)/\d+\*\*",        # Markdown format, e.g., **Grade:** 0/10
        r"Grade:\s*F\s*\(\s*(\d+)\s*out\s*of\s*\d+\)",  # Grade F with "out of", e.g., Grade: F (0 out of 10)
        r"You\s*received\s*a\s*score\s*of\s*(\d+)\s*out\s*of\s*\d+",  # Plain text: You received a score of 0 out of 10
        r"\*\*(\d+)/100\s*score\*\*",        # Markdown style, e.g., **100/100 score**
        r"would\s*earn\s*a\s*score\s*of\s*(\d+)",  # Plain text: would earn a score of 100
        r"return\s*a\s*score\s*of\s*(\d+)",       # Plain text: return a score of 0
    ]

    # Iterate over each pattern to find a match
    for pattern in patterns:
        match = re.search(pattern, response_string, re.IGNORECASE)
        if match:
            return int(match.group(1))

    # If no matching score pattern is found, return None
    return None

def create_template_json(
    student_model,
    output_path,
    question_id,
    category,
    human_answer,
    question,
    student_answer,
    evaluator_response,
    score,
):
    """
    Creates or updates a JSON file with evaluation results for a student's answer.

    This function ensures the output directory exists, loads existing data if available,
    updates the JSON structure with the new evaluation data, and saves it back to the file.

    Args:
        student_model (str):
            The identifier of the student model that generated the answer.
        output_path (str):
            The file path where the JSON data will be saved or updated.
        question_id (str):
            The unique identifier for the question being evaluated.
        category (str):
            The category or topic of the question.
        human_answer (str):
            The correct or reference answer provided by a human.
        question (str):
            The text of the question being evaluated.
        student_answer (str):
            The answer generated by the student model.
        evaluator_response (str):
            The feedback or evaluation provided by the evaluator.
        score (float):
            The numerical score assigned based on the evaluation.

    Returns:
        None

    Example:
        ```python
        create_template_json(
            student_model="gpt-4",
            output_path="./results/evaluation.json",
            question_id="Q123",
            category="Biology",
            human_answer="Photosynthesis is the process by which green plants...",
            question="Explain photosynthesis.",
            student_answer="Photosynthesis allows plants to convert sunlight into energy.",
            evaluator_response="The answer is correct but lacks detail on the chemical process.",
            score=85.0,
        )
        ```
    
    Notes:
        - Ensure that the `jn` module is correctly imported as `json`.
        - The function will overwrite existing entries with the same `question_id`.
        - Handle sensitive data appropriately when writing to JSON files.
    """
    # Ensure the directory for the output path exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    logger.info(f"student_model = {student_model} ")
    # Load existing data if the file exists
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as infile:
                template_data = jn.load(infile)
        except (jn.JSONDecodeError, FileNotFoundError):
            template_data = {}  # Start fresh if file is empty or corrupted
    else:
        template_data = {}

    # Define or update the structure of the template JSON
    template_data[question_id] = {
        "category": category,
        "question": question,
        "human_answer": human_answer,
        "model_answer": student_answer,
        "eval_response": evaluator_response,
        "score": score,
    }

    # Write the updated data back to the file
    with open(output_path, "w", encoding="utf-8") as json_file:
        jn.dump(template_data, json_file, indent=4, ensure_ascii=False)

    logger.info(f"Template JSON created/updated: {output_path}")


class EQUATOR_Client(object):
    """
    EQUATOR_Client handles the benchmarking process by evaluating student models against evaluator models
    using a vector database for storing and retrieving embeddings.

    Attributes:
        student_model (str): The identifier of the student model.
        evaluator_model (str): The identifier of the evaluator model.
        execution_steps (str): The workflow steps to execute.
        vectordb2: Instance of the vector database for embeddings management.
    """

    def __init__(
        self,
        execution_steps,
        student_model,
        evaluator_model,
        vectordb_instance,
    ):
        """
        Initializes the EQUATOR_Client with the necessary parameters.

        Args:
            execution_steps (str):
                Specifies the benchmarking workflow to execute (e.g., "ollama_to_groq_evaluate").
            
            student_model (str):
                The identifier of the student model to be evaluated.
            
            evaluator_model (str):
                The identifier of the evaluator model to assess the student model's performance.
            
            vectordb_instance:
                Instance of the vector database used for storing and retrieving embeddings.
        """
        self.student_model = student_model
        self.evaluator_model = evaluator_model
        self.execution_steps = execution_steps
        self.vectordb2 = vectordb_instance

    def EQUATOR_Controller_VISION(
        self,
        model_path,
        lab,
        student_models,
        answer_save_path_round,
        count,
        prefix_replace,
    ):
        """
        Controls the evaluation vision process by iterating through questions in the vector database,
        obtaining evaluator responses, and saving the results.

        Args:
            model_path (str):
                The path or identifier of the model to be used for generating responses.
            
            lab (str):
                The label or identifier for the current evaluation context.
            
            student_models (List[str]):
                A list of student model identifiers to be evaluated.
            
            answer_save_path_round (str):
                The directory path where the evaluation results for the current round will be saved.
            
            count (int):
                The current round count of the evaluation process.
            
            prefix_replace (str):
                A prefix string to replace or append in the output filenames for organization.
        
        Returns:
            None
        
        Notes:
            - Ensure that the `get_student_prompt`, `extract_score_from_string`, and `create_template_json` functions are defined and imported.
            - The `EQUATOR_Controller` method interacts with a SQLite database named `chroma.sqlite3`. Ensure that this database exists and is accessible.
            - Logging is used extensively for tracking the evaluation process. Ensure that the logging configuration captures the desired log levels.
            - The method currently stops processing if a question with ID "1" is encountered. Modify the stop condition as needed.
        """
        print("prefix ==", prefix_replace)

        # Path to your chroma.sqlite3 file
        db_path = "chroma.sqlite3"
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        batch_size = 100  # Define your batch size
        offset = 0  # Start offset
        stop_processing = False  # Flag to stop the outer loop
        while True:
            # Fetch a batch of results
            query = f"""
            SELECT 
                json_extract(string_value, '$.id'), 
                json_extract(string_value, '$.category'), 
                json_extract(string_value, '$.question'), 
                json_extract(string_value, '$.response') 
            FROM embedding_fulltext_search
            LIMIT {batch_size} OFFSET {offset}
            """
            logger.info(
                f"sqlite executing query with OFFSET={offset}, LIMIT={batch_size}"
            )
            cursor.execute(query)
            results = cursor.fetchall()

            # Break the loop if no more records are fetched
            if not results:
                logger.info("No more records found. Exiting.")
                break

            for row in results:
                question_id, category, question_text, response = row
                logger.info(f"Processing Question ID: {question_id}, Category: {category}, Question: {question_text}, Answer: {response}")
                ## TODO : Parse image directory for images based on question id 

                # Simulate stripping and processing text
                question = question_text.strip() if question_text else ""
                human_answer = response.strip() if response else ""

                for student_model in student_models:
                    output_path = f"{answer_save_path_round}/round_{count + 1}/{prefix_replace}{self.evaluator_model+'-'}{'stu-'}{student_model}.json"
                    if model_path:
                        logger.info(f"Model Path  = {model_path}")
                    else:
                        model_path = ""
                        logger.info("Model Path  = Not provided.")
                    logger.info(f"student_model = {student_model}")
                    # Call your evaluator function
                    images_dir = "images"
                    # Evaluator gets the student question as a prompt for call evaluattor vision 
                    evaluator_result = self.call_evaluator_vision(
                        question_id,
                        student_model, 
                        question,
                        images_dir,
                    )
                    logger.debug(evaluator_result)
                    if evaluator_result is None:
                        logger.error("Evaluator failed to return a result.")
                        continue

                    student_answer, evaluator_response = evaluator_result

                    if isinstance(evaluator_response, tuple) and evaluator_response[0] == "Error":
                        logger.error(f"Evaluator API failed: {evaluator_response[1]}")
                        evaluator_response = "No response"  # Assign a default string

                    if isinstance(evaluator_response, dict):  # Ensure it's a string before regex
                        evaluator_response = json.dumps(evaluator_response)

                    score = extract_score_from_string(evaluator_response)


                    logger.info(f"score = {score}")
                    create_template_json(
                        student_model,
                        output_path,
                        question_id,
                        category,
                        human_answer,
                        question,
                        student_answer,
                        evaluator_response,
                        score,
                    )
                # Stop processing if a condition is met
                if question_id == "1":  # Replace "1" with the desired stop condition
                    logger.debug("Stop condition met. Exiting.")
                    stop_processing = True  # Set the flag to stop outer loop
                    break
            # Increment offset to fetch the next batch
            if stop_processing:
                logger.debug("Breaking the outer loop.")
                break
            offset += batch_size  # Move to the next batch

        # Close the database connection after processing
        conn.close()
        logger.info("Database connection closed.")

    def EQUATOR_Controller(
        self,
        model_path,
        lab,
        student_models,
        answer_save_path_round,
        count,
        prefix_replace,
    ):
        """
        Controls the evaluation process by iterating through questions in the vector database,
        obtaining evaluator responses, and saving the results.

        Args:
            model_path (str):
                The path or identifier of the model to be used for generating responses.
            
            lab (str):
                The label or identifier for the current evaluation context.
            
            student_models (List[str]):
                A list of student model identifiers to be evaluated.
            
            answer_save_path_round (str):
                The directory path where the evaluation results for the current round will be saved.
            
            count (int):
                The current round count of the evaluation process.
            
            prefix_replace (str):
                A prefix string to replace or append in the output filenames for organization.
        
        Returns:
            None

        Example:
            ```python
            client = EQUATOR_Client(
                execution_steps="ollama_to_groq_evaluate",
                student_model="groq-model-1",
                evaluator_model="ollama-eval-model",
                vectordb_instance=vector_db,
            )
            client.EQUATOR_Controller(
                model_path="",
                lab="eval",
                student_models=["groq-model-1"],
                answer_save_path_round="./2025-01-19-midterm_benchmark/auto_eval_outputs",
                count=0,
                prefix_replace="equator-",
            )
            ```
        
        Notes:
            - Ensure that the `get_student_prompt`, `extract_score_from_string`, and `create_template_json` functions are defined and imported.
            - The `EQUATOR_Controller` method interacts with a SQLite database named `chroma.sqlite3`. Ensure that this database exists and is accessible.
            - Logging is used extensively for tracking the evaluation process. Ensure that the logging configuration captures the desired log levels.
            - The method currently stops processing if a question with ID "1" is encountered. Modify the stop condition as needed.
        """
        print("prefix ==", prefix_replace)

        # Path to your chroma.sqlite3 file
        db_path = "chroma.sqlite3"
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        batch_size = 100  # Define your batch size
        offset = 0  # Start offset
        stop_processing = False  # Flag to stop the outer loop
        while True:
            # Fetch a batch of results
            query = f"""
            SELECT 
                json_extract(string_value, '$.id'), 
                json_extract(string_value, '$.category'), 
                json_extract(string_value, '$.question'), 
                json_extract(string_value, '$.response') 
            FROM embedding_fulltext_search
            LIMIT {batch_size} OFFSET {offset}
            """
            logger.info(
                f"sqlite executing query with OFFSET={offset}, LIMIT={batch_size}"
            )
            cursor.execute(query)
            results = cursor.fetchall()

            # Break the loop if no more records are fetched
            if not results:
                logger.info("No more records found. Exiting.")
                break

            for row in results:
                question_id, category, question_text, response = row
                logger.info(f"Processing Question ID: {question_id}, Category: {category}, Question: {question_text}, Answer: {response}")

                # Simulate stripping and processing text
                question = question_text.strip() if question_text else ""
                human_answer = response.strip() if response else ""

                for student_model in student_models:
                    output_path = f"{answer_save_path_round}/round_{count + 1}/{prefix_replace}{self.evaluator_model+'-'}{'stu-'}{student_model}.json"
                    if model_path:
                        logger.info(f"Model Path  = {model_path}")
                    logger.info(f"student_model = {student_model}")

                    # Call your evaluator function
                    evaluator_result = self.call_evaluator(
                        model_path=model_path,
                        prompt=question,
                    )
                    if evaluator_result is None:
                        logger.error("Evaluator failed to return a result.")
                        continue

                    student_answer, evaluator_response = evaluator_result

                    score = extract_score_from_string(evaluator_response)
                    logger.info(f"score = {score}")
                    create_template_json(
                        student_model,
                        output_path,
                        question_id,
                        category,
                        human_answer,
                        question,
                        student_answer,
                        evaluator_response,
                        score,
                    )
                # Stop processing if a condition is met
                if question_id == "1":  # Replace "1" with the desired stop condition
                    logger.debug("Stop condition met. Exiting.")
                    stop_processing = True  # Set the flag to stop outer loop
                    break
            # Increment offset to fetch the next batch
            if stop_processing:
                logger.debug("Breaking the outer loop.")
                break
            offset += batch_size  # Move to the next batch

        # Close the database connection after processing
        conn.close()
        logger.info("Database connection closed.")

    def student_vision(self,student_model, full_prompt, json_path):
        logger.info(f"json_path: { json_path}")
    
        """
        Retrieves a student's vision based answer by invoking the appropriate evaluator API based on execution steps.

        Args:
            model_path (str):
                The path or identifier of the student model to be used.
            full_prompt_student (str):
                The student's prompt that needs to be processed and evaluated comes from prompt_vision.py

        Returns:
            Optional[str]:
                The student's answer returned by the evaluator API if successful, otherwise `None`.
        
        Notes:
            - Ensure that the `get_student_prompt_vision` function is defined and properly formats the messages.
            - The evaluator functions (`call_openrouter_student_api`, `call_ollama_student_api`, etc.) must be imported and accessible.
            - Logging is used to track the execution flow and responses.
        """
        logger.info(f"student model, full prompt , json_path = {student_model} {full_prompt} {json_path}")

        logger.info(f"!!!!!Execution steps = {self.execution_steps}")
        
        if "ollama_to_openrouter_evaluate" in self.execution_steps:
            # logger.info(f"call_openrouter_student_api <-  {self.execution_steps}")
            # response = call_openrouter_student_api(
            #     full_prompt_student,  model_path
            # )
            logger.info("ollama to openrouater vision not supported yet try ollama to groq or ollama to ollam. Edit in main.py")
            print("ollama to openrouater vision not supported yet try ollama to groq or ollama to ollam. Edit in main.py")
            return "ollama to openrouater vision not supported yet try ollama to groq or ollama to ollam. Edit in main.py"

        # elif "groq_to_ollama_evaluate" in self.execution_steps:
            # logger.info(f"call_ollama_student_api  <- {self.execution_steps}")
            # response = call_ollama_student_api_vision(
            #     full_prompt_student, self.student_model
            # )
            # logger.info(f"call_ollama_student_api -> response {response}")            
            # return response

        elif "groq_to_ollama_evaluate" in self.execution_steps:
            logger.info("groq to ollama vision not supported yet try ollama to groq or ollama to ollam model. Edit in main.py")        
            print("groq to ollama vision not supported yet try ollama to groq or ollama to ollam model. Edit in main.py") 
            return "groq to ollama vision not supported yet try ollama to groq or ollama to ollam model. Edit in main.py"

        elif "ollama_to_ollama_evaluate_vision" in self.execution_steps:
            logger.info(f"call_ollama_student_docker <- {self.execution_steps}")
            logger.info(f"json_path == {json_path}")
            response = call_lava_student_api_vision(full_prompt, json_path, student_model)
            logger.info(f"call_ollama_student_docker -> response {response}")
            logger.info(f"response == {response}")
            return response

        elif "ollama_to_groq_evaluate_vision" in self.execution_steps:
            logger.info(f"call_groq_student_api <- {self.execution_steps}") 
            logger.info(f"json_path == {json_path}")         
            response = call_groq_student_api_vision(full_prompt, json_path, student_model)
            logger.info(f"response == {response}")
            return response
        
        # elif "groq_to_openrouter_evaluate" in self.execution_steps:
        #     logger.info(f"call_openrouter_student_api <- {self.execution_steps}")

        #     response = call_openrouter_student_api(
        #         full_prompt_student, model_path
        #     )
        #     logger.info(f"call_openrouter_student_api -> response {response}")
        #     return response
        elif "groq_to_openrouter_evaluate" in self.execution_steps:
            logger.info(f"groq to openrouter vision not supported try ollama to groq or ollama to ollam model. Edit in main.py")     
            print("groq to openrouter vision not supported try ollama to groq or ollama to ollam model. Edit in main.py") 
            return "groq to openrouter vision not supported try ollama to groq or ollama to ollam model. Edit in main.py"

        return None
    # Generate student answer
    def student(self, model_path, full_prompt_student):
        """
        Retrieves a student's answer by invoking the appropriate evaluator API based on execution steps.

        Args:
            model_path (str):
                The path or identifier of the student model to be used.
            full_prompt_student (str):
                The student's prompt that needs to be processed and evaluated.

        Returns:
            Optional[str]:
                The student's answer returned by the evaluator API if successful, otherwise `None`.

        Example:
            ```python
            response = client.student("ollama-model-v1", "Explain photosynthesis.")
            if response:
                print(f"Student Answer: {response}")
            else:
                print("Failed to retrieve student answer.")
            ```
        
        Notes:
            - Ensure that the `get_student_prompt` function is defined and properly formats the messages.
            - The evaluator functions (`call_openrouter_student_api`, `call_ollama_student_api`, etc.) must be imported and accessible.
            - Logging is used to track the execution flow and responses.
        """
        model_path = str(model_path)
        if model_path:
            logger.info(f"Model Path = {model_path}")
        logger.info(f"Execution steps = {self.execution_steps}")
        
        if "ollama_to_openrouter_evaluate" in self.execution_steps:
            logger.info(f"call_openrouter_student_api <-  {self.execution_steps}")
            response = call_openrouter_student_api(
                full_prompt_student,  model_path
            )
            return response

        elif "groq_to_ollama_evaluate" in self.execution_steps:
            logger.info(f"call_ollama_student_api  <- {self.execution_steps}")
            response = call_ollama_student_docker(
                full_prompt_student, self.student_model
            )
            logger.info(f"call_ollama_student_api -> response {response}")            
            return response

        elif "ollama_to_ollama_evaluate" in self.execution_steps:
            logger.info(f"call_ollama_student_docker <- {self.execution_steps}")
        
            response = call_ollama_student_docker(
                full_prompt_student, self.student_model
            )

            logger.info(f"call_ollama_student_docker -> response {response}")
            return response

        elif "ollama_to_groq_evaluate" in self.execution_steps:
            logger.info(f"call_groq_student_api <- {self.execution_steps}")           

            response = call_groq_student_api(
                full_prompt_student, self.student_model
            )
            logger.info(f"call_groq_student_api -> response {response}")            
            return response

        elif "groq_to_openrouter_evaluate" in self.execution_steps:
            logger.info(f"call_openrouter_student_api <- {self.execution_steps}")

            response = call_openrouter_student_api(
                full_prompt_student, model_path
            )
            logger.info(f"call_openrouter_student_api -> response {response}")
            return response

        return None
    

    def call_evaluator_vision(self, question_id,  student_model, prompt, images_dir):
        """
        Calls the appropriate evaluator vision API based on the execution steps and retrieves the evaluation response.

        Args:
            model_path (str):
                The path or identifier of the evaluator model to be used.
            prompt (str):
                The prompt/question to be evaluated.
            images_dir (str, optional):
                The directory where image files (and their corresponding JSON metadata) are stored.
                Defaults to "images".

        Returns:
            Union[None, List, Tuple[str, str]]:
                - None: If retrieval of documents or the student's answer fails, or if no evaluation is performed.
                - List: An empty list if the specified images directory does not exist.
                - Tuple[str, str]: A tuple containing the student's answer and the evaluator's response, if successful.
        """
        results = self.vectordb2.retrieve_embedding(question_id)
        logger.info(f"Retrieved embedding {results}")
        if results is None:
            logger.error("Failed to retrieve similar documents.")
            return None
        context = ""
        student_answer = ""
        eval_response = ""
        if "documents" in results and results["documents"]:
                metadatas = results.get("metadatas", [])[0]
                
                for metadata in metadatas:
                    context += f"Question: {metadata.get('question', '')}\n"
                    context += f"Answer: {metadata.get('response', '')}\n\n"
                                        
                    unique_id = metadata.get("id", "").strip()  # Ensure the ID is clean

                    # Ensure unique_id is valid
                    if not unique_id:
                        logger.error("No unique ID found in metadata.")
                        return []

                    # Ensure the directory exists
                    if not os.path.isdir(images_dir):
                        logger.error(f"Directory '{images_dir}' does not exist.")
                        return []

                    # Iterate through images directory
                    for filename in os.listdir(images_dir):
                        if filename.lower().endswith(".jpg"):
                            unique_json = filename[:-4]  # Strip '.jpg' to get the ID
                            
                            if unique_id == unique_json:
                                json_filename = f"{unique_id}.jpg"
                                
                                # Ensure paths are cross-platform compatible
                                json_path = os.path.normpath(os.path.join(images_dir, json_filename))
                                image_path = os.path.normpath(os.path.join(images_dir, filename))

                                if os.path.isfile(json_path):
                                    print(f"Found matching JSON for '{filename}'. Image path: {image_path}")
                                    logger.info(f"found maching JSON  for '{filename}'. Image path: {image_path}")
                                else:
                                    print(f"No matching JSON for '{filename}'. Expected '{json_filename}'.")
                                model_path = ""
                                # student_answer = self.student_vision(model_path, prompt, image_path)
                                # if not student_answer:
                                #     logger.error("Failed to get Student Answer.")
                                #     return None
                                full_prompt = get_student_prompt_vision(prompt)
                                logger.info(f"Full prompt = {full_prompt}")
                                student_answer = self.student_vision(student_model, full_prompt, json_path)
                                logger.info(f"Student Answer: {student_answer}")

                                if not student_answer:
                                    logger.error("Failed to get Student Answer.")
                                    return None
                                eval_response = "None"
                                evaluator_system_prompt = get_evaluator_system_prompt_vision(context, student_answer)
                                # #Must pass student_answer to evaluator 
                                # if "ollama_to_ollama_evaluate_vision" in self.execution_steps:
                                
                                #     logger.info(f"!!!!!!call_ollama_evaluator_api <- {self.execution_steps}")

                                #     student_answer, eval_response, *extra = call_ollama_evaluator_api(
                                #         self.evaluator_model, json_filename, evaluator_system_prompt
                                #     )
                                    
                                #     if student_answer is None or eval_response is None:
                                #         logger.error("Failed to get Student Answer or Evaluator Response.")
                                #         return "Failed to get Student Answer or Evaluator Response"
                                #     logger.info(f"Student Answer: {student_answer}")
                                #     logger.info(f"Evaluator Response: {eval_response}")
                                #     return student_answer, eval_response
                                
                                # elif "ollama_to_groq_evaluate_vision" in self.execution_steps:
                                #     logger.info(f"call_groq_evaluator_api <- {self.execution_steps}")

                                #     student_answer, eval_response = call_groq_evaluator_api (
                                #         self.evaluator_model, student_answer, evaluator_system_prompt
                                #     )

                                return student_answer, eval_response

    def call_evaluator(self, model_path, prompt):
        """
        Calls the appropriate evaluator API based on the execution steps and retrieves the evaluation response.

        Args:
            model_path (str):
                The path or identifier of the evaluator model to be used.
            prompt (str):
                The prompt/question to be evaluated.

        Returns:
            Optional[Tuple[str, str]]:
                A tuple containing the student's answer and the evaluator's response if successful, otherwise `None`.
        """
        results = self.vectordb2.retrieve_embedding(prompt)
        if results is None:
            logger.error("Failed to retrieve similar documents.")
            return None
        context = ""
        if "documents" in results and results["documents"]:
            metadatas = results.get("metadatas", [])[0]
            for metadata in metadatas:
                context += f"Question: {metadata.get('question', '')}\n"
                context += f"Answer: {metadata.get('response', '')}\n\n"
            # logger.info(context)
            logger.info(f"Similar documents found. -> {context}")
        else:
            logger.warning("No similar documents found.")
        # full prompt is called from prompt.py 
        full_prompt = get_student_prompt(prompt)
        student_answer = self.student(model_path, full_prompt)
        if not student_answer:
            logger.error("Failed to get Student Answer.")
            return None

        logger.info(f"Student Answer: {student_answer}")

        evaluator_system_prompt = get_evaluator_system_prompt(context, student_answer)

        if "ollama_to_groq_evaluate" in self.execution_steps:
            logger.info(f"call_ollama_evaluator_api <- {self.execution_steps}")          
            student_answer, eval_response = call_ollama_evaluator_api(
                self.evaluator_model, student_answer, evaluator_system_prompt
            )
            return student_answer, eval_response

        elif (
            "ollama_to_ollama_evaluate" in self.execution_steps
            or "ollama_to_openrouter_evaluate" in self.execution_steps
        ):
            logger.info(f"call_ollama_evaluator_api <- {self.execution_steps}")

            student_answer, eval_response = call_ollama_evaluator_api(
                self.evaluator_model, student_answer, evaluator_system_prompt
            )
            return student_answer, eval_response


        elif "groq_to_openrouter_evaluate" in self.execution_steps:
            logger.info(f"call_openrouter_student_api <- {self.execution_steps}")
         
            student_answer, eval_response = call_openrouter_student_api(
                self.evaluator_model, student_answer, evaluator_system_prompt
            )
            return student_answer, eval_response

        return None
