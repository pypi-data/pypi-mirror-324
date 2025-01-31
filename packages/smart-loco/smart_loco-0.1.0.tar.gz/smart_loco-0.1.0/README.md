# Smart Loco

A Streamlit application to interact with local LLMs using Ollama APIs.

## Features

- Chat interface for interacting with local LLMs
- Support for multiple local models through Ollama
- Customizable system prompts
- Adjustable temperature settings
- Chat history management
- Minimal and clean user interface

## Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running locally
- At least one model pulled in Ollama

## Installation

```bash
pip install smart-loco
```

## Usage

After installation, you can start the application by running:

```bash
smart-loco
```

This will launch the Streamlit interface in your default web browser.

### Configuration

1. Select a model from the sidebar (models must be previously pulled using Ollama)
2. Customize the system prompt to set the AI's behavior and context
3. Adjust the temperature setting (0.0 for more focused responses, 1.0 for more creative ones)
4. Start chatting!

### Chat History

Chat history is automatically saved locally and can be cleared using the "Clear History" button in the sidebar.

## Development

To contribute or modify the application:

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Run the application in development mode:
   ```bash
   smart-loco
   ```

## License

MIT