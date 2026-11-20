# Capacity, 2026-11-20T17:29:51Z UTC

- Mac: GPU 97%, load 7.24, processes {'harvest.py': 0, 'train_live.py': 0, 'mlx_lm lora': 0, 'mlx_lm server': 2, 'dpo': 0}
- Armature: GPU 12.0%, CPU 79.0%, VRAM 8.0 of 10.0 GB, Ollama [{'name': 'freed-qwen:14b', 'on_gpu': True}]
- Harvest logs silent (s): {'hermes3_8b': 701984, 'mistral_7b': 724160}

## Advice
- Harvest hermes3_8b silent for 11699 min.
- Harvest mistral_7b silent for 12069 min.
- Judge replies slow or timing out: mac 21 s, armature timeout. One tiny request should take under 5 s.
