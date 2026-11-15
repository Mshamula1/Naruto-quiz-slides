# one-time per session: python deps + Kokoro voice model (downloaded from GitHub releases; Hugging Face is blocked)
set -e
pip install -q --break-system-packages kokoro-onnx soundfile scipy 2>&1 | grep -v -i warning || true
mkdir -p ~/tts; cd ~/tts
[ -s v.onnx ] || curl -sSL -o v.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -s voices.bin ] || curl -sSL -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
ls -la ~/tts; echo SETUP_OK
