# Deepgram TTS profile

Create a Deepgram API key with Text-to-Speech access and billing/usage permission, then download `recipes/deepgram/deepgram-tts-v1.0.1.json` and use **Import Profile…** in Atonim. Enter the key in Configure, then use **Discover** to load the currently available Aura 2 voices. The displayed voice name is friendly; Atonim stores Deepgram's canonical model ID. Keep the MP3 output setting unless you intentionally publish a compatible new profile version.

Version 1.0.1 uses Deepgram's public `GET /v1/models` TTS collection and filters `architecture=aura-2`; it does not claim account-private models. This profile is structurally validated against Atonim's generic HTTP contract and Deepgram's documented REST API. It has not made a paid synthesis request or completed clean-build GUI/provider acceptance.
