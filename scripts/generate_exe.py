#!/usr/bin/env python3.10
import ast
from itertools import chain
from pathlib import Path

INTERNAL_MODULES = ['app', 'constants', 'data', 'main', 'utils']
def remove_internal_imports(module: ast.Module) -> ast.Module:
  def clean(statement):
    # import x, y, z
    if isinstance(statement, ast.Import):
      filtered_names = [name
                        for name in statement.names
                        if name not in INTERNAL_MODULES]
      if filtered_names == []: return None
      return ast.Import(names=filtered_names)
    # from x import a, b, c
    if isinstance(statement, ast.ImportFrom):
      if statement.module in INTERNAL_MODULES:
        return None
      return statement
    return statement
  return ast.Module(
      body=[cleaned
            for statement in module.body
            if (cleaned := clean(statement)) is not None],
      type_ignores=module.type_ignores
    )

def generate_script():
  with open('dev/constants.py') as constants:
    constants_code = ast.parse(constants.read())
  with open('dev/utils.py') as utils:
    utils_code = ast.parse(utils.read())
  with open('dev/data.py') as data:
    data_code = ast.parse(data.read())
  with open('dev/app.py') as app:
    app_code = ast.parse(app.read())
  with open('dev/main.py') as main:
    main_code = ast.parse(main.read())

  def combine(*modules: ast.Module) -> ast.Module:
    return ast.Module(
        body=chain.from_iterable((module.body for module in modules)),
        type_ignores=[] # we are not parsing the types anyway
      )

  all_code = combine(constants_code, utils_code, data_code, app_code, main_code)
  all_code_no_internal_imports = remove_internal_imports(all_code)
  return ast.unparse(all_code_no_internal_imports)


def main():
  if not Path(Path.cwd() / 'scripts/generate_exe.py').exists():
    print('Run `python scripts/generate_exe.py` from the project root.')
    exit()

  with open('todotxtpy/todotxt.py', 'w') as file:
    file.write("#!/bin/python3.10\n\"\"\"Full executable file.\"\"\"\n\n")
    file.write(generate_script())

if __name__ == '__main__':
  main()
