# Anime AI — AnimeXstream Fine-tuned Model

**Model name**: Anime AI
**Base**: HuggingFaceTB/SmolLM2-135M-Instruct
**Developer**: Om Sharma (AnimeXstream coder, modder, developer)
**Made for**: AnimeXstream

## Purpose
Anime AI is a lightweight LoRA fine-tuned model that understands anime metadata:
seasons, episodes, titles, release dates, categories, and keywords.

## Safety guarantees
- **Never** trained on URLs, streaming links, download links, or video IDs.
- Training data whitelist-filtered before training.
- No external identifiers embedded in weights.

## Usage
```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
model = PeftModel.from_pretrained(base, "models/round-5/adapter")
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
```

## Disclaimer
Model provides metadata suggestions, not guaranteed production data.
