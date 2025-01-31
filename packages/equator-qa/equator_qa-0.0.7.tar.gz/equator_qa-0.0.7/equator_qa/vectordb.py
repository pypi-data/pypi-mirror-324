from loguru import logger
import json
import chromadb
import requests


class VectorDB_Controller(object):
    def __init__(self, keepVectorDB, VISION):
        """
        Initialize the VectorDB_Controller class.

        Parameters:
        keepVectorDB (bool): A flag indicating whether to keep the VectorDB or not.

        Attributes:
        base_url (str): The base URL for the VectorDB service.
        chroma_client (chromadb.PersistentClient): The Chroma client for interacting with the VectorDB.
        keepVectorDB (bool): A flag indicating whether to keep the VectorDB or not.

        If keepVectorDB is False, the function will open the "linguistic_benchmark.json" file,
        parse the data, and create a VectorDB using the parsed conversations.
        """
        self.base_url = "http://localhost:11434"  # in container
        self.chroma_client = chromadb.PersistentClient(path=".")
        self.keepVectorDB = keepVectorDB

        if not keepVectorDB:
            # open file for vector score
            # Open and load the JSON file
            logger.info(f"Vector db vision = {VISION}")
            if VISION == True:
                with open("vision_benchmark.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            elif VISION == False:
                with open("linguistic_benchmark.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

            # Initialize a list to store the parsed conversations
            conversations = []
            # Iterate over the list of dictionaries
            for entry in data:
                parsed_entry = {
                    "id": entry.get(
                        "index", ""
                    ),  # Use "index" as the unique identifier
                    "category": entry.get("category", ""),  # Extract category
                    "question": entry.get("question", ""),  # Extract the question
                    "response": entry.get(
                        "human_answer", ""
                    ),  # Extract the human answer
                }
                conversations.append(parsed_entry)
            logger.info(conversations)
            self.create_vector_db(conversations)

    def generate_embeddings(self, model, input_text, truncate=True):
        """
        Generate embeddings for the given input text using the specified model.

        This function sends a POST request to the embedding API endpoint to generate
        embeddings for the provided input text.

        Parameters:
        model (str): The name of the model to use for generating embeddings.
        input_text (str): The text for which embeddings are to be generated.
        truncate (bool, optional): Whether to truncate the input text. Defaults to True.

        Returns:
        dict or None: A dictionary containing the generated embeddings if successful,
                      or None if there was an error or no embeddings were found in the response.

        Raises:
        requests.RequestException: If there's an error in making the API request.
        """
        url = f"{self.base_url}/api/embed"
        payload = {"model": model, "input": input_text, "truncate": truncate}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            if response.headers.get("Content-Type").startswith("application/json"):
                response_json = response.json()
                if "embeddings" in response_json:
                    return response_json
                else:
                    logger.error(f"No embeddings found in response: {response_json}")
                    return None
            else:
                logger.error(
                    f"Unexpected response content type: {response.headers.get('Content-Type')}"
                )
                logger.error(f"Response content: {response.text}")
                return None
        except requests.RequestException as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return None

    def retrieve_embedding(self, prompt, n_results=1):
        """
        Retrieve embeddings for a given prompt and query the vector database.

        This function generates embeddings for the input prompt, flattens them,
        and then queries the vector database to find similar entries.

        Parameters:
        prompt (str): The input text for which to retrieve similar embeddings.
        n_results (int, optional): The number of results to return from the query. Defaults to 1.

        Returns:
        dict or None: A dictionary containing the query results if successful,
                      or None if there was an error in embedding generation or database querying.
        """
        response = self.generate_embeddings(model="all-minilm", input_text=prompt)
        if not response or "embeddings" not in response:
            logger.error("Failed to retrieve embeddings from the model.")
            return None
        prompt_embedding = self.flatten_embedding(response["embeddings"])
        vector_db = self.chroma_client.get_collection(name="conversations")
        try:
            results = vector_db.query(
                query_embeddings=[prompt_embedding], n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying vector DB: {e}")
            return None
    def retrieve_embedding_vision(self, prompt, n_results=1):
        """
        Retrieve embeddings for a given prompt and query the vector database.

        This function generates embeddings for the input prompt, flattens them,
        and then queries the vector database to find similar entries.

        Parameters:
        prompt (str): The input text for which to retrieve similar embeddings.
        n_results (int, optional): The number of results to return from the query. Defaults to 1.

        Returns:
        dict or None: A dictionary containing the query results if successful,
                      or None if there was an error in embedding generation or database querying.
        """
        response = self.generate_embeddings(model="all-minilm", input_text=prompt)
        if not response or "embeddings" not in response:
            logger.error("Failed to retrieve embeddings from the model.")
            return None
        prompt_embedding = self.flatten_embedding(response["embeddings"])
        vector_db = self.chroma_client.get_collection(name="conversations")
        try:
            results = vector_db.query(
                query_embeddings=[prompt_embedding], n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying vector DB: {e}")
            return None
    def add_to_vector_db(self, vector_db, entry_id, serialized_conversations, metadata):
        """
        Adds a conversation entry to the specified vector database with its corresponding embeddings and metadata.

        This method performs the following steps:
        1. Generates embeddings for the provided serialized conversations using the "all-minilm" model.
        2. Flattens the embeddings if they are nested.
        3. Converts metadata values to appropriate formats.
        4. Adds the entry, including its ID, embeddings, serialized conversations, and metadata, to the vector database.

        If embedding generation fails or the entry cannot be added to the vector database, the method logs an error message.

        Args:
            vector_db (VectorDatabase):
                An instance of the vector database where the entry will be stored. 
                This database should support the `add` method with parameters `ids`, `embeddings`, `documents`, and `metadatas`.
            
            entry_id (Union[str, int]):
                A unique identifier for the entry being added to the vector database. 
                This ID is used to reference the entry in future operations.
            
            serialized_conversations (str):
                The serialized conversation data to be embedded and stored. 
                This should be a string representation of the conversation, suitable for embedding generation.
            
            metadata (Dict[str, Any]):
                A dictionary containing metadata associated with the conversation. 
                Metadata values will be converted to appropriate formats before being stored.

        Returns:
            None

        Raises:
            None. All exceptions are handled internally and logged as error messages.

        Example:
            ```python
            vector_db = VectorDatabase(...)
            entry_id = 12345
            serialized_conversations = "User: Hello\nBot: Hi there!"
            metadata = {
                "user_id": 67890,
                "timestamp": "2025-01-19T12:34:56Z",
                "conversation_length": 2
            }
            instance.add_to_vector_db(vector_db, entry_id, serialized_conversations, metadata)
            ```

        Notes:
            - The embedding generation uses the "all-minilm" model. Ensure that this model is supported and properly configured.
            - The `flatten_embedding` method is used to handle nested embeddings, ensuring they are in a suitable format for the vector database.
            - Metadata conversion is handled by the `convert_metadata_value` method, which should appropriately transform each metadata value.
            - Errors during embedding generation or database insertion do not raise exceptions but are logged for debugging purposes.
            - Ensure that the `vector_db` instance is properly initialized and connected before calling this method.
        """
        response = self.generate_embeddings(
            model="all-minilm", input_text=serialized_conversations
        )

        if not response or "embeddings" not in response:
            logger.error(
                f"Failed to retrieve embeddings for entry {entry_id}. Response: {response}"
            )
            return
        # Flatten the embedding if it is nested
        embedding = self.flatten_embedding(response["embeddings"])

        converted_metadata = {
            k: self.convert_metadata_value(v) for k, v in metadata.items()
        }

        try:
            vector_db.add(
                ids=[str(entry_id)],
                embeddings=[embedding],
                documents=[serialized_conversations],
                metadatas=[converted_metadata],
            )
        except Exception as e:
            logger.error(f"Error adding entry {entry_id} to the vector DB: {e}")


    def create_vector_db(self, conversations):
        """
        Creates and initializes a vector database collection with the provided conversations.

        This method performs the following steps:
        1. Attempts to delete an existing collection named "conversations" to ensure a fresh start.
        If the collection does not exist, it gracefully handles the `ValueError`.
        2. Creates a new collection named "conversations" using the Chroma client.
        3. Iterates through each conversation in the provided list, serializes it to JSON,
        and adds it to the newly created vector database using the `add_to_vector_db` method.

        Args:
            conversations (List[Dict[str, Any]]):
                A list of conversation dictionaries to be stored in the vector database.
                Each conversation dictionary should contain at least an "id" key and other relevant metadata.

        Returns:
            None

        Raises:
            None. All exceptions related to deleting the existing collection are handled internally.
            Any exceptions raised during the addition of entries to the vector database are handled
            by the `add_to_vector_db` method, which logs the errors.

        Example:
            ```python
            conversations = [
                {
                    "id": 1,
                    "user_id": 101,
                    "timestamp": "2025-01-19T12:00:00Z",
                    "messages": [
                        {"sender": "user", "text": "Hello"},
                        {"sender": "bot", "text": "Hi there!"}
                    ]
                },
                {
                    "id": 2,
                    "user_id": 102,
                    "timestamp": "2025-01-19T12:05:00Z",
                    "messages": [
                        {"sender": "user", "text": "How are you?"},
                        {"sender": "bot", "text": "I'm a bot, so I don't have feelings, but thanks for asking!"}
                    ]
                }
            ]
            instance.create_vector_db(conversations)
            ```

        Notes:
            - The method uses the `chroma_client` to interact with the Chroma vector database.
            Ensure that `chroma_client` is properly initialized and authenticated before calling this method.
            - The collection name is hardcoded as "conversations". If multiple collections are needed,
            consider modifying the method to accept the collection name as a parameter.
            - The `add_to_vector_db` method is responsible for generating embeddings and handling
            the addition of each conversation to the vector database. Ensure that this method
            is correctly implemented and accessible within the class.
            - Conversations are serialized to JSON strings before being added to the vector database.
            Ensure that all conversation dictionaries are JSON-serializable.
            - Deleting the existing "conversations" collection ensures that the vector database starts
            fresh each time `create_vector_db` is called. If persistent storage of previous data is needed,
            consider removing or modifying the deletion step.
        """
        vector_db_name = "conversations"
        try:
            self.chroma_client.delete_collection(name=vector_db_name)
        except ValueError:
            pass  # Handle collection not existing
        vector_db = self.chroma_client.create_collection(name=vector_db_name)
        for c in conversations:
            serialized_conversations = json.dumps(c)
            self.add_to_vector_db(vector_db, c["id"], serialized_conversations, c)


    def convert_metadata_value(self, value):
        """
        Converts a metadata value to a JSON-serializable format suitable for storage.

        This method processes the input `value` to ensure it is in a format that can be
        stored within the vector database's metadata. The conversion rules are as follows:
        - If the value is `None`, it returns an empty string.
        - If the value is a list or dictionary, it serializes it to a JSON string.
        - For all other data types, it returns the value unchanged.

        Args:
            value (Any):
                The metadata value to be converted. This can be of any data type, including
                `None`, list, dictionary, string, integer, float, etc.

        Returns:
            Union[str, Any]:
                - Returns an empty string if the input `value` is `None`.
                - Returns a JSON string if the input `value` is a list or dictionary.
                - Returns the original `value` unchanged for all other data types.

        Raises:
            TypeError:
                If the input `value` is a type that cannot be serialized to JSON (when it's a list or dictionary).

        Example:
            ```python
            # Example usage of convert_metadata_value

            # Case 1: Value is None
            converted = instance.convert_metadata_value(None)
            print(converted)  # Output: ""

            # Case 2: Value is a list
            converted = instance.convert_metadata_value([1, 2, 3])
            print(converted)  # Output: "[1, 2, 3]"

            # Case 3: Value is a dictionary
            converted = instance.convert_metadata_value({"key": "value"})
            print(converted)  # Output: "{"key": "value"}"

            # Case 4: Value is a string
            converted = instance.convert_metadata_value("sample text")
            print(converted)  # Output: "sample text"

            # Case 5: Value is an integer
            converted = instance.convert_metadata_value(42)
            print(converted)  # Output: 42
            ```

        Notes:
            - This method is primarily used to ensure that metadata values are in a consistent and
            JSON-compatible format before being stored in the vector database.
            - When serializing lists or dictionaries, ensure that all nested elements are also JSON-serializable.
            - If the input `value` is a complex object that cannot be serialized to JSON, a `TypeError` will be raised.
            - It is advisable to handle or validate input values before passing them to this method to prevent unexpected errors.
            - The method does not modify the original input; it returns a new converted value based on the input.
        """
        if value is None:
            return ""
        if isinstance(value, (list, dict)):
            return json.dumps(value)
        return value

    def flatten_embedding(self, embedding):
        """
        Flattens a nested embedding list into a single-level list if necessary.

        This method checks whether the first element of the `embedding` is a list. If it is, the method
        assumes that the entire `embedding` is a nested list and proceeds to flatten it into a single-level
        list. If the `embedding` is already a single-level list, it is returned unchanged.

        Args:
            embedding (List[Any]):
                A list representing the embedding. This can be either a single-level list of numerical
                values or a nested list (i.e., a list of lists) that needs to be flattened.

        Returns:
            List[Any]:
                A single-level list containing all elements of the original `embedding`. If the input was
                already a single-level list, it is returned as-is. If it was a nested list, it is flattened
                into a single-level list.

        Raises:
            IndexError:
                If the `embedding` list is empty, accessing `embedding[0]` will raise an `IndexError`.
                Ensure that the `embedding` is a non-empty list before calling this method.
            TypeError:
                If the elements within the `embedding` are not lists when the method expects a nested list,
                a `TypeError` may be raised during the flattening process.

        Example:
            ```python
            # Example usage of flatten_embedding

            # Case 1: Nested embedding
            nested_embedding = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
            flattened = instance.flatten_embedding(nested_embedding)
            print(flattened)  # Output: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

            # Case 2: Already flat embedding
            flat_embedding = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
            flattened = instance.flatten_embedding(flat_embedding)
            print(flattened)  # Output: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
            ```

        Notes:
            - The method assumes that if the first element of `embedding` is a list, then all elements are lists.
            Ensure that the `embedding` follows this structure to avoid inconsistent flattening.
            - Flattening is performed using a list comprehension that iterates through each sublist and each item
            within those sublists. This approach ensures that the order of elements is preserved.
            - If the `embedding` contains elements that are not lists (when the first element is a list), a
            `TypeError` may occur during the flattening process. It is recommended to validate the structure
            of `embedding` before invoking this method.
            - The method does not modify the original `embedding` but returns a new flattened list if necessary.
            - To handle empty embeddings gracefully, consider adding a check for emptiness before attempting
            to access `embedding[0]`.
        """
        # Flatten nested embeddings if necessary
        if isinstance(embedding[0], list):
            return [item for sublist in embedding for item in sublist]
        return embedding


    def add_to_vector_db(self, vector_db, entry_id, serialized_conversations, metadata):
        """
        Adds a conversation entry to the specified vector database with its corresponding embeddings and metadata.

        This method performs the following steps:
        1. Generates embeddings for the provided serialized conversations using the "all-minilm" model.
        2. Validates the response to ensure embeddings are retrieved successfully.
        3. Flattens the embeddings if they are nested to ensure compatibility with the vector database.
        4. Converts metadata values to appropriate formats suitable for storage.
        5. Adds the entry, including its ID, embeddings, serialized conversations, and metadata, to the vector database.

        If embedding generation fails or the entry cannot be added to the vector database, the method logs an error message.

        Args:
            vector_db (VectorDatabase):
                An instance of the vector database where the entry will be stored. 
                This database should support the `add` method with parameters `ids`, `embeddings`, `documents`, and `metadatas`.
            
            entry_id (Union[str, int]):
                A unique identifier for the entry being added to the vector database. 
                This ID is used to reference the entry in future operations.
            
            serialized_conversations (str):
                The serialized conversation data to be embedded and stored. 
                This should be a string representation of the conversation, suitable for embedding generation.
            
            metadata (Dict[str, Any]):
                A dictionary containing metadata associated with the conversation. 
                Metadata values will be converted to appropriate formats before being stored.

        Returns:
            None

        Raises:
            None. All exceptions are handled internally and logged as error messages.

        Example:
            ```python
            # Assuming `instance` is an instance of the class containing this method
            vector_db = VectorDatabase(...)
            entry_id = 12345
            serialized_conversations = "User: Hello\nBot: Hi there!"
            metadata = {
                "user_id": 67890,
                "timestamp": "2025-01-19T12:34:56Z",
                "conversation_length": 2
            }
            instance.add_to_vector_db(vector_db, entry_id, serialized_conversations, metadata)
            ```

        Notes:
            - **Embedding Generation**: The method uses the "all-minilm" model for generating embeddings. Ensure that this model is supported, properly configured, and that the necessary dependencies are installed.
            - **Flattening Embeddings**: The `flatten_embedding` method is used to handle nested embeddings, ensuring they are in a suitable format for the vector database. It's crucial that the embeddings are correctly flattened to maintain their integrity and usefulness.
            - **Metadata Conversion**: Metadata conversion is handled by the `convert_metadata_value` method, which transforms each metadata value into a JSON-serializable format if necessary. Ensure that this method is correctly implemented to handle various data types.
            - **Error Handling**: 
                - If embedding generation fails (e.g., due to an unsupported model or invalid input), an error is logged, and the method exits without adding the entry to the database.
                - If adding the entry to the vector database fails (e.g., due to connectivity issues or invalid data), an error is logged with details of the exception.
            - **Vector Database Requirements**: The `vector_db` instance must be properly initialized, connected, and configured to accept entries with the specified parameters (`ids`, `embeddings`, `documents`, `metadatas`). Ensure that the vector database schema aligns with the data being inserted.
            - **Data Integrity**: 
                - The `entry_id` should be unique to prevent collisions or overwrites in the vector database.
                - The `serialized_conversations` should accurately represent the conversation to ensure meaningful embeddings and retrieval.
            - **Logging**: The method relies on a configured `logger` to record error messages. Ensure that the logging system is set up appropriately to capture and store these logs for debugging and monitoring purposes.
            - **Performance Considerations**: 
                - Batch processing of multiple entries might improve performance if supported by the vector database.
                - Consider implementing retry mechanisms for transient failures during embedding generation or database insertion.
            - **Security**: 
                - Ensure that sensitive information within `serialized_conversations` or `metadata` is handled securely, adhering to data protection regulations and best practices.
                - Validate and sanitize inputs to prevent potential injection attacks or data corruption.

        """
        response = self.generate_embeddings(
            model="all-minilm", input_text=serialized_conversations
        )

        if not response or "embeddings" not in response:
            logger.error(
                f"Failed to retrieve embeddings for entry {entry_id}. Response: {response}"
            )
            return
        # Flatten the embedding if it is nested
        embedding = self.flatten_embedding(response["embeddings"])

        converted_metadata = {
            k: self.convert_metadata_value(v) for k, v in metadata.items()
        }

        try:
            vector_db.add(
                ids=[str(entry_id)],
                embeddings=[embedding],
                documents=[serialized_conversations],
                metadatas=[converted_metadata],
            )
        except Exception as e:
            logger.error(f"Error adding entry {entry_id} to the vector DB: {e}")

