import lark

from mathlamp_pocket.base import calc, out_results

class CodeRunner:
    def run_code_lines(self, code:str) -> list:
        """
        Runs multiple lines from a multiline string.

        Args:
            code (str): A multiline string, which each line represents a statement that will be run at the same time by the runner, like a `.lmp` file.

        Returns:
            list: List of each MathLamp `out[]` prints
        """
        code_list = code.splitlines()
        for line in code_list:
            line_clean = line.rstrip()
            if not line_clean:
                continue
            try:
                calc(line_clean)
            except (lark.UnexpectedCharacters, lark.UnexpectedEOF) as e:
                raise Exception(e)
        return out_results