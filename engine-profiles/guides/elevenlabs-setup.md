# ElevenLabs profiles

Download one JSON profile from `recipes/elevenlabs/`, then use **Import Profile…** in Atonim. Enter your ElevenLabs API key in Configure. Select a voice and model through Discover before rendering. Voice Changer v1.0.1 discovers up to 100 My Voices per page (up to 10 pages); manage or add personal voices in ElevenLabs **My Voices**, then choose Discover again in Atonim. It does not search the public Voice Library.

Voice Changer exposes Stability, Similarity and Speaker Boost as request-scoped voice settings. It accepts normal source-audio assets through Atonim's generic HTTP audio pipeline; ElevenLabs accepts common encoded audio formats, while the application owns any project-media normalization. These profiles are structurally validated only; they have not yet completed clean-build provider acceptance or paid Voice Changer playback/failure-path acceptance.
