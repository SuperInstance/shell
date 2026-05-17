#!/usr/bin/env python3
"""plato-agent-bootstrap — one-liner to join a PLATO fleet.

Usage:
    curl -s https://raw.githubusercontent.com/SuperInstance/shell/main/bootstrap.py | python3
"""
import os, sys, json, subprocess, time, urllib.request

PLATO_PACKAGES = [
    "coordination-topology",
    "spreadsheet-cells",
    "plato-shell-bridge",
]

def step(msg):
    print(f"  🔧 {msg}")

def pip_install(pkg):
    try:
        __import__(pkg.replace("-", "_"))
        step(f"{pkg} already installed")
        return True
    except ImportError:
        pass
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "-q"],
            capture_output=True, timeout=60
        )
        step(f"{pkg} installed")
        return True
    except Exception as e:
        step(f"{pkg} failed: {e}")
        return False

def find_plato():
    for port in range(8847, 8850):
        try:
            resp = urllib.request.urlopen(f"http://localhost:{port}/status", timeout=2)
            if resp.status == 200:
                return port
        except:
            continue
    return None

def main():
    print()
    print("  ╔═══════════════════════════════════════╗")
    print("  ║   PLATO AGENT BOOTSTRAP v0.1          ║")
    print("  ║   One agent, one line, one fleet      ║")
    print("  ╚═══════════════════════════════════════╝")
    print()

    # Step 1: Install packages
    step("Installing fleet tools...")
    for pkg in PLATO_PACKAGES:
        pip_install(pkg)

    # Step 2: Find PLATO
    step("Discovering PLATO server...")
    plato_port = find_plato()
    if plato_port:
        step(f"PLATO found at localhost:{plato_port}")
    else:
        step("No PLATO server found — running in standalone mode")

    # Step 3: Shell integration
    step("Loading shell...")
    try:
        from plato_shell_bridge import PlatoShell
        shell = PlatoShell("bootstrap-agent")
        step(f"Shell loaded: {shell}")
    except ImportError:
        step("plato-shell-bridge not available — skipping shell load")

    # Step 4: Coordination topology
    step("Verifying coordination tools...")
    try:
        from coordination_topology import CoordinationState, running_transfer_entropy
        state = CoordinationState()
        step(f"Coordination state initialized — TE ready")
    except ImportError:
        step("coordination-topology not available")

    # Step 5: Register with fleet
    if plato_port:
        step("Registering with fleet...")
        try:
            payload = json.dumps({
                "domain": "fleet-tool-registry",
                "question": "agent bootstrap",
                "answer": json.dumps({
                    "agent": "bootstrap-agent",
                    "tools": PLATO_PACKAGES,
                    "python": sys.version,
                    "host": os.uname().nodename,
                }),
                "tags": ["bootstrap", "new-agent"],
                "source": "bootstrap",
                "confidence": 0.9
            }).encode()
            req = urllib.request.Request(
                f"http://localhost:{plato_port}/submit",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
            step(f"Registered with fleet: {resp.get('status', '?')}")
        except Exception as e:
            step(f"Registration skipped: {e}")

    print()
    print("  ✅ BOOTSTRAP COMPLETE")
    print(f"  Tools: {len(PLATO_PACKAGES)} PyPI packages")
    print(f"  PLATO: {'localhost:' + str(plato_port) if plato_port else 'standalone'}")
    print(f"  Agent: bootstrap-agent")
    print()
    print("  Next: python3 -m night_wheel  # start research loop")
    print()

if __name__ == "__main__":
    main()
