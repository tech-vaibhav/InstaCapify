# InstaCapify

## 📁 Project Structure

```
InstaCapify/
│
├── main.py                      # Entry point for FastAPI app
├── requirements.txt             # Python dependencies
├── .gitignore                   # Ignore untracked files
│
├── routes/                      # All API route definitions
│   └── caption_route.py         # Route to handle caption generation
|   └── music_route.py           # Route to handle music suggestions
│
├── services/                    # All core logic / third-party APIs
│   └── gemini_service.py        # Logic to interact with Gemini API
|   └── spotify_mood_map.py      # Logic to interact with mood to playlist
|   └── spotify_service.py       # Logic to interact with Spotify API
|
└── utils/                       # Helper functions, validations, etc
    └── image_utils.py           # Image pre-processing utilities
```
