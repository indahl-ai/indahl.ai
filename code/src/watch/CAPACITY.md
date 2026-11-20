# Capacity, 2026-11-20T11:07:10Z UTC

- Mac: GPU 0%, load 1.36, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 0.0%, CPU 3.0%, VRAM 6.1 of 10.0 GB, Ollama [{'name': 'qwen3:8b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 679024, 'mistral_7b': 701200}

## Advice
- Armature GPU under 10% for the last 10 readings (VRAM 6.1 of 10.0 GB). Put a judge or a training job on it.
- Harvest hermes3_8b silent for 11317 min.
- Harvest mistral_7b silent for 11686 min.
- Judge replies slow or timing out: armature timeout. One tiny request should take under 5 s.
