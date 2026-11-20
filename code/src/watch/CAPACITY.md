# Capacity, 2026-11-20T15:30:28Z UTC

- Mac: GPU 4%, load 1.9, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 0.0%, CPU 3.0%, VRAM 8.0 of 10.0 GB, Ollama [{'name': 'freed-qwen:14b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 694820, 'mistral_7b': 716996}

## Advice
- Armature GPU under 10% for the last 10 readings (VRAM 8.0 of 10.0 GB). Put a judge or a training job on it.
- Harvest hermes3_8b silent for 11580 min.
- Harvest mistral_7b silent for 11949 min.
- Judge replies slow or timing out: armature timeout. One tiny request should take under 5 s.
