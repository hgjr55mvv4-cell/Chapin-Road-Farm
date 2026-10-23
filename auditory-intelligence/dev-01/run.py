"""Print synthetic development results; no microphones or recordings."""
import json
from audio_dev import evaluate

if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
