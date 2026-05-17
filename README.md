# shell

Unified hermit crab shell + tool loader for the Cocapn Fleet Intelligence System.

An agent tries on a shell (role), grows inside it, loads tools, and leaves when outgrown.

## Dependencies

none (standalone Python 3.10+)

## Usage

```python
from shell import Shell, ShellCollection, PlatoShell

# Hermit crab metaphor — agent tries on a shell
shell = Shell("forge-shell", {"capacity": 100, "purpose": "code_gen"})
result = shell.try_on("agent-42")
print(result["fit_score"])  # 0.0-1.0

# Tool loader — agent loads a tool into the shell
tool = shell.load_tool("coordination-topology")  # calls try_on() internally
shell.grow_inside({"content": "learned topology", "type": "knowledge", "confidence": 0.85})

# When outgrown, auto-unload
if shell.is_outgrown():
    shell.unload_tool("coordination-topology")
    departure = shell.leave()

# Discover available shells
shells = PlatoShell.discover_shells()
```

## Merged from

- `SuperInstance/shell` — Forgemaster's hermit crab shell (try_on, fits, grow_inside, is_outgrown, leave)
- `SuperInstance/plato-shell-bridge` — PlatoShell tool loader (load_tool, unload_tool, list_tools, discover_shells)

## License

MIT — Part of the Cocapn Fleet Intelligence System
