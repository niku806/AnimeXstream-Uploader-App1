# Anime AI - GGUF (llama.cpp / Termux)

**Model**: Anime AI (SmolLM2-135M-Instruct + LoRA Round-5 merged)
**Developer**: Om Sharma (AnimeXstream)
**Format**: GGUF Q4_K_M

## Termux usage

1. Install Termux packages:
   pkg install git cmake clang python -y

2. Clone this repo:
   git clone https://github.com/niku806/AnimeXstream-Uploader-App1.git
   cd AnimeXstream-Uploader-App1

3. Download llama.cpp Termux binary from:
   https://github.com/ggml-org/llama.cpp/releases

4. Run inference (prompt uses SmolLM2 chat template):
   ./llama-cli -m models/gguf/anime-ai-Q4_K_M.gguf -n 200 -c 512 --temp 0

## Safety
- No URLs, IDs, or streaming links in training data.
- Model provides metadata suggestions, not guaranteed production data.