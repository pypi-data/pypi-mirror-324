from enum import Enum, unique


class AsciiEscapeCode(Enum):
    """Control Sequence Introducer (CSI) marks the beginning of a control sequence."""

    OCTAL = "\033"
    HEX = "\x1b"
    UNICODE = "\u001b"

    def __str__(self) -> str:
        return str(self.value)


RESET_ALL: str = f"{AsciiEscapeCode.OCTAL}[0m"


@unique
class AnsiColor(Enum):
    """ANSI color palette 0-7 to be mixed with AnsiColorSelector for foreground (30-37), background (40-47) and other combinations."""

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

    def __str__(self) -> str:
        return str(self.value)


@unique
class AnsiColorSelector(Enum):
    """ANSI color selector to be mixed with AnsiColor for foreground (30-37), background (40-47) and other combinations."""

    FOREGROUND = 3
    """Mix with AnsiColor to select foreground 8 colors palette: 30-37, 90-97."""

    BACKGROUND = 4
    """Mix with AnsiColor to select background 8 colors palette: 40-47, 100-107."""

    BRIGHT_FOREGROUND = 9
    """Mix with AnsiColor to select bright foreground 8 colors palette: 90-97."""

    BRIGHT_BACKGROUND = 10
    """Mix with AnsiColor to select bright background 8 colors palette: 100-107."""

    def __str__(self) -> str:
        return str(self.value)


@unique
class AnsiRgbColorSelector(Enum):
    """ANSI RGB color selector to be mixed with values for red, green, blue."""

    FOREGROUND = "38;2"
    """Parameter for RGB foreground color sequence: 38;2;r;g;b."""

    BACKGROUND = "48;2"
    """Parameter for RGB background color sequence: 48;2;r;g;b."""

    def __str__(self) -> str:
        return str(self.value)


@unique
class Ansi256ColorSelector(Enum):
    """ANSI 256-color selector to be mixed with values for the color index."""

    FOREGROUND = "38;5"
    """Parameter for 256-color foreground sequence: 38;5;n, where n is the color index (0-255)."""

    BACKGROUND = "48;5"
    """Parameter for 256-color background sequence: 48;5;n, where n is the color index (0-255)."""

    def __str__(self) -> str:
        return str(self.value)


@unique
class AnsiEffect(Enum):
    """ANSI effect codes to be mixed with effect selector."""

    RESET = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    SLOW_BLINK = 5
    RAPID_BLINK = 6
    REVERSE = 7
    HIDE = 8
    STRIKETHROUGH = 9
    DOUBLE_UNDERLINE = 21
    NORMAL_INTENSITY = 22
    NOT_ITALIC = 23
    NOT_UNDERLINED = 24
    BLINK_OFF = 25
    REVERSE_OFF = 27
    REVEAL = 28
    NOT_STRIKETHROUGH = 29

    def __str__(self) -> str:
        return str(self.value)


@unique
class AnsiEffectSelector(Enum):
    """ANSI effect selector to be mixed with AnsiEffect for on (1-8) or off (21-28)."""

    ON = ""
    """Mix with AnsiEffect to select effects: 1-8, 21-28."""

    OFF = 2
    """Mix with AnsiEffect to select effects: 21-28."""

    def __str__(self) -> str:
        return str(self.value)


@unique
class AnsiCursorMovement(Enum):
    """ANSI cursor movement codes."""

    MOVE_UP = "A"
    MOVE_DOWN = "B"
    MOVE_FORWARD = "C"
    MOVE_BACK = "D"
    MOVE_NEXT_LINE = "E"
    MOVE_PREV_LINE = "F"
    MOVE_COLUMN = "G"
    MOVE_POSITION = "H"
    SAVE_CURSOR_POSITION = "s"
    RESTORE_CURSOR_POSITION = "u"

    def __str__(self) -> str:
        return self.value


@unique
class AnsiScreenControl(Enum):
    """ANSI screen control codes."""

    CLEAR_TO_END_OF_SCREEN = "J"
    CLEAR_TO_START_OF_SCREEN = "1J"
    CLEAR_ENTIRE_SCREEN = "2J"
    CLEAR_TO_END_OF_LINE = "K"
    CLEAR_TO_START_OF_LINE = "1K"
    CLEAR_ENTIRE_LINE = "2K"
    SHOW_CURSOR = "?25h"
    HIDE_CURSOR = "?25l"
    SWITCH_ALTERNATE_SCREEN = "?1049h"
    SWITCH_NORMAL_SCREEN = "?1049l"

    def __str__(self) -> str:
        return self.value


class AnsiScrollingRegion(Enum):
    """ANSI scrolling region codes."""

    SET_SCROLLING_REGION = "r"
    RESET_SCROLLING_REGION = "r"

    def __str__(self) -> str:
        return self.value


@unique
class AnsiDeviceStatus(Enum):
    """ANSI device status codes."""

    DEVICE_STATUS_REPORT = "5n"
    TERMINAL_OK = "0n"
    TERMINAL_MALFUNCTION = "3n"
    CURSOR_POSITION_REPORT = "6n"
    QUERY_DEVICE_ATTRIBUTES = ">p"

    def __str__(self) -> str:
        return self.value


@unique
class AnsiGraphicsAndCharacterSets(Enum):
    """ANSI graphics and character set codes."""

    STANDARD_MODE = "0m"
    ENABLE_LINE_WRAPPING = "?7h"
    DISABLE_LINE_WRAPPING = "?7l"
    SET_CHARACTER_SET_G0 = "11m"
    SET_CHARACTER_SET_G1 = "12m"

    def __str__(self) -> str:
        return self.value


@unique
class AnsiKeyboardAndInputModes(Enum):
    """ANSI keyboard and input mode codes."""

    APPLICATION_KEYPAD_MODE = "?1h"
    NORMAL_KEYPAD_MODE = "?1l"
    ENABLE_CURSOR_VISIBILITY = "?25h"
    DISABLE_CURSOR_VISIBILITY = "?25l"

    def __str__(self) -> str:
        return self.value

@unique
class AnsiCursorShape(Enum):
    """ANSI cursor shape codes."""

    BLINKING_BLOCK = "1 q"
    STEADY_BLOCK = "2 q"
    BLINKING_UNDERLINE = "3 q"
    STEADY_UNDERLINE = "4 q"
    BLINKING_BAR = "5 q"
    STEADY_BAR = "6 q"

    def __str__(self) -> str:
        return self.value
