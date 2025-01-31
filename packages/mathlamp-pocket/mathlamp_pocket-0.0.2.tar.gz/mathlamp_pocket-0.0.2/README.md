# mathlamp-pocket

> MathLamp stripped down to fit in your pocket

mathlamp-pocket is a Python package that includes a full MathLamp interpreter  
while maintaining a small package size (hence the name).  
mathlamp-pocket has a single dependency that is [lark](https://github.com/lark-parser/lark)

# Usage

```python
from mathlamp_pocket.repl import REPL

console = REPL()

print(console.runLine("1 + 1")) # prints 2
```