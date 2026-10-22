# Tests for the terminal command. They run "localbench info" the way a person would, but with
# made-up hardware, so they check what gets shown without depending on the machine running them.

from typer.testing import CliRunner

from localbench import cli
from localbench.hardware import GpuInfo, HardwareInfo

runner = CliRunner()

FAKE_PC = HardwareInfo(
    os="Linux 6.6.87.2-microsoft-standard-WSL2",
    is_wsl=True,
    cpu_name="AMD Ryzen 7 7800X3D 8-Core Processor",
    cpu_threads=16,
    ram_gb=32.0,
    gpus=[
        GpuInfo(
            index=0, name="NVIDIA GeForce RTX 4070 Ti SUPER", vram_gb=16.0, driver_version="581.57"
        )
    ],
)


def test_info_shows_the_hardware(monkeypatch):
    monkeypatch.setattr(cli, "detect_hardware", lambda: FAKE_PC)
    result = runner.invoke(cli.app, ["info"])
    assert result.exit_code == 0
    assert "RTX 4070 Ti SUPER" in result.output
    assert "(WSL)" in result.output
    assert "32.0 GB" in result.output


def test_info_without_a_gpu(monkeypatch):
    monkeypatch.setattr(cli, "detect_hardware", lambda: FAKE_PC.model_copy(update={"gpus": []}))
    result = runner.invoke(cli.app, ["info"])
    assert result.exit_code == 0
    assert "No NVIDIA GPU found" in result.output
