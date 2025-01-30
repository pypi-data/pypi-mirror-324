__VER__ = '7.6.21'


if __name__ == "__main__":
  with open("pyproject.toml", "rt") as fd:
    new_lines = []
    lines = fd.readlines()
    for line in lines:
      if "version" in line:
        line = f'version = "{__VER__}"\n'
      new_lines.append(line)

  with open("pyproject.toml", "wt") as fd:
    fd.writelines(new_lines)
