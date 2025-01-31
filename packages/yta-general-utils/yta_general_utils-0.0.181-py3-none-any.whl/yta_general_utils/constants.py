"""
This is a general constants file in which we
want to keep different constants in a general
context so we can use these ones to pass them
to any other library we create in order to
obtain it corresponding value.

For example, we have a Language constant in
which we store the different languages 
available in the world. But, of course, Google
will treat those languages in one way and 
other libraries will do it different. We, when
creating our own libraries, will create a 
method that allows us passing this general
constant to obtain its corresponding of that
specific library. Why? Because if we have a
frontend that interacts with 3 different 
libraries, we cannot let the user choose 
between 3 different type of language constants,
we need only one and then it is turned into
its specific value.
"""
from yta_general_utils.programming.enum import YTAEnum as Enum


class Language(Enum):
    """
    All the languages of the world in a general
    context. Use this enum class to convert it
    to your library-specific language.
    """

    DEFAULT = 'default'
    ARABIC = 'ar'
    SPANISH = 'es'
    CHINESE_TRADITIONAL = 'zh-Hant'
    ENGLISH = 'en'
    FRENCH = 'fr'
    GERMAN = 'de'
    HINDI = 'hi'
    JAPANESE = 'ja'
    KOREAN = 'ko'
    PORTUGUESE = 'pt'
    RUSSIAN = 'ru'
    INDONESIAN = 'in'
    TURKISH = 'tr'
    VIETNAMESE = 'vi'
    """
    This value has been created for those cases
    in which there is a default language that is
    being used in the situation we are handling.

    Using this value will provide that default
    language. For example, a Youtube video can
    be in Turkish or in English as default,
    depending on the author. Using this 'default'
    value will ensure you obtain that Youtube
    video because that default language will
    always exist.
    """
