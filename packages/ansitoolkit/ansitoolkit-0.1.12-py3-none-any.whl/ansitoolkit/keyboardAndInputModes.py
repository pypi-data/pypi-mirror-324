from ansitoolkit.core.constants import AnsiKeyboardAndInputModes
from ansitoolkit.core.generator import ansi_keyboard_and_input_mode_sequence


class KeyboardAndInputModes:
    APPLICATION_KEYPAD_MODE = ansi_keyboard_and_input_mode_sequence(AnsiKeyboardAndInputModes.APPLICATION_KEYPAD_MODE)
    NORMAL_KEYPAD_MODE = ansi_keyboard_and_input_mode_sequence(AnsiKeyboardAndInputModes.NORMAL_KEYPAD_MODE)
    ENABLE_CURSOR_VISIBILITY = ansi_keyboard_and_input_mode_sequence(AnsiKeyboardAndInputModes.ENABLE_CURSOR_VISIBILITY)
    DISABLE_CURSOR_VISIBILITY = ansi_keyboard_and_input_mode_sequence(
        AnsiKeyboardAndInputModes.DISABLE_CURSOR_VISIBILITY
    )
