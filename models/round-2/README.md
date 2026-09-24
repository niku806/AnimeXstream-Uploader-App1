# Round 2 — Anime AI LoRA Adapter

**Base model**: HuggingFaceTB/SmolLM2-135M-Instruct
**Adapter type**: LoRA (r=16, alpha=32, dropout=0.05)
**Trainable params**: 4,884,480 (3.50%)
**Final loss**: 0.1363891033075189
**Training time**: 122.0 sec
**Examples trained**: 2000
**Resumed from**: models/round-1/

## Purpose
Anime AI — anime metadata assistant for AnimeXstream.
Developer: Om Sharma (AnimeXstream coder, modder, developer).

## Safety
- No URLs, streaming links, download links, or video IDs in training data.
- Training data sanitized via whitelist filter.
