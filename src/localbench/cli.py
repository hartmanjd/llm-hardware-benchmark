"""The localbench terminal command."""

# Everything a person types in the terminal ("localbench info", and later "run", "doctor" and
# "results") starts here. This file only handles the conversation with the person: it asks other
# modules for the actual work (hardware.py for the computer's details) and shows the answers.

import typer
from rich.console import Console
from rich.table import Table

from localbench import __version__
from localbench.hardware import detect_hardware

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.callback()
def main() -> None:
    """Benchmark local LLMs on your own hardware."""


# "localbench info": shows what localbench can see about this computer, the same details that
# will be saved with every benchmark run.


@app.command()
def info() -> None:
    """Show this computer's OS, CPU, RAM and GPUs."""
    hw = detect_hardware()

    system = Table(title=f"localbench {__version__}", show_header=False)
    system.add_row("OS", hw.os + (" (WSL)" if hw.is_wsl else ""))
    system.add_row("CPU", hw.cpu_name or "unknown")
    system.add_row("CPU threads", str(hw.cpu_threads or "unknown"))
    system.add_row("RAM", f"{hw.ram_gb} GB" if hw.ram_gb else "unknown")
    console.print(system)

    if not hw.gpus:
        console.print("No NVIDIA GPU found (nvidia-smi not available).")
        return

    gpus = Table(title="GPUs")
    gpus.add_column("#")
    gpus.add_column("Name")
    gpus.add_column("VRAM")
    gpus.add_column("Driver")
    for gpu in hw.gpus:
        gpus.add_row(str(gpu.index), gpu.name, f"{gpu.vram_gb} GB", gpu.driver_version)
    console.print(gpus)
