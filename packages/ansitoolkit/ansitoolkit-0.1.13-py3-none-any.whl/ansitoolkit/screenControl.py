from ansitoolkit.core.constants import AnsiScreenControl
from ansitoolkit.core.generator import ansi_screen_control_sequence


class ScreenControl:
    CLEAR_TO_END_OF_SCREEN = ansi_screen_control_sequence(AnsiScreenControl.CLEAR_TO_END_OF_SCREEN)
    CLEAR_TO_START_OF_SCREEN = ansi_screen_control_sequence(AnsiScreenControl.CLEAR_TO_START_OF_SCREEN)
    CLEAR_ENTIRE_SCREEN = ansi_screen_control_sequence(AnsiScreenControl.CLEAR_ENTIRE_SCREEN)
    CLEAR_ENTIRE_SCREEN = ansi_screen_control_sequence(AnsiScreenControl.CLEAR_ENTIRE_SCREEN)
    CLEAR_TO_END_OF_LINE = ansi_screen_control_sequence(AnsiScreenControl.CLEAR_TO_END_OF_LINE)
    CLEAR_TO_START_OF_LINE = ansi_screen_control_sequence(AnsiScreenControl.CLEAR_TO_START_OF_LINE)
    CLEAR_ENTIRE_LINE = ansi_screen_control_sequence(AnsiScreenControl.CLEAR_ENTIRE_LINE)
    SHOW_CURSOR = ansi_screen_control_sequence(AnsiScreenControl.SHOW_CURSOR)
    HIDE_CURSOR = ansi_screen_control_sequence(AnsiScreenControl.HIDE_CURSOR)
    SWITCH_ALTERNATE_SCREEN = ansi_screen_control_sequence(AnsiScreenControl.SWITCH_ALTERNATE_SCREEN)
    SWITCH_NORMAL_SCREEN = ansi_screen_control_sequence(AnsiScreenControl.SWITCH_NORMAL_SCREEN)
