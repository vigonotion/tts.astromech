import io
from typing import Any
from homeassistant.components import tts
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

import re
import random
import string
import wave

from .const import DOMAIN
from ttastromech import TTAstromech


def replace_non_alpha_chars(text):
    """Replace invalid characters with a random lowercase ascii letter"""

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
        self._r2 = TTAstromech()

        self._attr_name = "Astromech"
        self._attr_unique_id = "astromech-tts"

    @property
    def supported_languages(self) -> list[str]:
        return ["en", "de", "pl", "es", "it", "fr", "pt", "hi"]  # TODO return all

    @property
    def default_language(self) -> str:
        return "en"

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [tts.ATTR_VOICE]

    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any] | None = None
    ) -> tts.TtsAudioType:
        """Load tts audio file from the engine."""
        slug = replace_non_alpha_chars(message.lower())
        data = self._r2.generate(slug)

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
