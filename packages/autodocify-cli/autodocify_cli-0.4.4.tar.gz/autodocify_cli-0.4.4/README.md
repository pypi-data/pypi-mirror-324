# AutoDocify CLI

## Overview

AutoDocify CLI is a command-line tool designed to automate the generation of various project documentation, including READMEs, technical documentation, Swagger specifications, and test files.  Leveraging AI, it streamlines your documentation workflow, saving you valuable time and effort.  It currently supports Gemini, OpenAI, and Bard as language models (LLMs).

[//]: # (This is a comment used for Table of Contents generation)
[TOC]


## Installation Instructions

**Prerequisites:**

* Python 3.8 or higher
* `pip` (Python package installer)

**Installation:**

1. Clone the repository:
   ```bash
   git clone <REPOSITORY_URL>
   cd <PROJECT_NAME>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration (Optional):**  Set your AI API keys and backend URLs in the `.env` file.  An example `.env` file (`.env.example`) is provided.  You need to replace the placeholder values with your actual keys.


## Usage Guide

The AutoDocify CLI offers several commands to generate different types of documentation.  All commands accept a `base_dir` argument to specify the project directory. If not provided, it defaults to the current working directory.  The `llm` argument allows you to specify the LLM to use ("gemini", "openai", or "bard").

**Basic Usage:**

```bash
autodocify <command> [options]
```

**Available Commands:**

* `greet`:  A simple greeting command.
* `generate-readme`: Generates a README.md file.
* `generate-tests`: Generates test files (currently supports Python's `pytest`).
* `generate-docs`: Generates technical documentation.
* `generate-swagger`: Generates Swagger documentation (JSON or YAML).

**Examples:**

* Generate a README using Gemini:
  ```bash
  autodocify generate-readme --llm gemini --output-file README_gemini.md
  ```

* Generate tests using Bard in a specific directory:
  ```bash
  autodocify generate-tests --base-dir /path/to/my/project --llm bard
  ```

* Generate Swagger documentation as YAML:
  ```bash
  autodocify generate-swagger --format yaml --output-file swagger.yaml
  ```

## Configuration

AutoDocify uses a `.env` file for configuration.  You can customize settings like the backend URL and AI API keys.  Refer to the `.env.example` file for the structure and available options.  Remember to rename `.env.example` to `.env` after setting your configurations.

## Technical Details

* **Programming Language:** Python
* **Framework:** Typer (for CLI), Rich (for console output)
* **Libraries:**  `requests`, `pydantic-settings`, `google.generativeai` (for Gemini), OpenAI Python library (for OpenAI), potentially others depending on LLM support.
* **Architecture:** The CLI interacts with an AI backend service (currently a placeholder, but the structure supports different LLMs) to generate the documentation.


## Contribution Guidelines

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure they are well-documented and tested.
4. Commit your changes with clear commit messages.
5. Submit a pull request.  Please follow our coding standards and ensure your code passes all tests.


## License

This project is licensed under the <LICENSE_NAME> License - see the [LICENSE](LICENSE) file for details.


## FAQs

* **Q: What AI models are supported?**
    * A: Currently, Gemini, OpenAI, and Bard are supported.  Support for more LLMs may be added in future releases.

* **Q: How can I customize the generated documentation?**
    * A: You can customize the output by modifying the prompts templates found in the `prompt_templates` directory, adjusting settings in the `.env` file, or adding arguments to the CLI commands.

* **Q:  What if the AI generation fails?**
    * A: The CLI includes robust error handling.  It will display informative error messages, which often provide hints to help debug the problem. Contact support if you're unable to resolve the issue.


## Support

For support or bug reports, please open an issue on the [GitHub repository](<REPOSITORY_URL>).  For urgent issues, contact <YOUR_EMAIL>

