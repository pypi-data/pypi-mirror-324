from ansitoolkit.core.constants import AnsiScrollingRegion
from ansitoolkit.core.generator import ansi_scrolling_region_sequence


class ScrollingRegion:
    @staticmethod
    def set_scrolling_region(top: int, bottom: int) -> str:
        return ansi_scrolling_region_sequence(top, bottom, AnsiScrollingRegion.SET_SCROLLING_REGION)

    RESET_SCROLLING_REGION = ansi_scrolling_region_sequence(0, 0, AnsiScrollingRegion.RESET_SCROLLING_REGION)
