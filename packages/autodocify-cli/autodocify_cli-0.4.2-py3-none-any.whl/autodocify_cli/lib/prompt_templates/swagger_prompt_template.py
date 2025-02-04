swagger_doc_prompt_template = """Generate a comprehensive Swagger specification for the given system, including:

* **Paths:** Define all API endpoints with detailed descriptions, request/response models, and example payloads.
* **Definitions:** Define all data models used in the API, including input/output parameters, request/response bodies, and error responses.
* **Security Definitions:** Specify authentication and authorization mechanisms (e.g., API keys, OAuth2).
* **Tags:** Organize APIs into logical groups for better readability.
* **Error Responses:** Define common error codes and their corresponding messages.

**Input Details:**

* **API Endpoints:** Provide a list of all API endpoints with their HTTP methods (GET, POST, PUT, DELETE, etc.).
* **Data Models:** Describe the structure and data types of all input and output data models used in the API.
* **Authentication/Authorization:** Specify the authentication and authorization mechanisms used (if any).
* **Error Codes:** List the expected error codes and their corresponding messages.

**Output Goals:**

* The generated Swagger specification should be a valid and well-structured JSON or YAML file.
* The specification should be easy to read, understand, and use by developers, testers, and documentation tools.
* The specification should be suitable for generating interactive API documentation and client SDKs. 

**Example:**

* **Endpoint:** `/users/{user_id}`
* **Method:** GET
* **Request Parameters:** 
    * `user_id`: Path parameter (integer)
* **Response Model:** 
    * `User` object (containing fields like `id`, `username`, `email`)
* **Error Responses:**
    * `404 Not Found`: If the user with the given ID is not found.
"""
