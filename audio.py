import math
import wave
import struct
from pathlib import Path
import pygame  # type: ignore

AUDIO_DIR = Path(__file__).resolve().parent / "audio_assets"
SFX_DIR = AUDIO_DIR / "sfx"
MUSIC_DIR = AUDIO_DIR / "music"
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2
CHANNELS = 2

_initialized = False
_available = False
_sounds = {}
_current_music = None
_master_volume = 0.8  # 0-1 float, default 80%
_sfx_enabled = True
_music_enabled = True


def _ensure_dirs():
    for folder in (AUDIO_DIR, SFX_DIR, MUSIC_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def _write_wav(path, samples, channels=1):
    with wave.open(str(path), "wb") as file:
        file.setnchannels(channels)
        file.setsampwidth(SAMPLE_WIDTH)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(samples)


def _make_samples(frequencies, duration, volume=0.5, waveform="sine", channels=1):
    length = int(SAMPLE_RATE * duration)
    buffer = bytearray()
    for i in range(length):
        t = i / SAMPLE_RATE
        sample = 0.0
        for freq, amp in frequencies:
            angle = 2.0 * math.pi * freq * t
            if waveform == "triangle":
                sample += (2.0 / math.pi) * math.asin(math.sin(angle)) * amp
            else:
                sample += math.sin(angle) * amp
        sample = max(-1.0, min(1.0, sample * volume))
        packed = struct.pack("<h", int(sample * 32767))
        buffer.extend(packed * channels)
    return bytes(buffer)


def _generate_sound(path, frequencies, duration, volume=0.35, waveform="sine", channels=1):
    if not path.exists():
        samples = _make_samples(frequencies, duration, volume=volume, waveform=waveform, channels=channels)
        _write_wav(path, samples, channels=channels)


def _generate_assets():
    _ensure_dirs()
    _generate_sound(SFX_DIR / "button.wav", [(880, 1.0)], 0.08, volume=0.3)
    _generate_sound(SFX_DIR / "move.wav", [(660, 1.0)], 0.05, volume=0.25)
    _generate_sound(SFX_DIR / "rotate.wav", [(980, 1.0)], 0.06, volume=0.3)
    _generate_sound(SFX_DIR / "hard_drop.wav", [(520, 1.0)], 0.08, volume=0.35)
    _generate_sound(SFX_DIR / "hold.wav", [(720, 1.0)], 0.07, volume=0.28)
    _generate_sound(SFX_DIR / "clear.wav", [(440, 1.0), (660, 0.5)], 0.16, volume=0.4)
    _generate_sound(SFX_DIR / "game_over.wav", [(220, 1.0), (110, 0.5), (330, 0.5)], duration=0.45, volume=0.35, waveform="triangle")

    # Tạo nhạc default nếu không có file nhạc nào trong thư mục
    audio_exts = ['.wav', '.mp3', '.mp4', '.ogg', '.m4a']
    has_audio = any(any(MUSIC_DIR.glob(f"*{ext}")) for ext in audio_exts)
    if not has_audio:
        melody = [440, 494, 523, 587, 660, 740, 784, 880]
        mix = []
        for note in melody:
            mix.append((note, 0.7))
            mix.append((note * 0.5, 0.4))
        music_samples = _make_samples(mix, 8.0, volume=0.26, waveform="triangle", channels=2)
        _write_wav(MUSIC_DIR / "background.wav", music_samples, channels=2)


def _load_sounds():
    if not _available:
        return
    file_map = {
        "button": SFX_DIR / "button.wav",
        "move": SFX_DIR / "move.wav",
        "rotate": SFX_DIR / "rotate.wav",
        "hard_drop": SFX_DIR / "hard_drop.wav",
        "hold": SFX_DIR / "hold.wav",
        "clear": SFX_DIR / "clear.wav",
        "game_over": SFX_DIR / "game_over.wav",
    }
    for key, path in file_map.items():
        try:
            _sounds[key] = pygame.mixer.Sound(str(path))
            _sounds[key].set_volume(_master_volume)
        except Exception:
            _sounds[key] = None


def init_audio():
    global _initialized, _available
    if _initialized:
        return
    try:
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
        _available = True
    except Exception:
        _available = False

    _generate_assets()
    _load_sounds()
    _initialized = True


def set_master_volume(volume_percent):
    """Set master volume from 0-100 integer to 0.0-1.0 float"""
    global _master_volume
    _master_volume = max(0.0, min(1.0, volume_percent / 100.0))
    if not _available:
        return
    pygame.mixer.music.set_volume(_master_volume)
    for sound in _sounds.values():
        if sound:
            sound.set_volume(_master_volume)


def set_sfx_enabled(enabled):
    global _sfx_enabled
    _sfx_enabled = enabled


def set_music_enabled(enabled):
    global _music_enabled
    _music_enabled = enabled
    if not _available:
        return
    if _music_enabled:
        pass
    else:
        pygame.mixer.music.stop()


def play_sfx(name):
    if not _available or not _sfx_enabled or _master_volume == 0:
        return
    sound = _sounds.get(name)
    if sound:
        sound.play()


def play_music(track_name="background", loops=-1):
    global _current_music
    if not _available or not _music_enabled or _master_volume == 0:
        return
    extensions = ['.mp4', '.mp3', '.wav', '.ogg', '.m4a']
    track_path = None
    for ext in extensions:
        path = MUSIC_DIR / f"{track_name}{ext}"
        if path.exists():
            track_path = path
            break
    if track_path:
        try:
            pygame.mixer.music.load(str(track_path))
            pygame.mixer.music.set_volume(_master_volume)
            pygame.mixer.music.play(loops)
            _current_music = track_name
        except Exception as e:
            print(f"Audio load error: {e}")
    else:
        if track_name == "background":
            default_path = MUSIC_DIR / "background.wav"
            if not default_path.exists():
                melody = [440, 494, 523, 587, 660, 740, 784, 880]
                mix = []
                for note in melody:
                    mix.append((note, 0.7))
                    mix.append((note * 0.5, 0.4))
                music_samples = _make_samples(mix, 8.0, volume=0.26, waveform="triangle", channels=2)
                _write_wav(default_path, music_samples, channels=2)
            try:
                pygame.mixer.music.load(str(default_path))
                pygame.mixer.music.set_volume(_master_volume)
                pygame.mixer.music.play(loops)
                _current_music = track_name
            except Exception:
                pass


def stop_music():
    if _available:
        pygame.mixer.music.stop()


def update_audio_settings(config):
     vol = config.get("volume", 80)
     if isinstance(vol, str):
         vol = 100 if vol == "on" else 0
     set_master_volume(vol)
     set_sfx_enabled(config.get("sfx", "on") == "on")
     set_music_enabled(config.get("music", "on") == "on")

def apply_volume_only(volume_value):
     """Chỉ thay đổi volume, không restart nhạc"""
     set_master_volume(volume_value)


def is_audio_available():
    return _available
