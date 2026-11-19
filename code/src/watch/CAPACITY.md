# Capacity, 2026-11-19T20:47:21Z UTC

- Mac: GPU 93%, load 1.3, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 0.0%, CPU 7.0%, VRAM 6.1 of 10.0 GB, Ollama [{'name': 'qwen3:8b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 627434, 'mistral_7b': 649610}

## Advice
- Armature GPU under 10% for the last 10 readings (VRAM 6.1 of 10.0 GB). Put a judge or a training job on it.
- Harvest hermes3_8b silent for 10457 min.
- Harvest mistral_7b silent for 10826 min.
- Judge replies slow or timing out: armature timeout. One tiny request should take under 5 s.
