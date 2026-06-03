import json

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from app.models.subtitle import Subtitle
from app.tools.json_extraction import JSONExtractor
from app.tools.llm import stream_request_llm_server
from app.tools.translation import process_subtitle_file


__all__ = ["main"]

MAX_CONCAT_SUBTITLES = 5
TRANSLATED_SUFFIX = "_translated.srt"
NARROW_NO_BREAK_SPACE = "\u202f"  # narrow no-break space to normalize
SOURCE_PROMPT = "Enter the path to the subtitle file to translate: "
LANGUAGE_PROMPT = "Enter the target language (e.g., French, Spanish): "


@dataclass(frozen=True)
class TranslationContext:
    """Shared collaborators for translating subtitle batches."""

    language: str
    extractor: JSONExtractor
    output: TextIO


def main() -> int:
    """Prompt for a subtitle file and a language, then translate it."""
    source = _prompt_existing_file(SOURCE_PROMPT)
    language = input(LANGUAGE_PROMPT).strip()
    destination = source.with_name(f"{source.stem}{TRANSLATED_SUFFIX}")
    _translate_file(source, destination, language)
    return 0


def clean_path(raw: str) -> Path:
    """Strip surrounding quotes/whitespace and expand a user-typed path.

    Terminals often wrap a dragged path in quotes; remove them so the
    path resolves correctly.
    """
    return Path(raw.strip().strip("'\"")).expanduser()


def _prompt_existing_file(message: str) -> Path:
    """Ask for a file path until an existing file is provided."""
    while True:
        path = clean_path(input(message))
        if path.is_file():
            return path
        print(f"The file {path} doesn't exist.")


def chunk(items: list[Subtitle], size: int) -> list[list[Subtitle]]:
    """Split a list into consecutive chunks of at most size elements."""
    return [items[i : i + size] for i in range(0, len(items), size)]


def _translate_file(source: Path, destination: Path, language: str) -> None:
    """Translate a subtitle file chunk by chunk and write the result."""
    subtitles = process_subtitle_file(str(source))
    with destination.open("w", encoding="utf-8") as output:
        context = TranslationContext(language, JSONExtractor(), output)
        for batch in chunk(subtitles, MAX_CONCAT_SUBTITLES):
            _translate_batch(batch, context)
    print(f"Translation finished. Result written to {destination}")


def _translate_batch(batch: list[Subtitle], context: TranslationContext) -> None:
    """Translate one batch of subtitles and write them to the output file."""
    prompt = json.dumps([sub.text for sub in batch])
    print(f"Sending request for translation of {len(batch)} items...")
    response = stream_request_llm_server(prompt, context.language)
    translations = _extract_translations(context.extractor, response)
    if not translations:
        print("No translations found in the response.")
        return
    for subtitle, text in zip(batch, translations, strict=False):
        subtitle.text = text.replace(NARROW_NO_BREAK_SPACE, " ")
        context.output.write(_format_subtitle(subtitle))
        print(subtitle)


def _extract_translations(extractor: JSONExtractor, response: str | None) -> list[str]:
    """Return the first translated array from the LLM response, if any."""
    if not response:
        return []
    arrays = extractor.extract_json_arrays(response)
    return arrays[0] if arrays else []


def _format_subtitle(subtitle: Subtitle) -> str:
    """Render a subtitle as an SRT block."""
    return f"{subtitle.index}\n{subtitle.start} --> {subtitle.end}\n{subtitle.text}\n\n"
