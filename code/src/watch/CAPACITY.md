# Capacity, 2026-11-20T00:17:55Z UTC

- Mac: GPU 3%, load 3.57, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 0.0%, CPU 6.0%, VRAM 6.1 of 10.0 GB, Ollama [{'name': 'qwen3:8b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 640068, 'mistral_7b': 662244}

## Advice
- Armature GPU under 10% for the last 10 readings (VRAM 6.1 of 10.0 GB). Put a judge or a training job on it.
- Harvest hermes3_8b silent for 10667 min.
- Harvest mistral_7b silent for 11037 min.
- Judge replies slow or timing out: armature timeout. One tiny request should take under 5 s.
