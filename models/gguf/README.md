# Anime AI - GGUF (llama.cpp / Termux)

**Model**: Anime AI (SmolLM2-135M-Instruct + LoRA Round-5 merged)
**Developer**: Om Sharma (AnimeXstream)
**Format**: GGUF F16 (no quantization - best quality)

## Files
- anime-ai-f16.gguf - Full precision F16 (~270 MB)

## Termux usage
   llama-cli -m models/gguf/anime-ai-f16.gguf \
     -p "<|im_start|>system\nYou are Anime AI.<|im_end|>\n
         <|im_start|>user\nAnime: X, Season: 1, Episode: 1<|im_end|>\n
         <|im_start|>assistant\n" \
     -n 200 -c 512 --temp 0.2 -t 4

## Safety
- No URLs, IDs, or streaming links in training data.