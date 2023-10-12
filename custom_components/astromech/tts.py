"""Astromech TTS component."""

import io
from typing import Any
from homeassistant.components import tts
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.tts.models import Voice

import re
import random
import string
import wave
import hashlib

from ttastromech import TTAstromech

from .const import VOICE_ASTROMECH, VOICE_ASTROMECH_SHORT


def generate_hash(input, length):
    """Generate hash."""
    md5_hash = hashlib.md5(input.encode()).hexdigest()
    hash_length = len(md5_hash)
    ratio = hash_length / length
    result = ""

    for i in range(length):
        start = int(i * ratio)
        end = int((i + 1) * ratio)
        substring = md5_hash[start:end]
        ascii_sum = sum(ord(c) for c in substring)
        char_index = ascii_sum % 26
        char = chr(ord("a") + char_index)
        result += char

    return result


def replace_non_alpha_chars(text):
    """Replace invalid characters with a random lowercase ascii letter."""

    random_char = lambda: random.choice(string.ascii_lowercase)

    replaced_text = re.sub(r"[^a-z]", lambda match: random_char(), text)
    return replaced_text


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wyoming speech to text."""
    async_add_entities(
        [
            TextToAstromech(),
        ]
    )


class TextToAstromech(tts.TextToSpeechEntity):
    """Represent a Text To Speech entity."""

    def __init__(self) -> None:
        """Init."""
        self._r2 = TTAstromech()

        self._attr_name = "Astromech"
        self._attr_unique_id = "astromech-tts"

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return ["en", "de", "pl", "es", "it", "fr", "pt", "hi"]  # TODO return all

    @property
    def default_language(self) -> str:
        """Returns the default language."""
        return "en"

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [tts.ATTR_AUDIO_OUTPUT, tts.ATTR_VOICE]

    @property
    def default_options(self):
        """Return a dict include default options."""
        return {tts.ATTR_AUDIO_OUTPUT: "wav"}

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return a list of supported voices for a language."""
        return [
            Voice(VOICE_ASTROMECH, "Astromech"),
            Voice(VOICE_ASTROMECH_SHORT, "Astromech (short)"),
        ]

    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> tts.TtsAudioType:
        """Load tts audio file from the engine."""
        slug = replace_non_alpha_chars(message.lower())

        if options.get(tts.ATTR_VOICE) == VOICE_ASTROMECH_SHORT:
            slug = generate_hash(message.lower(), 6)

        data = self._r2.generate(slug)

        if options[tts.ATTR_AUDIO_OUTPUT] == "wav":
            output_stream = io.BytesIO()
            output_file = wave.open(output_stream, "wb")
            output_file.setnchannels(1)  # mono
            output_file.setsampwidth(2)  # 16 bits
            output_file.setframerate(22050)  # Hz
            output_file.writeframes(data)
            output_file.close()

            # Read the content of the byte stream into a byte array
            byte_array = output_stream.getvalue()

            return ("wav", byte_array)

        return ("raw", data)