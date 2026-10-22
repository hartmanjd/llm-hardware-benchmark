# localbench

Benchmark local LLMs on your own hardware, and find out which model, quantization and KV cache
setting runs best on your machine.

Each run measures:

| Metric | Meaning |
| --- | --- |
| Prefill tok/s | How fast the model reads your prompt |
| Decode tok/s | How fast it writes the answer |
| TTFT ms | Time to first token: the wait before the answer starts |
| Peak VRAM GB | GPU memory used at the busiest moment |
| Avg / peak W | GPU power draw |
| Energy Wh | Electricity the GPU used during the run |
| Cost | That energy times an electricity price |

## Data sources

Electricity cost uses your own price per kWh when you give one. Otherwise it uses the US average
residential price of $0.182/kWh, the 2026 figure from the US Energy Information Administration's
[Short-Term Energy Outlook](https://www.eia.gov/outlooks/steo/report/elec_coal_renew.php)
(October 2026). EIA data is published by the US government and is free to use. Each cost
records which price it was based on.

## License

[Apache 2.0](LICENSE)
