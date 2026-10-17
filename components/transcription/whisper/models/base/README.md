# Whisper base multilingual, Atonim component 1.0.0

This component distributes the existing OpenAI Whisper base multilingual model
in whisper.cpp-compatible GGML form. Atonim does not claim model authorship and
does not modify, quantize, or reconvert these model bytes.

- Upstream model and exact Git LFS identity: [ggml-base.bin](https://huggingface.co/ggerganov/whisper.cpp/blob/80da2d8bfee42b0e836fc3a9890373e5defc00a6/ggml-base.bin).
- [Upstream model card](https://huggingface.co/ggerganov/whisper.cpp/blob/80da2d8bfee42b0e836fc3a9890373e5defc00a6/README.md): OpenAI Whisper GGML models, MIT license.
- [OpenAI MIT license](https://github.com/openai/whisper/blob/86098128c0b4f24f0e2aa2994de830614b474227/LICENSE): Copyright (c) 2022 OpenAI. The full notice accompanies both release and component archive.
- Unchanged model: 147951465 bytes, SHA-256 `60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe`.
- [Immutable Atonim distribution release](https://github.com/Ruckola/atonim-dependencies/releases/tag/whisper-base-macos-arm64-v1.0.0) contains the exact raw model, the license notice, and the component archive. The archive is required by the existing component installer; its distinct size is 133317540 bytes and its SHA-256 is `b81f51a850d813faa45c54ae54c0b21c6e76f3c3b1c83b25fa17b1937f3313f9`.

The signed `1.0.0.json` manifest is the authenticated archive installation
contract; its model export hash refers to the unchanged raw model inside it.
