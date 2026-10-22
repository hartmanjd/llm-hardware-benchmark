"""The localbench terminal command."""

# Everything a person types in the terminal ("localbench info", "localbench monitor", and later
# "run", "doctor" and "results") starts here. This file only handles the conversation with the
# person: it asks other modules for the actual work (hardware.py for the computer's details,
# gpu_monitor.py for GPU readings) and shows the answers.

import time

import typer
from rich.console import Console
from rich.table import Table

from localbench import __version__
from localbench.gpu_monitor import GpuMonitor
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


# "localbench monitor": watches the GPU for a few seconds and shows what it used, the same
# measurements that will be taken while every benchmark runs. Handy for seeing the readings work,
# or for watching the GPU while something else (a game, a model) is running.


@app.command()
def monitor(
    seconds: float = typer.Option(10, help="How long to watch the GPU."),
    gpu: int = typer.Option(0, help="Which GPU to watch, by its # from 'localbench info'."),
) -> None:
    """Watch the GPU's power, memory, load and temperature."""
    console.print(f"Watching GPU {gpu} for {seconds:g} seconds...")
    with GpuMonitor(gpu_index=gpu) as gpu_monitor:
        time.sleep(seconds)
    summary = gpu_monitor.summary()

    if summary is None:
        console.print("No GPU readings (is an NVIDIA GPU and nvidia-smi available?).")
        raise typer.Exit(1)

    table = Table(title=f"GPU {gpu} over {summary.duration_s:.1f} s", show_header=False)
    if summary.avg_power_w is not None:
        table.add_row(
            "Power", f"{summary.avg_power_w:.0f} W avg, {summary.peak_power_w:.0f} W peak"
        )
    table.add_row(
        "VRAM",
        f"{summary.peak_vram_gb:.1f} GB peak ({summary.added_vram_gb:.1f} GB more than at start)",
    )
    table.add_row("Load", f"{summary.avg_utilization_pct:.0f}% avg")
    table.add_row("Temperature", f"{summary.peak_temperature_c:.0f} °C peak")
    if summary.energy_wh is not None:
        table.add_row("Energy", f"{summary.energy_wh:.3f} Wh")
    else:
        table.add_row("Energy", "unknown (this GPU doesn't report power)")
    console.print(table)
