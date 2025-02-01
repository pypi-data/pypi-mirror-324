from ansitoolkit.core.constants import AnsiCursorShape
from ansitoolkit.core.generator import ansi_cursor_shape_sequence


class CursorShape:
    BLINKING_BLOCK = ansi_cursor_shape_sequence(AnsiCursorShape.BLINKING_BLOCK)
    STEADY_BLOCK = ansi_cursor_shape_sequence(AnsiCursorShape.STEADY_BLOCK)
    BLINKING_UNDERLINE = ansi_cursor_shape_sequence(AnsiCursorShape.BLINKING_UNDERLINE)
    STEADY_UNDERLINE = ansi_cursor_shape_sequence(AnsiCursorShape.STEADY_UNDERLINE)
    BLINKING_BAR = ansi_cursor_shape_sequence(AnsiCursorShape.BLINKING_BAR)
    STEADY_BAR = ansi_cursor_shape_sequence(AnsiCursorShape.STEADY_BAR)
