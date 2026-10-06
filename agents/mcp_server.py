"""Minimal read/validate/experiment MCP server for GitHub2VLPI.

Open repository control plane only. No network, credentials, proprietary PDK,
or fabrication access is provided by this server.
"""

import json
import os
import subprocess
from pathlib import Path
import sys

ROOT = Path(os.environ.get("EIS_OPEN_VLPI_ROOT", Path(__file__).resolve().parents[1]))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml
from jsonschema import Draft202012Validator
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EIS-VLPI-MCP")


def load_yaml(relpath):
    path = ROOT / relpath
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@mcp.tool()
def vlpi_discover() -> dict:
    return load_yaml("agents/agent-manifest.yaml")


@mcp.tool()
def vlpi_pdk_list() -> dict:
    """Return an explicitly object-shaped PDK environment collection over MCP."""
    return {"environments": load_yaml("verification/pdk/VLPI-PDK-001.yaml")["experiment"]["environments"]}


@mcp.tool()
def vlpi_pdk_capabilities(pdk_path: str) -> dict:
    return load_yaml(pdk_path)


@mcp.tool()
def vlpi_validate_compatibility(result: dict) -> dict:
    schema = load_yaml("schema/pdk/pdk-compatibility.schema.yaml")
    errors = sorted(Draft202012Validator(schema).iter_errors(result), key=lambda e: list(e.path))
    return {"valid": not errors, "errors": [e.message for e in errors]}


@mcp.tool()
def vlpi_run_pdk001() -> dict:
    """Run only the repository-contained VLPI-PDK-001 capability/reference experiment."""
    proc = subprocess.run(
        ["python", "tests/vlpi-pdk-001/test_pdk_matrix.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "experiment": "VLPI-PDK-001",
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "physicalValidation": False,
    }


@mcp.tool()
def vlpi_run_ru001_reference(a_real: float, a_imag: float, b_real: float, b_imag: float, phase_rad: float = 0.0) -> dict:
    """Run the executable mathematical RU-001 reference transformation."""
    from reference_model.ru001 import residual_field

    result = residual_field(
        complex(a_real, a_imag),
        complex(b_real, b_imag),
        phase_rad,
    )
    return {
        "model": "RU-001-reference",
        "residualReal": result.residual.real,
        "residualImag": result.residual.imag,
        "residualPower": result.residual_power,
        "phaseRad": result.phase_rad,
        "evidenceStatus": "computationally-demonstrated",
        "physicalValidation": False,
    }


if __name__ == "__main__":
    mcp.run()
