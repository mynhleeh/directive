import sys
from pathlib import Path
import importlib.util

cli_dir = Path(__file__).resolve().parent

if "directive_cli" not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        "directive_cli",
        cli_dir / "__init__.py",
        submodule_search_locations=[str(cli_dir)],
    )
    if spec and spec.loader:
        mod = importlib.util.module_from_spec(spec)
        sys.modules["directive_cli"] = mod
        spec.loader.exec_module(mod)
