"""AUDITORY-DEV-01. Controlled pure-tone WAV timing, NOT speech understanding.

Words are external symbolic labels. No microphone, ASR, mental-state inference,
or external participant recordings are accessed.
"""
from __future__ import annotations
import io
import math
import random
import struct
import wave
from dataclasses import dataclass

SAMPLE_RATE = 8000
FRAME_SAMPLES = 80  # 10 ms
AMPLITUDE = 0.42
SILENCE_RMS_MAX = 0.08
CLIP_COUNT_MIN = 4
FIRST = (0.20, 0.62)
TONES = (440., 620.)

@dataclass(frozen=True)
class Observation:
    sensor_status: str
    active_intervals_s: tuple[tuple[float, float], ...]
    gap_s: float | None
    reason: str


def render(gap_s: float, *, seed: int = 42, noise: float = .008,
           amplitude: float = AMPLITUDE, omit_second: bool = False) -> bytes:
    """Generate two pure-tone bursts at known times in mono PCM16 WAV."""
    if not (0 <= gap_s <= 2.0) or noise < 0 or amplitude < 0:
        raise ValueError('invalid synthetic generator parameter')
    second_start = FIRST[1] + gap_s
    spans = [(FIRST[0], FIRST[1], TONES[0])]
    if not omit_second:
        spans.append((second_start, second_start + .42, TONES[1]))
    duration = second_start + .62
    rng = random.Random(seed)
    out = io.BytesIO()
    with wave.open(out, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        pcm = bytearray()
        for i in range(int(duration * SAMPLE_RATE)):
            t = i / SAMPLE_RATE
            sample = rng.uniform(-noise, noise)
            for start, stop, f in spans:
                if start <= t < stop:
                    sample += amplitude * math.sin(2 * math.pi * f * (t - start))
            pcm += struct.pack('<h', round(max(-1., min(1., sample)) * 32767))
        wav.writeframes(pcm)
    return out.getvalue()


def observe(wav_bytes: bytes | None) -> Observation:
    """Return post-hoc inter-burst gap; abstain on questionable sensor data."""
    if not wav_bytes:
        return Observation('MISSING', (), None, 'No waveform was supplied')
    try:
        with wave.open(io.BytesIO(wav_bytes), 'rb') as wav:
            if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getframerate() != SAMPLE_RATE:
                return Observation('UNSUPPORTED_FORMAT', (), None, 'Expected mono PCM16 8 kHz')
            raw = wav.readframes(wav.getnframes())
    except (wave.Error, EOFError, ValueError):
        return Observation('UNREADABLE', (), None, 'Invalid or truncated WAV')
    if len(raw) < FRAME_SAMPLES * 2 * 5 or len(raw) % 2:
        return Observation('UNREADABLE', (), None, 'Not enough complete audio frames')
    samples = struct.unpack('<' + str(len(raw) // 2) + 'h', raw)
    clipped = sum(abs(x) >= 32766 for x in samples)
    if clipped >= CLIP_COUNT_MIN:
        return Observation('CLIPPED', (), None, 'Clipped samples; timing unreliable')
    nframes = len(samples) // FRAME_SAMPLES
    active = []
    for k in range(nframes):
        chunk = samples[k * FRAME_SAMPLES:(k + 1) * FRAME_SAMPLES]
        rms = math.sqrt(sum((v/32767.)**2 for v in chunk) / len(chunk))
        active.append(rms > SILENCE_RMS_MAX)
    if active[0] or active[1] or sum(active) / len(active) > .80:
        return Observation('BACKGROUND_UNRELIABLE', (), None, 'Activity at recording boundary or nearly continuous energy')
    intervals = []
    start = None
    for i, flag in enumerate(active + [False]):
        if flag and start is None:
            start = i
        if not flag and start is not None:
            if (i - start) >= 3:
                intervals.append((round(start * .01, 3), round(i * .01, 3)))
            start = None
    if len(intervals) != 2:
        return Observation('INSUFFICIENT_EVENTS', tuple(intervals), None,
                           'Need exactly two observed bursts to measure inter-burst gap')
    gap = round(intervals[1][0] - intervals[0][1], 3)
    if gap < 0:
        return Observation('UNRELIABLE', tuple(intervals), None, 'Overlapping measured events')
    return Observation('OK', tuple(intervals), gap, 'Energy-based gap only; not identified as speech')


def gap_band(gap_s: float | None) -> str:
    if gap_s is None:
        return 'UNKNOWN'
    return 'SHORT' if gap_s <= .30 else ('LONG' if gap_s >= .50 else 'AMBIGUOUS')


def decide(*, text: str, gap_s: float | None, sensor_status: str = 'OK') -> str:
    """Illustrative conservative routing, NOT real-world appropriateness."""
    if sensor_status != 'OK':
        return 'ABSTAIN_REQUEST_CLEAR_SAMPLE'
    if 'no, i meant' in text.lower():
        return 'CONFIRM_EXPLICIT_CORRECTION'
    return {'SHORT': 'WAIT', 'LONG': 'READY_NOT_OBLIGATED_TO_REPLY',
            'AMBIGUOUS': 'WAIT', 'UNKNOWN': 'UNKNOWN_WAIT'}[gap_band(gap_s)]


def evaluate() -> dict:
    texts = ['I thought you knew.', 'I thought you knew.']
    examples = [('short', .12), ('long', .68)]
    rows = []
    for (name, target_gap), text in zip(examples, texts):
        observation = observe(render(target_gap))
        rows.append({
            'case': name, 'external_transcript': text,
            'waveform_is_real_speech': False,
            'gold_gap_s': target_gap,
            'sensor_status': observation.sensor_status,
            'observed_gap_s': observation.gap_s,
            'gap_absolute_error_s': round(abs(observation.gap_s - target_gap), 3) if observation.gap_s is not None else None,
            'audio_activity_action': decide(text=text, gap_s=observation.gap_s,
                                           sensor_status=observation.sensor_status),
            'transcript_only_action': decide(text=text, gap_s=None),
            'transcript_with_gold_timestamps_action': decide(text=text, gap_s=target_gap),
        })
    return {
        'research_id': 'AUDITORY-DEV-01', 'status': 'EXPOSED_ENGINEERING_DEV',
        'sample_rate_hz': SAMPLE_RATE, 'frame_resolution_ms': 10,
        'cases': rows,
        'nonclaims': [
            'No intelligible speech is generated or decoded; transcript text is an external label.',
            'No turn-end prediction before a future event; this measures a completed inter-burst gap offline.',
            'No real user preference, intent, mental state, or AI conversation effect is measured.',
            'Transcript plus accurate timestamps is a fair strong baseline that matches audio-derived timing when detection works.',
        ],
    }
