from ansitoolkit.core.constants import Ansi256ColorSelector, AnsiColor, AnsiColorSelector, AnsiRgbColorSelector
from ansitoolkit.core.generator import ansi_rgb_color_sequence, ansi_standard_color_sequence


class Colors:
    FG_BLACK = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.BLACK)
    FG_RED = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.RED)
    FG_GREEN = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.GREEN)
    FG_YELLOW = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.YELLOW)
    FG_BLUE = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.BLUE)
    FG_MAGENTA = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.MAGENTA)
    FG_CYAN = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.CYAN)
    FG_WHITE = ansi_standard_color_sequence(AnsiColorSelector.FOREGROUND, AnsiColor.WHITE)
    FG_BRIGHT_BLACK = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.BLACK)
    FG_BRIGHT_RED = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.RED)
    FG_BRIGHT_GREEN = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.GREEN)
    FG_BRIGHT_YELLOW = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.YELLOW)
    FG_BRIGHT_BLUE = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.BLUE)
    FG_BRIGHT_MAGENTA = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.MAGENTA)
    FG_BRIGHT_CYAN = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.CYAN)
    FG_BRIGHT_WHITE = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_FOREGROUND, AnsiColor.WHITE)

    BG_BLACK = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.BLACK)
    BG_RED = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.RED)
    BG_GREEN = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.GREEN)
    BG_YELLOW = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.YELLOW)
    BG_BLUE = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.BLUE)
    BG_MAGENTA = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.MAGENTA)
    BG_CYAN = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.CYAN)
    BG_WHITE = ansi_standard_color_sequence(AnsiColorSelector.BACKGROUND, AnsiColor.WHITE)
    BG_BRIGHT_BLACK = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.BLACK)
    BG_BRIGHT_RED = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.RED)
    BG_BRIGHT_GREEN = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.GREEN)
    BG_BRIGHT_YELLOW = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.YELLOW)
    BG_BRIGHT_BLUE = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.BLUE)
    BG_BRIGHT_MAGENTA = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.MAGENTA)
    BG_BRIGHT_CYAN = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.CYAN)
    BG_BRIGHT_WHITE = ansi_standard_color_sequence(AnsiColorSelector.BRIGHT_BACKGROUND, AnsiColor.WHITE)


class RGBColors:
    @staticmethod
    def rgb_foreground(red: int, green: int, blue: int) -> str:
        """Generate RGB foreground color sequence."""
        try:
            if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
                raise ValueError("RGB values must be from 0 to 255.")
            return ansi_rgb_color_sequence(AnsiRgbColorSelector.FOREGROUND, red, green, blue)
        except ValueError as e:
            print(f"ValueError: {e}")
            raise

    @staticmethod
    def rgb_background(red: int, green: int, blue: int) -> str:
        """Generate RGB background color sequence."""
        try:
            if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
                raise ValueError("RGB values must be from 0 to 255.")
            return ansi_rgb_color_sequence(AnsiRgbColorSelector.BACKGROUND, red, green, blue)
        except ValueError as e:
            print(f"ValueError: {e}")
            raise


class Ansi256Colors:
    @staticmethod
    def color_foreground(color_index: int) -> str:
        """Generate 256-color foreground sequence."""
        try:
            if not (0 <= color_index <= 255):
                raise ValueError("Color index must be from 0 to 255.")
            return f"\033[{Ansi256ColorSelector.FOREGROUND};{color_index}m"
        except ValueError as e:
            print(f"ValueError: {e}")
            raise

    @staticmethod
    def color_background(color_index: int) -> str:
        """Generate 256-color background sequence."""
        try:
            if not (0 <= color_index <= 255):
                raise ValueError("Color index must be from 0 to 255.")
            return f"\033[{Ansi256ColorSelector.BACKGROUND};{color_index}m"
        except ValueError as e:
            print(f"ValueError: {e}")
            raise


class HSLColors:
    @staticmethod
    def hsl_to_rgb(hue: float, saturation: float, lightness: float) -> tuple[int, int, int]:
        """Convert HSL to RGB without using the colorsys module."""
        try:
            if not (0 <= hue <= 360 and 0 <= saturation <= 1 and 0 <= lightness <= 1):
                raise ValueError("HSL values must be H: 0-360, S: 0-1, L: 0-1.")

            c = (1 - abs(2 * lightness - 1)) * saturation
            x = c * (1 - abs((hue / 60) % 2 - 1))
            m = lightness - c / 2

            if 0 <= hue < 60:
                red, green, blue = c, x, 0
            elif 60 <= hue < 120:
                red, green, blue = x, c, 0
            elif 120 <= hue < 180:
                red, green, blue = 0, c, x
            elif 180 <= hue < 240:
                red, green, blue = 0, x, c
            elif 240 <= hue < 300:
                red, green, blue = x, 0, c
            else:
                red, green, blue = c, 0, x

            red, green, blue = int((red + m) * 255), int((green + m) * 255), int((blue + m) * 255)
            return red, green, blue
        except ValueError as e:
            print(f"ValueError: {e}")
            raise

    @staticmethod
    def hsl_foreground(hue: float, saturation: float, lightness: float) -> str:
        """Generate HSL foreground color sequence."""
        red, green, blue = HSLColors.hsl_to_rgb(hue, saturation, lightness)
        return RGBColors.rgb_foreground(red, green, blue)

    @staticmethod
    def hsl_background(hue: float, saturation: float, lightness: float) -> str:
        """Generate HSL background color sequence."""
        red, green, blue = HSLColors.hsl_to_rgb(hue, saturation, lightness)
        return RGBColors.rgb_background(red, green, blue)


class HexColors:
    @staticmethod
    def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
        """Convert hex color code to RGB."""
        try:
            hex_code = hex_code.lstrip("#")
            if len(hex_code) != 6:
                raise ValueError("Hex code must be 6 characters long.")
            red, green, blue = tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
            return red, green, blue
        except ValueError as e:
            print(f"ValueError: {e}")
            raise

    @staticmethod
    def hex_foreground(hex_code: str) -> str:
        """Generate hex foreground color sequence."""
        red, green, blue = HexColors.hex_to_rgb(hex_code)
        return RGBColors.rgb_foreground(red, green, blue)

    @staticmethod
    def hex_background(hex_code: str) -> str:
        """Generate hex background color sequence."""
        red, green, blue = HexColors.hex_to_rgb(hex_code)
        return RGBColors.rgb_background(red, green, blue)
