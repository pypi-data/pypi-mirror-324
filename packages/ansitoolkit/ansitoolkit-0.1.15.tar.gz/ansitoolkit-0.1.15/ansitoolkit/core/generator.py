from .constants import (
    Ansi256ColorSelector,
    AnsiColor,
    AnsiColorSelector,
    AnsiCursorMovement,
    AnsiCursorShape,
    AnsiDeviceStatus,
    AnsiEffect,
    AnsiEffectSelector,
    AnsiGraphicsAndCharacterSets,
    AnsiKeyboardAndInputModes,
    AnsiRgbColorSelector,
    AnsiScreenControl,
    AnsiScrollingRegion,
    AsciiEscapeCode,
)


def control_sequence_inducer(ascii_escape_code: AsciiEscapeCode) -> str:
    """Control Sequence Inducer (CSI) marks the beginning of a control sequence, e.g. "\\u1b[" in "\\u1b[31m"."""
    return f"{ascii_escape_code}["


def ansi_standard_color_sequence(
    selector: AnsiColorSelector | AnsiEffectSelector,
    value: AnsiColor | AnsiEffect,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate standard ANSI color sequence, e.g. "\\u1b[31m"."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{selector}{value}m"


def ansi_rgb_color_sequence(
    selector: AnsiRgbColorSelector,
    r: int,
    g: int,
    b: int,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate RGB ANSI color sequence, e.g. "\\u1b[38;2;255;100;50m"."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{selector};{r};{g};{b}m"


def ansi_256_color_sequence(
    selector: Ansi256ColorSelector, color_index: int, ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL
) -> str:
    """Generate an ANSI escape sequence for 256-color mode."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{selector};{color_index}m"


def ansi_effect_sequence(
    effect: AnsiEffect,
    selector: AnsiEffectSelector,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate ANSI effect sequence, e.g. "\\u1b[1m" for bold."""
    csi = control_sequence_inducer(ascii_escape_code)
    if selector == AnsiEffectSelector.ON:
        return f"{csi}{effect.value}m"
    elif selector == AnsiEffectSelector.OFF:
        return f"{csi}{effect.value + 20}m"


def ansi_cursor_movement_sequence(
    movement: AnsiCursorMovement,
    count: int,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate ANSI cursor movement sequence, e.g. "\\u1b[5A" for moving up 5 lines."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{count}{movement.value}"


def ansi_screen_control_sequence(
    control: AnsiScreenControl,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate ANSI screen control sequence, e.g. "\\u1b[2J" for clearing the screen."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{control.value}"


def ansi_scrolling_region_sequence(
    top: int = 0,
    bottom: int = 0,
    action: AnsiScrollingRegion = AnsiScrollingRegion.SET_SCROLLING_REGION,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate ANSI scrolling region sequence, e.g. "\\u1b[5;20r"."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{top};{bottom}{action.value}"


def ansi_device_status_sequence(
    status: AnsiDeviceStatus,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate ANSI device status sequence, e.g. "\\u1b[5n" for device status report."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{status.value}"


def ansi_graphics_and_character_set_sequence(
    graphics: AnsiGraphicsAndCharacterSets,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate ANSI graphics and character set sequence, e.g. "\\u1b[0m" for standard mode."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{graphics.value}"


def ansi_keyboard_and_input_mode_sequence(
    mode: AnsiKeyboardAndInputModes,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate ANSI keyboard and input mode sequence, e.g. "\\u1b[?25h" for enabling cursor visibility."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{mode.value}"

def ansi_cursor_shape_sequence(
    shape: AnsiCursorShape,
    ascii_escape_code: AsciiEscapeCode = AsciiEscapeCode.OCTAL,
) -> str:
    """Generate an ANSI sequence for setting the cursor shape, e.g. "\\u1b[1 q" for a blinking block cursor."""
    csi = control_sequence_inducer(ascii_escape_code)
    return f"{csi}{shape}"
