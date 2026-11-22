# Capacity, 2026-11-22T03:17:36Z UTC

- Mac: GPU 28%, load 3.6, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 0, 'dpo': 0}
- The GPU host: GPU 0.0%, CPU 0.0%, VRAM 0.0 of 10.0 GB, Ollama []
- Harvest logs silent (s): {}

## Advice
- GPU host under 10% for the last 10 readings (VRAM 0.0 of 10.0 GB). Put a judge or a training job on it.
- Judge replies slow or timing out: gpuhost timeout. One tiny request should take under 5 s.
