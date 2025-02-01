from ansitoolkit.core.constants import AnsiEffect, AnsiEffectSelector
from ansitoolkit.core.generator import ansi_effect_sequence


class Effects:
    RESET: str = ansi_effect_sequence(AnsiEffect.RESET, AnsiEffectSelector.ON)
    BOLD: str = ansi_effect_sequence(AnsiEffect.BOLD, AnsiEffectSelector.ON)
    DIM: str = ansi_effect_sequence(AnsiEffect.DIM, AnsiEffectSelector.ON)
    ITALIC: str = ansi_effect_sequence(AnsiEffect.ITALIC, AnsiEffectSelector.ON)
    UNDERLINE: str = ansi_effect_sequence(AnsiEffect.UNDERLINE, AnsiEffectSelector.ON)
    SLOW_BLINK: str = ansi_effect_sequence(AnsiEffect.SLOW_BLINK, AnsiEffectSelector.ON)
    RAPID_BLINK: str = ansi_effect_sequence(AnsiEffect.RAPID_BLINK, AnsiEffectSelector.ON)
    REVERSE: str = ansi_effect_sequence(AnsiEffect.REVERSE, AnsiEffectSelector.ON)
    HIDE: str = ansi_effect_sequence(AnsiEffect.HIDE, AnsiEffectSelector.ON)
    STRIKETHROUGH: str = ansi_effect_sequence(AnsiEffect.STRIKETHROUGH, AnsiEffectSelector.ON)
    DOUBLE_UNDERLINE: str = ansi_effect_sequence(AnsiEffect.DOUBLE_UNDERLINE, AnsiEffectSelector.ON)
    NORMAL_INTENSITY: str = ansi_effect_sequence(AnsiEffect.NORMAL_INTENSITY, AnsiEffectSelector.ON)
    NOT_ITALIC: str = ansi_effect_sequence(AnsiEffect.NOT_ITALIC, AnsiEffectSelector.ON)
    NOT_UNDERLINED: str = ansi_effect_sequence(AnsiEffect.NOT_UNDERLINED, AnsiEffectSelector.ON)
    BLINK_OFF: str = ansi_effect_sequence(AnsiEffect.BLINK_OFF, AnsiEffectSelector.ON)
    REVERSE_OFF: str = ansi_effect_sequence(AnsiEffect.REVERSE_OFF, AnsiEffectSelector.ON)
    REVEAL: str = ansi_effect_sequence(AnsiEffect.REVEAL, AnsiEffectSelector.ON)
    NOT_STRIKETHROUGH: str = ansi_effect_sequence(AnsiEffect.NOT_STRIKETHROUGH, AnsiEffectSelector.ON)
