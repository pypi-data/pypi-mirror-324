# FileCannon

## Introduction

FileCannon is an AI-powered file generation CLI tool that creates new files based on examples and natural language descriptions. It leverages AI models to generate content, making it easy to quickly create files with a structure similar to provided examples.

## Installation

```bash
pip install filecannon
```

Then, you can use the `filecannon` command with the following syntax:

```bash
filecannon <prompt> [options]
```

### Arguments:

- `prompt`: Description of the file to generate (required)

### Options:

- `-e, --example`: Path to example file(s) (can be used multiple times)
- `-m, --model`: Model to use (default: claude-3-5-sonnet-20240620)
- `-o, --output`: Output directory (default: current directory)

### Example:

```bash
filecannon "Create a Python script that calculates fibonacci numbers" -e examples/math_functions.py -o output/
```

## Files

The main custom files in this project are:

- `filecannon.py`: The main script containing the CLI logic and core functionality
- `ai_manager.py`: Handles AI interactions and prompt management
- `file_manager.py`: Manages file operations and tool implementations
- `tool_parser.py`: Allows XML use of tools by FileCannon

## Methods

### AIManager

- `generate_content(prompt: str, examples: List[str], example_contents: List[str]) -> str`
- `construct_prompt(user_prompt: str, context: dict) -> str`

### FileManager

- `list_files(directory: str) -> List[str]`
- `read_file(path: str) -> str`
- `write_file(path: str, content: str) -> bool`
- `validate_path(path: str) -> bool`

### ToolParser

This component allows XML use of tools by FileCannon. The specific methods are not detailed in the specification.

## Models

FileCannon supports the following AI models:

- Claude 3.5 Sonnet (default)
- OpenAI models (configurable)

## Available CSS styles

This project is a CLI tool and does not include any CSS styles.

## Available JS functions

This project is a CLI tool and does not include any JavaScript functions.

## Additional notes

1. Environment Variables:
   - Set `ANTHROPIC_API_KEY` if using Claude models
   - Set `OPENAI_API_KEY` if using OpenAI models
   - Set `OPENAI_BASE_URL` if using OpenAI (defaults to "https://api.openai.com")

2. Dependencies:
   - openai
   - anthropic

3. This project uses [ai-agent-toolbox](https://github.com/255BITS/ai-agent-toolbox) for tool management and XML handling.

*Part of the [255labs.xyz](https://255labs.xyz) toolkit for AI-first development.*

## License

MIT
