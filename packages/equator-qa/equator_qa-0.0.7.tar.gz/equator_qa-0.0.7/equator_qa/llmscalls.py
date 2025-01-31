import os
import json
from loguru import logger
import requests
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
from prompts import get_student_prompt
import base64
from prompts_vision import get_student_prompt_vision
import time 
# from pathlib import Path 
import configparser

# Initialize the parser
config = configparser.ConfigParser()

# Read the INI file
config.read("config.ini")

load_dotenv()

def call_groq_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt):
    """
    Evaluates a student's answer using the Groq Evaluator API.

    This function sends the student's answer along with a system prompt to the Groq Evaluator API
    and retrieves the evaluation response.

    Args:
        evaluator_model (str):
            The identifier of the evaluator model to use.
        
        student_answer (str):
            The student's answer to be evaluated.
        
        evaluator_system_prompt (List[Dict[str, str]]):
            A list of messages defining the system prompt for the evaluator.

    Returns:
        Optional[Tuple[str, str]]:
            A tuple containing the `student_answer` and the evaluator's feedback if successful.
            Returns `None` if the evaluation fails.
    
    Example:
        ```python
        evaluator_model = "groq-eval-model-v1"
        student_answer = "The capital of France is Paris."
        evaluator_system_prompt = [
            {"role": "system", "content": "You are an evaluator for geography questions."},
            {"role": "user", "content": "Evaluate the following student answer for correctness and completeness."}
        ]

        result = call_groq_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt)
        if result:
            answer, feedback = result
            print(f"Answer: {answer}\nFeedback: {feedback}")
        else:
            print("Evaluation failed.")
        ```
    
    Notes:
        - Ensure that the `GROQ_API_KEY` environment variable is set.
        - The `Groq` client library must be installed and imported.
        - Handle sensitive data securely.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    gorq_api = Groq(api_key=api_key)
    completion_eval = gorq_api.chat.completions.create(
        temperature=0,
        model=evaluator_model,
        messages=evaluator_system_prompt,
    )
    response_eval = completion_eval.choices[0].message.content

    if response_eval:
        logger.info(f"call_groq_evaluator_api: {response_eval}")
        return student_answer, response_eval
    else:
        logger.error("Failed to get evaluator response.")
        return None


def call_ollama_evaluator_api_vision(evaluator_model, student_answer, evaluator_system_prompt):
    URL = config["ollama_evaluator_vision_url"]["URL"]
    # url = "http://localhost:11434/api/chat"
    payload = {"model": evaluator_model, "messages": evaluator_system_prompt}
    # Make a single POST request
    response = requests.post(
        URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        stream=True,
    )

    complete_message = ""

    # Read the streamed response line by line
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line.decode("utf-8"))
            # Safely retrieve content if present
            if "message" in chunk and "content" in chunk["message"]:
                complete_message += chunk["message"]["content"]

            # If the API signals completion
            if chunk.get("done"):
                break

    logger.info(f"Complete message: {complete_message}")
    return student_answer, complete_message


def call_ollama_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt):
    """
    Evaluates a student's answer using the Ollama Evaluator API.

    Sends the student's answer and a system prompt to the Ollama API and retrieves the evaluation response.

    Args:
        evaluator_model (str):
            The evaluator model to use.
        
        student_answer (str):
            The student's answer to be evaluated.
        
        evaluator_system_prompt (List[Dict[str, str]]):
            A list of messages defining the system prompt for the evaluator.

    Returns:
        Tuple[str, str]:
            A tuple containing the `student_answer` and the evaluator's feedback.

    Example:
        ```python
        evaluator_model = "ollama-model-v1"
        student_answer = "The capital of France is Paris."
        evaluator_system_prompt = [
            {"role": "system", "content": "You are an evaluator for geography questions."},
            {"role": "user", "content": "Evaluate the following student answer for correctness and completeness."}
        ]

        result = call_ollama_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt)
        if result:
            answer, feedback = result
            print(f"Answer: {answer}\nFeedback: {feedback}")
        else:
            print("Evaluation failed.")
        ```

    Notes:
        - Ensure the Ollama API is running and accessible at the specified URL.
        - Handle sensitive data securely.
    """
    logger.info(f"evaluator_model = {evaluator_model}")
    url = config["ollama_evaluator_url"]["URL"]
    # url = "http://localhost:11434/api/chat"
    payload = {"model": evaluator_model, "messages": evaluator_system_prompt}
    # Make a single POST request
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        stream=True,
    )

    complete_message = ""

    # Read the streamed response line by line
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line.decode("utf-8"))
            # Safely retrieve content if present
            if "message" in chunk and "content" in chunk["message"]:
                complete_message += chunk["message"]["content"]

            # If the API signals completion
            if chunk.get("done"):
                break

    logger.info(f"Complete message: {complete_message}")
    return student_answer, complete_message


def call_openrouter_student_api(full_prompt_student, model_path):
    """
    Sends a student's prompt to the OpenRouter API and retrieves the response.

    Args:
        full_prompt_student (str):
            The complete prompt from the student that needs to be processed.
        
        model_path (str):
            The path or identifier of the model to be used for generating the response.

    Returns:
        str:
            The response generated by the OpenRouter API based on the provided prompts.

    Example:
        ```python
        full_prompt_student = "Explain the theory of relativity."
        model_path = "gpt-4"

        response = call_openrouter_student_api(full_prompt_student, model_path)
        print(response)
        ```
    
    Notes:
        - Ensure the `OPENROUTER_KEY` environment variable is set with a valid API key.
        - The `OpenAI` client should be properly installed and imported.
        - The function assumes that `get_student_prompt` is defined and returns the appropriate message format.
    """
    api_key = os.environ.get("OPENROUTER_KEY")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    model_path = str(model_path)

    # Make the API call
    completion = client.chat.completions.create(
        model=model_path,
        messages=get_student_prompt(full_prompt_student),
    )
    # last_api_call_time = time.time()  # Update the time of the last API call
    response = completion.choices[0].message.content
    logger.info(f"call_openrouter_student_api: {response}")
    return response

def process_image(file_name):
    """
    Reads an image file, encodes it in Base64, and returns the encoded string.
    Works on both Windows and Linux.
    
    Args:
        file_name (str): The name of the image file.

    Returns:
        str or None: Base64-encoded image string if successful, None if file not found.
    """
    # Ensure file_name does not contain an extra directory path
    file_name = os.path.basename(file_name)  

    # Get absolute path of the images directory (cross-platform)
    images_dir = os.path.abspath(os.path.join(os.getcwd(), "images"))
    full_path = os.path.join(images_dir, file_name)
    full_path = os.path.normpath(full_path)  # Normalize path

    logger.info(f"Looking for image at: {full_path}")

    if not os.path.exists(full_path):
        logger.error(f"Error: File '{file_name}' not found at '{full_path}'")
        return None

    try:
        with open(full_path, "rb") as image_file:
            encoded_bytes = base64.b64encode(image_file.read())
            return encoded_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return None
    


def call_lava_student_api_vision(full_prompt, image_filename, student_model):
    """
    Calls the LAVA Student API to perform vision-related tasks using the specified student model.

    This function processes an image file, encodes it, and sends it along with a prompt to the LAVA Student API 
    for vision tasks. It handles the API response and logs relevant information throughout the process.

    Args:
        full_prompt (str or list): 
            - If a string, it represents the user prompt to be sent to the API.
            - If a list, it should contain a sequence of messages formatted as dictionaries 
              with roles and content, e.g., [{"role": "user", "content": "Your prompt here"}].
            This prompt guides the API in generating the desired vision-related response.
        
        image_filename (str): 
            The file path to the image that needs to be processed and analyzed by the API. 
            The image will be read, encoded, and included in the API request payload.
        
        student_model (str): 
            The identifier or name of the student model to be used for processing the vision task. 
            This specifies which model variant the API should utilize to handle the request.

    Returns:
        str or tuple:
            - Returns `"Success"` if the API call is successful and the response is received without errors.
            - Returns `("Error", {"error": "Image processing failed"})` if the image encoding fails.
            - Returns an empty string `""` if the API request fails due to network issues or invalid responses.

    Raises:
        None. All exceptions related to the API request and image processing are handled internally. 
        Errors are logged, and appropriate return values are provided to indicate failure states.

    Example:
        ```python
        status = call_lava_student_api_vision(
            full_prompt="Analyze the content of this image.",
            image_filename="/path/to/image.jpg",
            student_model="vision-model-v1"
        )
        if status == "Success":
            print("API call was successful.")
        elif isinstance(status, tuple) and status[0] == "Error":
            print(f"Error occurred: {status[1]['error']}")
        else:
            print("API request failed.")
        ```

    Dependencies:
        - `config`: A dictionary containing configuration settings, specifically the API URL under 
          `config["ollama_evalutor_vision_url"]["URL"]`.
        - `logger`: A logging instance used to log informational and error messages.
        - `process_image`: A function that takes an image filename and returns an encoded version 
          suitable for API transmission.
        - `requests`: The `requests` library is used to send HTTP POST requests to the API endpoint.

    Notes:
        - Ensure that the `image_filename` points to a valid image file that `process_image` can handle.
        - The function currently does not support streaming responses (`"stream": False` in payload).
        - The commented-out code for formatting `full_prompt` suggests potential flexibility 
          for handling different prompt formats, which may be re-enabled or modified in future iterations.
    """
    URL = config["ollama_evalutor_vision_url"]["URL"]

    logger.info(f"Processing image: {image_filename}")

    # Encode the image
    encoded_image = process_image(image_filename)
    if encoded_image is None:
        logger.error("Failed to process image.")
        return "Error", {"error": "Image processing failed"}

    # # Ensure full_prompt is properly formatted
    # if isinstance(full_prompt, list):
    #     messages = full_prompt
    # elif isinstance(full_prompt, str):
    #     messages = [{"role": "user", "content": full_prompt}]
    # else:
    #     logger.error("full_prompt must be a string or a list of messages.")
    #     return "Error", {"error": "Invalid prompt type"}

    # ✅ Corrected API Payload
        # Prepare API payload
    payload = {
        "model": student_model,
        "prompt": full_prompt,
        "stream": False,
        "images": [encoded_image],
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send request to API
        response = requests.post(URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        logger.info(f"API Request successful with status code {response.status_code}")
        logger.info(f"Response: {response.get('response')}")
        logger.info(f"Response: {response.json()}")
        logger.info(f"Response: {response['response']}")

        return "Success"
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return ""
    

def call_groq_student_api_vision(full_prompt, image_filename, student_model):
    """
    Calls the Groq Student API to perform vision-related tasks using the specified student model.

    This function processes an image file, encodes it, and sends it along with a prompt to the Groq Student API 
    for vision tasks. It handles the API response by generating a descriptive caption for the provided image 
    and logs relevant information throughout the process.

    Args:
        full_prompt (str): 
            A string representing the initial prompt or instruction to guide the API in generating the desired response.
            In this function, the `full_prompt` is integrated into the message content to provide context for the API.

        image_filename (str): 
            The file path to the image that needs to be processed and analyzed by the API. 
            The image will be read, encoded in base64 format, and included in the API request payload.

        student_model (str): 
            The identifier or name of the student model to be used for processing the vision task. 
            This specifies which model variant the API should utilize to handle the request.

    Returns:
        str:
            - Returns the generated descriptive one-sentence caption for the provided image if the API call is successful.
            - Returns an empty string `""` if the API request fails due to image processing issues or other exceptions.

    Raises:
        None. All exceptions related to the API request and image processing are handled internally. 
        Errors are logged, and appropriate return values are provided to indicate failure states.

    Example:
        ```python
        caption = call_groq_student_api_vision(
            full_prompt="Analyze the content of this image.",
            image_filename="/path/to/image.jpg",
            student_model="vision-model-v2"
        )
        if caption:
            print(f"Generated Caption: {caption}")
        else:
            print("Failed to generate caption.")
        ```

    Dependencies:
        - `Groq`: A client library for interacting with the Groq Student API. Ensure it is properly installed and configured.
        - `logger`: A logging instance used to log informational and error messages.
        - `process_image`: A function that takes an image filename and returns a base64-encoded version 
          suitable for API transmission.
        - `requests`: Although not directly used in this function, it's commonly used for HTTP requests 
          and may be required by the `Groq` client internally.

    Notes:
        - Ensure that the `image_filename` points to a valid image file that `process_image` can handle.
        - The function concatenates the `full_prompt` with the base64-encoded image in Markdown image syntax.
          This allows the API to interpret and process the image correctly.
        - The function currently expects the Groq client to return a response in the structure 
          `chat_completion.choices[0].message.content`. Adjustments may be necessary if the API response format changes.
        - Logging levels (`info`, `debug`, `error`) are used to provide detailed insights into the function's execution flow.
        - The function does not support streaming responses; it waits for the complete response before returning.
    """
    client = Groq()

    # Encode the image
    encoded_image = process_image(image_filename)
    if encoded_image is None:
        logger.error("Failed to process image.")
        return "Error", {"error": "Image processing failed"}
    
    # Concatenate text and image URL into a single string
    message_content = f"Provide a descriptive one-sentence caption for the given image.\n![Image](data:image/jpg;base64,{encoded_image})"
    
    messages = [
        {
            "role": "user",
            "content": message_content
        }
    ]
    
    logger.debug(f"Sending messages: {messages}")
    
    try:
        logger.debug(f"groq client {client}")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=student_model,
        )
        logger.debug(f"groq vision chat completion generated: {chat_completion}")
        response = chat_completion.choices[0].message.content
        logger.info(f"Groq api vision received response = {response}")
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return ""
    
    logger.info(f"groq api vision resopnse = {response}")
    return response

    
def call_ollama_student_docker(full_prompt_student, student_model):
    """
    Sends a student's formatted conversation history to the Ollama Docker API for evaluation.

    Args:
        full_prompt_student (list[dict]): A list of message dictionaries representing 
            the conversation history. Each dictionary should have:
            - "role" (str): The role in the conversation (e.g., "system", "user", "assistant").
            - "content" (str): The corresponding message content.
        student_model (str): The name of the model to use for generating the response.

    Returns:
        Optional[str]: 
            The assistant's response extracted from the Ollama API response if successful, 
            otherwise None.

    Example:
        
    python
        messages = [
            {"role": "system", "content": "You are a student being tested."},
            {"role": "user", "content": "Explain photosynthesis."}
        ]
        response = call_ollama_student_docker(messages, "ollama-model-v1")
        if response:
            print(response)
        else:
            print("Evaluation failed.")


    Notes:
        - Ensure the Ollama API is running and accessible at http://localhost:11435/api/chat.
        - The function assumes full_prompt_student is a properly formatted list of message 
          dictionaries and does not require additional string manipulation.
    """
    try:
        # Retrieve the API URL from the configuration
        # URL = config["ollama_student_docker_url"]["URL"]
        url = "http://localhost:11435/api/chat"
    
        logger.info(f"Full prompt student = {full_prompt_student}")
        logger.info(f"Student model = {student_model}")
        messages_str = json.dumps(full_prompt_student)
        messages_list = json.loads(messages_str)
        # Prepare the payload for the Ollama API
        logger.info(f"messages_list = {messages_list}")
        logger.info(f"messages_list = {messages_list[1]}")

        logger.info(f"messages_list = {messages_list[0]}")
        payload = {
            "model": "llama3.2",
            "messages": messages_list,  # Directly use the list of dictionaries
            "stream": False,
        }
  

        # Send the POST request to the Ollama API
        response = requests.post(url, json=payload)
        logger.info(f"response = {response}")
        # Log the HTTP status code
        logger.debug(f"HTTP Status Code: {response.status_code}")

        # Log the raw response text for debugging
        logger.debug(f"Raw API response: {response.text}")

        # Raise an exception for HTTP error responses (4xx and 5xx)
        response.raise_for_status()

        try:
            # Attempt to parse the response as JSON
            response_data = response.json()
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON decode error: {json_err} - Response Text: {response.text}")
            return None
        logger.info(f"response_data = {response_data}")
        # Extract the assistant's response
        assistant_response = response_data.get("message", {}).get("content", "")
        
        logger.info(f"Ollama Docker response = {assistant_response}")
        return assistant_response

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response Text: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"General request exception occurred: {req_err}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return None
    
    
def call_groq_student_api(full_prompt_student, groq_student_model):
    """
    Sends a student's prompt to the Groq API and retrieves the response.

    Args:
        full_prompt_student (str):
            The student's prompt to be processed.
        groq_student_model (str):
            The model identifier to use for generating the response.

    Returns:
        Optional[str]:
            The response from the Groq API if successful, otherwise `None`.

    Example:
        ```python
        response = call_groq_student_api("Explain photosynthesis.", "groq-model-v1")
        if response:
            print(response)
        else:
            print("Evaluation failed.")
        ```
    
    Notes:
        - Ensure the `GROQ_API_KEY` environment variable is set with a valid API key.
        - The `Groq` client library must be installed and imported.
        - The `get_student_prompt` function should be defined to format the messages correctly.
    """

    logger.info(f"Groq API full prompt = {full_prompt_student}")
    messages1 =get_student_prompt(full_prompt_student)
    logger.info(f"full prompt = {messages1}")
    api_key = os.environ.get("GROQ_API_KEY")
    gorq_api = Groq(api_key=api_key)
    completion_eval = gorq_api.chat.completions.create(
        temperature=0,
        model=groq_student_model,
        messages=full_prompt_student,
    )
    response = completion_eval.choices[0].message.content

    if response:
        logger.info(f"call_groq_student_api: {response}")
        return response
    else:
        logger.error("Failed to get evaluator response.")
        return None
