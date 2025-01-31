from yta_audio.voice.generation.voices import NarrationVoice
from yta_general_utils.constants import Language
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union
from gtts import gTTS


class GoogleNarrationLanguage(Enum):
    """
    The google narration languages accepted by their
    API
    """

    SPANISH = 'es'
    ENGLISH = 'en'

    @staticmethod
    def from_general_language(language: Language) -> 'GoogleNarrationLanguage':
        """
        Turn a general 'language' instance into a Google
        narration language instance.
        """
        return {
            Language.DEFAULT: GoogleNarrationLanguage.SPANISH,
            Language.SPANISH: GoogleNarrationLanguage.SPANISH,
            Language.ENGLISH: GoogleNarrationLanguage.ENGLISH,
        }[Language.to_enum(language)]

class GoogleTld(Enum):

    SPANISH_MEXICO = 'com.mx'
    SPANISH_SPAIN = 'es'
    SPANISH_US = 'us'

    @staticmethod
    def from_google_language(language: GoogleNarrationLanguage) -> 'GoogleTld':
        """
        Turn the Google narration 'language' into the
        corresponding Google TLD.
        """
        return {
            GoogleNarrationLanguage.SPANISH: GoogleTld.SPANISH_SPAIN,
            # TODO: Change this
            GoogleNarrationLanguage.ENGLISH:  GoogleTld.SPANISH_US,
        }[GoogleNarrationLanguage.to_enum(language)]

class GoogleNarrationVoice(NarrationVoice):
    """
    Voice instance to be used when narrating with
    Google engine.
    """

    def validate_and_process(
        self,
        name: str,
        emotion: str,
        speed: float,
        pitch: float,
        language: Language
    ):
        super().validate_and_process(name, emotion, speed, pitch, language)

        language = Language.to_enum(language).value

        # Speed must be above or below 100

        return name, emotion, speed, pitch, language
        
    @staticmethod
    def default():
        return GoogleNarrationVoice('', '', 130, 1.0, Language.DEFAULT)

VOICE_NAME_OPTIONS = [None]
LANGUAGE_OPTIONS = [
    Language.SPANISH,
    Language.ENGLISH,
    Language.DEFAULT
]

def narrate(
    text: str,
    voice: GoogleNarrationVoice = GoogleNarrationVoice.default(),
    output_filename: Union[str, None] = None
):
    """
    Creates an audio narration of the provided 'text' with the Google voice and stores it
    as 'output_filename'. This will use the provided 'language' language for the narration.
    """
    if not output_filename:
        return None
    
    slow_speed = voice.speed < 100

    language = GoogleNarrationLanguage.from_general_language(voice.language).value
    tld = GoogleTld.from_google_language(language).value
    
    # TODO: Check valid language tag in this table (https://en.wikipedia.org/wiki/IETF_language_tag)
    # TODO: Use this library for languages (https://pypi.org/project/langcodes/)
    # TODO: Here we have the languages and tlds (https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang)
    tts = gTTS(text, lang = language, tld = tld, slow = slow_speed)
    tts.save(output_filename)

    return output_filename