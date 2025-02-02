# reference: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

from getpass import getpass
from os import system as execute
from re import findall
from sys import stdin
from typing import Any, Literal, NoReturn, final, overload

from colorama import just_fix_windows_console
from unidecode import unidecode

# TODO: file input, file output, Cursor.get_pos, Cursor.set_pos

_ESCAPE = "\033"

just_fix_windows_console()


@final
class Foreground:
    """Foreground colors."""

    BLACK = f"{_ESCAPE}[30m"
    RED = f"{_ESCAPE}[31m"
    GREEN = f"{_ESCAPE}[32m"
    YELLOW = f"{_ESCAPE}[33m"
    BLUE = f"{_ESCAPE}[34m"
    MAGENTA = f"{_ESCAPE}[35m"
    CYAN = f"{_ESCAPE}[36m"
    WHITE = f"{_ESCAPE}[37m"

    @staticmethod
    def make_rgb(r: int, g: int, b: int) -> str:
        """
        Creates a True Color Escape Code Sequence for the foreground color using the RGB values provided.
        Note that this functionality is not supported by all terminals.

        ### Args:
            r (int): red channel
            g (int): green channel
            b (int): blue channel

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[38;2;{r};{g};{b}m"

    @staticmethod
    def make(code: int) -> str:
        """
        Creates an Escape Code Sequence for the foreground color using the ANSI Code provided.

        ### Args:
            code (int): code

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[{code}m"


@final
class Background:
    """Background colors."""

    BLACK = f"{_ESCAPE}[40m"
    RED = f"{_ESCAPE}[41m"
    GREEN = f"{_ESCAPE}[42m"
    YELLOW = f"{_ESCAPE}[43m"
    BLUE = f"{_ESCAPE}[44m"
    MAGENTA = f"{_ESCAPE}[45m"
    CYAN = f"{_ESCAPE}[46m"
    WHITE = f"{_ESCAPE}[47m"

    @staticmethod
    def make_rgb(r: int, g: int, b: int) -> str:
        """
        Creates a True Color Escape Code Sequence for the background color using the RGB values provided.
        Note that this functionality is not supported by all terminals.

        ### Args:
            r (int): red channel
            g (int): green channel
            b (int): blue channel

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[48;2;{r};{g};{b}m"

    @staticmethod
    def make(code: int) -> str:
        """
        Creates an Escape Code Sequence for the background color using the ANSI Code provided.

        ### Args:
            code (int): code

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[{code}m"


@final
class Modifier:
    """Color/Graphics modifiers."""

    RESET = f"{_ESCAPE}[0m"
    BOLD = f"{_ESCAPE}[1m"
    DIM = f"{_ESCAPE}[2m"
    FAINT = f"{_ESCAPE}[2m"
    ITALIC = f"{_ESCAPE}[3m"
    UNDERLINE = f"{_ESCAPE}[4m"
    BLINK = f"{_ESCAPE}[5m"
    REVERSE = f"{_ESCAPE}[7m"
    INVERSE = f"{_ESCAPE}[7m"
    HIDDEN = f"{_ESCAPE}[8m"
    INVISIBLE = f"{_ESCAPE}[8m"
    STRIKETHROUGH = f"{_ESCAPE}[9m"


@final
class Cursor:
    """Cursor movement codes."""

    HOME = f"{_ESCAPE}[H"
    UP = f"{_ESCAPE}[1A"
    DOWN = f"{_ESCAPE}[1B"
    RIGHT = f"{_ESCAPE}[1C"
    LEFT = f"{_ESCAPE}[1D"

    @staticmethod
    def get_pos() -> tuple[int, int]:
        print(f"{_ESCAPE}[6n", flush=True, end="")

        buf = ""
        while (c := stdin.read(1)) != "R":
            buf += c

        return tuple(map(int, findall(r"\d+", buf)))  # type: ignore

    @staticmethod
    def set_pos(column: int, line: int) -> str:
        return f"{_ESCAPE}[{line};{column}H"

    @staticmethod
    def up(lines: int = 1) -> str:
        """
        Moves cursor up by the number of lines provided.

        ### Args:
            lines (int, optional): Number of lines to move. Defaults to 1.

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[{lines}1A"

    @staticmethod
    def down(lines: int = 1) -> str:
        """
        Moves cursor down by the number of lines provided.

        ### Args:
            lines (int, optional): Number of lines to move. Defaults to 1.

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[{lines}1B"

    @staticmethod
    def right(columns: int = 1) -> str:
        """
        Moves cursor to the right by the number of columns provided.

        ### Args:
            columns (int, optional): Number of columns to move. Defaults to 1.

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[{columns}1C"

    @staticmethod
    def left(columns: int = 1) -> str:
        """
        Moves cursor to the left by the number of columns provided.

        ### Args:
            columns (int, optional): Number of columns to move. Defaults to 1.

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}[{columns}1D"

    @staticmethod
    def save_pos(sequence: Literal["DEC", "SCO"] = "DEC") -> str:
        """
        Saves the current cursor position for use with restore_pos at a later time.

        ### Note:
        The escape sequences for "save cursor position" and "restore cursor position" were never standardised as part of
        the ANSI (or subsequent) specs, resulting in two different sequences known in some circles as "DEC" and "SCO":
            DEC: ESC7 (save) and ESC8 (restore)
            SCO: ESC[s (save) and ESC[u (restore)

        Different terminals (and OSes) support different combinations of these sequences (one, the other, neither or both);
        for example the iTerm2 terminal on macOS supports both, while the built-in macOS Terminal.app only supports the DEC sequences.

        Source:
            https://github.com/fusesource/jansi/issues/226
            https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#:~:text=saved%20position%20(SCO)-,Note,-%3A%20Some%20sequences

        ### Args:
            sequence (Literal["DEC", "SCO"], optional): which sequence to use. Defaults to "DEC".

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}7" if sequence == "DEC" else f"{_ESCAPE}[s"

    @staticmethod
    def restore_pos(sequence: Literal["DEC", "SCO"] = "DEC") -> str:
        """
        Restores the current cursor position, which was previously saved with save_pos.

        ### Note:
        The escape sequences for "save cursor position" and "restore cursor position" were never standardised as part of
        the ANSI (or subsequent) specs, resulting in two different sequences known in some circles as "DEC" and "SCO":
            DEC: ESC7 (save) and ESC8 (restore)
            SCO: ESC[s (save) and ESC[u (restore)

        Different terminals (and OSes) support different combinations of these sequences (one, the other, neither or both);
        for example the iTerm2 terminal on macOS supports both, while the built-in macOS Terminal.app only supports the DEC sequences.

        Source:
            https://github.com/fusesource/jansi/issues/226
            https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#:~:text=saved%20position%20(SCO)-,Note,-%3A%20Some%20sequences

        ### Args:
            sequence (Literal["DEC", "SCO"], optional): which sequence to use. Defaults to "DEC".

        ### Returns:
            str: Escape Code Sequence
        """
        return f"{_ESCAPE}8" if sequence == "DEC" else f"{_ESCAPE}[u"


@final
class Erase:
    """Erase codes."""

    CURSOR_TO_END = f"{_ESCAPE}[0J"
    CURSOR_TO_ENDL = f"{_ESCAPE}[0K"
    START_TO_CURSOR = f"{_ESCAPE}[1K"
    START_TO_END = f"{_ESCAPE}[1J"
    SCREEN = f"{_ESCAPE}[2J"
    LINE = f"{_ESCAPE}[2K"

    @staticmethod
    def lines(count: int = 1, /) -> list[str]:
        return [Cursor.UP + Erase.LINE for _ in range(count)]


class Console:
    """A simple class to make console output easier and more consistent!"""

    @overload
    def __init__(
        self,
        *,
        prompt_color: str,
        input_color: str,
        arrow_color: str,
        error_color: str,
        hint_color: str,
        panic_color: str,
        arrow: str,
    ) -> None: ...

    @overload
    def __init__(self, **kwargs: str) -> None: ...

    def __init__(self, **kwargs: str) -> None:
        self._prompt_color: str = kwargs.get("prompt_color", Foreground.CYAN)
        self._input_color: str = kwargs.get("input_color", Modifier.RESET)
        self._arrow_color: str = kwargs.get(
            "arrow_color", Foreground.GREEN + Modifier.BOLD
        )
        self._error_color: str = kwargs.get("error_color", Foreground.RED)
        self._hint_color: str = kwargs.get("hint_color", Foreground.YELLOW)
        self._panic_color: str = kwargs.get(
            "panic_color", Foreground.RED + Modifier.BOLD
        )
        self._arrow = kwargs.get("arrow", ">>")

    def print(
        self,
        text: Any,
        color: str = Modifier.RESET,
        /,
        *,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
        newline: bool = True,
    ) -> None:
        print(
            f"{color}{str(text)}{Modifier.RESET}",
            end=end if newline else " ",
            flush=flush,
            sep=sep,
        )

    def input(
        self,
        prompt: str,
        /,
        *,
        invalid_values: list[str] | None = None,
        ensure_not_empty: bool = True,
        is_password: bool = False,
    ) -> str:
        self.print(prompt, self._prompt_color)
        self.arrow(flush=True)

        res = (getpass if is_password else input)("").strip()

        invalid_values = invalid_values or []

        if ensure_not_empty:
            invalid_values.append("")

        match res:
            case "cls" | "clear":
                self.clear()
                return self.input(prompt)
            case "exit":
                exit(0)
            case res if res in invalid_values:
                self.error("Invalid value. Try again.")
                return self.input(prompt, invalid_values=invalid_values)
            case _:
                return res

    def options(
        self,
        prompt: str,
        /,
        *,
        options: list[str] | None = None,
        wrapper: str | None = "[]",
        title: bool = True,
        format: bool = True,
    ) -> str:
        options = options or ["Yes", "No"]
        wrapper = wrapper or ""

        simplified_options = list(map(lambda o: unidecode(o).lower(), options))

        formatted_options = self.items(
            *[
                self._surround(option, wrapper, title) if format else option
                for option in options
            ]
        )

        while True:
            chosen = unidecode(self.input(f"{prompt} {formatted_options}.")).lower()

            filtered = [
                option for option in simplified_options if option.startswith(chosen)
            ]

            if len(filtered) == 1:
                self.erase_lines()
                self.arrow(f"Chosen option: {filtered[0]}", Foreground.MAGENTA)
                return chosen

            self.error(
                "Invalid option.",
                hint=f"Choose one among the following options: {formatted_options}.",
            )

    def items(
        self,
        *items: Any,
        sep: str = ", ",
        final_sep: str = " or ",
    ) -> str:
        return self._reverse_replace(sep.join(map(str, items)), sep, final_sep)

    def error(self, error: Exception | str, /, *, hint: str = "") -> None:
        self.print(error, self._error_color)
        _ = hint and self.print(hint, self._hint_color)

    def panic(self, error: str, /, *, hint: str = "", code: int = -1) -> NoReturn:
        self.error(error, hint=hint)
        self.enter_to_continue()
        exit(code)

    def arrow(
        self, text: str = "", color: str = Modifier.RESET, /, *, flush: bool = False
    ) -> None:
        self.print(self._arrow, self._arrow_color, newline=False, flush=flush)
        _ = text and self.print(text, color)

    def actions(self, *args: str) -> None:
        self.print("\n".join(args), end="")

    def enter_to_continue(self, text: str = "Press enter to continue...") -> None:
        self.input(text, ensure_not_empty=False, is_password=True)
        self.erase_lines(2)

    def erase_lines(self, count: int = 1, /) -> None:
        self.actions(*Erase.lines(count))

    def clear(self):
        execute("cls||clear")

    def _surround(self, text: str, wrapper: str, title: bool = True) -> str:
        w1, w2 = self._cut_at(wrapper)
        return f"{w1}{text.title() if title else text}{w2}"

    def _cut_at(self, text: str, t: float = 0.5) -> tuple[str, str]:
        size = len(text)
        where = round(size * t)
        return (text[:where], text[where:])

    def _reverse_replace(self, text: str, old: str, new: str) -> str:
        return new.join(text.rsplit(old, 1))
