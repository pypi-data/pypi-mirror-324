"""Wrapper class for the MathLamp REPL."""
import lark

from mathlamp_pocket.base import calc

class REPL:
    def run_line(self,code:str) -> str:
        """
        Runs a line in REPL.

        Args:
            code (str): The code to be executed.

        Returns:
            The output of the REPL. if `code` it doesn't output, (Ex: Variable assignments) an empty string will be returned instead
        """
        try:
            return calc(code)
        except (lark.UnexpectedCharacters, lark.UnexpectedEOF) as e:
            raise Exception(e)

    def run_code_lines(self,code:str) -> list:
        """
        Runs multiple lines from a multiline string

        Args:
            code (str): A multiline string, which each line represents a statement that will be run individually in the REPL, same as running `run_line()` for each line

        Returns:
            list: List of each statement's output, if a statement doesn't output, (Ex: Variable assignments) they will be missing in the list
        """
        output = []
        code_list = code.splitlines()
        for line in code_list:
            line_clean = line.rstrip()
            if not line_clean:
                continue
            try:
                output.append(calc(line_clean))
            except (lark.UnexpectedCharacters, lark.UnexpectedEOF) as e:
                raise Exception(e)
        return output