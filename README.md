# Language Pal
The project is an assistant for language spoken practice, the idea is for you to practice speaking to yourself, but with a little bit of help from the CLI, It gives you realtime feedback on the words you're pronouncing + the translation to your native language, so that you're sure that you're not accidentally swearing!

### Setup
Pre-download the speech model so the first recording does not stall on a
few-hundred-MB download:

```
uv run python fetch_models.py
```

Skipping this still works — the model downloads on the first mic tap instead.

### Features
* Speech-to-text + realtime translation
* [pending] - Save your conversations locally for later practice

