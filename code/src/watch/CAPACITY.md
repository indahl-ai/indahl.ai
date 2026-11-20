# Capacity, 2026-11-20T04:37:43Z UTC

- Mac: GPU 81%, load 8.04, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 0.0%, CPU 2.0%, VRAM 6.1 of 10.0 GB, Ollama [{'name': 'qwen3:8b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 655657, 'mistral_7b': 677833}

## Advice
- Armature GPU under 10% for the last 10 readings (VRAM 6.1 of 10.0 GB). Put a judge or a training job on it.
- Harvest hermes3_8b silent for 10927 min.
- Harvest mistral_7b silent for 11297 min.
- Judge replies slow or timing out: mac 55 s, armature timeout. One tiny request should take under 5 s.
