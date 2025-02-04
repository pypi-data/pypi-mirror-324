class AutoDocifyError(Exception):
    """
    Base exception for all AutoDocify errors.
    """
    def __init__(self, message: str, suggestion: str = ""):
        super().__init__(message)
        self.message = message
        self.suggestion = suggestion

    def __str__(self):
        if self.suggestion:
            return f"{self.message} Suggestion: {self.suggestion}"
        return self.message


class InvalidDirectoryError(AutoDocifyError):
    """
    Raised when the provided directory is invalid or does not exist.
    """
    def __init__(self, directory: str):
        super().__init__(
            message=f"Invalid directory: '{directory}'.",
            suggestion="Ensure the directory exists and the path is correct."
        )


class GitError(AutoDocifyError):
    """
    Raised for Git-related issues, such as not being in a Git repository.
    """
    def __init__(self, message: str, suggestion: str = "Ensure you are in a valid Git repository."):
        super().__init__(message=message, suggestion=suggestion)


class AIGenerationError(AutoDocifyError):
    """
    Raised when AI content generation fails (e.g., due to API errors or invalid responses).
    """
    def __init__(self, message: str):
        super().__init__(
            message=message,
            suggestion="Check your AI integration settings and ensure the API is reachable."
        )


class MergeError(AutoDocifyError):
    """
    Raised when file merging fails during content generation.
    """
    def __init__(self, message: str):
        super().__init__(
            message=message,
            suggestion="Verify that the files being merged exist and are accessible."
        )


class FileValidationError(AutoDocifyError):
    """
    Raised when provided files are invalid or do not meet expected criteria.
    """
    def __init__(self, invalid_files: list):
        super().__init__(
            message=f"The following files are invalid or inaccessible: {', '.join(invalid_files)}",
            suggestion="Ensure the files exist and are readable."
        )


class UnsupportedLLMError(AutoDocifyError):
    """
    Raised when an unsupported LLM (Language Learning Model) is specified.
    """
    def __init__(self, llm: str, supported_llms: list):
        super().__init__(
            message=f"Unsupported LLM: '{llm}'.",
            suggestion=f"Use one of the supported LLMs: {', '.join(supported_llms)}."
        )


class TemporaryFileError(AutoDocifyError):
    """
    Raised when temporary files like merge.txt cannot be created or deleted.
    """
    def __init__(self, message: str):
        super().__init__(
            message=message,
            suggestion="Check file permissions and ensure the temporary directory is writable."
        )
