# Capacity, 2026-11-21T02:50:53Z UTC

- Mac: GPU 97%, load 4.87, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 12.0%, CPU 74.0%, VRAM 8.0 of 10.0 GB, Ollama [{'name': 'freed-qwen:14b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 735647, 'mistral_7b': 757823}

## Advice
- Harvest hermes3_8b silent for 12260 min.
- Harvest mistral_7b silent for 12630 min.
- Judge replies slow or timing out: armature timeout. One tiny request should take under 5 s.
