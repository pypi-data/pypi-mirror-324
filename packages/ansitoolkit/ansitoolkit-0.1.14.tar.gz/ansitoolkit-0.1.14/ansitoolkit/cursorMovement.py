from ansitoolkit.core.constants import AnsiCursorMovement, AsciiEscapeCode
from ansitoolkit.core.generator import ansi_cursor_movement_sequence, control_sequence_inducer


class CursorMovement:
    @staticmethod
    def move_up(count: int) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_UP, count)

    @staticmethod
    def move_down(count: int) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_DOWN, count)

    @staticmethod
    def move_forward(count: int) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_FORWARD, count)

    @staticmethod
    def move_back(count: int) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_BACK, count)

    @staticmethod
    def move_next_line(count: int) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_NEXT_LINE, count)

    @staticmethod
    def move_prev_line(count: int) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_PREV_LINE, count)

    @staticmethod
    def move_column(count: int) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_COLUMN, count)

    @staticmethod
    def move_position(row: int = 0, col: int = 0) -> str:
        return ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_POSITION, f"{row};{col}")

    RESET_POSITION = f"{ansi_cursor_movement_sequence(AnsiCursorMovement.MOVE_POSITION, "")}"
    SAVE_POSITION = f"{control_sequence_inducer(AsciiEscapeCode.OCTAL)}{AnsiCursorMovement.SAVE_CURSOR_POSITION}"
    RESTORE_POSITION = f"{control_sequence_inducer(AsciiEscapeCode.OCTAL)}{AnsiCursorMovement.RESTORE_CURSOR_POSITION}"
