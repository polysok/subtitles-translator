# Subtitles Translator

Subtitles Translator is a command-line tool for easily translating subtitle
files (`.srt`) into different languages using an LLM (OpenAI-compatible) server.

## Features

- Automatic translation of subtitle files
- Support for any target language
- Works with any OpenAI-compatible LLM endpoint (local or remote)
- Simple interactive command-line interface

## Why use this project?

This project facilitates video content localization by automating subtitle
translation, allowing you to reach a broader international audience.

## Requirements

- Python 3.13+
- An OpenAI-compatible LLM server (e.g. [LM Studio](https://lmstudio.ai/),
  Ollama, or a remote API)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/polysok/subtitles-translator.git
   cd subtitles-translator
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests
   ```

3. Configure the LLM endpoint (optional — defaults shown below):
   ```bash
   export LLM_ENDPOINT="http://localhost:1234"   # OpenAI-compatible server
   export LLM_NAME="gemma-4-26b-a4b-it-mlx"       # model name
   export LLM_APIKEY="your-api-key"               # API key, if required
   ```

4. Run the application:
   ```bash
   python -m app
   ```
   You will be prompted for the path to your `.srt` file and the target
   language. The translated file is written next to the source with a
   `_translated.srt` suffix.

> Tip: running from the `src/` directory, or installing the package, ensures the
> `app` module is importable. From the project root you can also run:
> ```bash
> PYTHONPATH=src python -m app
> ```

## Building a standalone executable

You can package the tool as a single self-contained binary (no Python required
on the target machine) using [PyInstaller](https://pyinstaller.org/):

```bash
./build.sh
```

The binary is written to `dist/subtitles-translator`. Build on each platform you
want to target (the produced binary is platform-specific). On macOS, unsigned
binaries may be blocked by Gatekeeper on other machines; sign and notarize them
for distribution.

## Support

For help, open an issue on the [project's GitHub](https://github.com/polysok/subtitles-translator/issues).

## Contributors

This project is maintained by Poly SOK and GitHub contributors. Contributions are welcome!

## License

MIT
