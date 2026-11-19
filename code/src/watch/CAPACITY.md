# Capacity, 2026-11-19T04:11:31Z UTC

- Mac: GPU 22%, load 2.24, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 0.0%, CPU 2.0%, VRAM 6.1 of 10.0 GB, Ollama [{'name': 'qwen3:8b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 567684, 'mistral_7b': 589859}

## Advice
- Armature GPU under 10% for the last 10 readings (VRAM 6.1 of 10.0 GB). Put a judge or a training job on it.
- Harvest hermes3_8b silent for 9461 min.
- Harvest mistral_7b silent for 9830 min.
- Judge replies slow or timing out: armature timeout. One tiny request should take under 5 s.
