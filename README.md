# shell

Shell + ShellCollection + PrivateBreeding + OutgrowMetaSkill — hermit crab finding/outgrowing shells

## Dependencies

none (standalone)

## Usage

```python
from core.shell import ...
```

## Shell Loading

This tool can be loaded into any PLATO shell environment:

```python
# Neo loads this tool from the weapon rack
from plato_shell_bridge import PlatoShell
shell = PlatoShell("agent-shell")
shell.load_tool("shell")
```

## Tests

```bash
python3 -m pytest tests/test_shell.py -v
```

## License

MIT — Part of the Cocapn Fleet Intelligence System
