import array
import math

import pygame


class SoundManager:
    """Builds the three sound effects in code (no audio files needed).

    If the machine has no audio device the game still runs, just silently.
    """

    SAMPLE_RATE = 44100

    def __init__(self):
        self.sounds = {}
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(self.SAMPLE_RATE, -16, 1, 512)
            rate, fmt, channels = pygame.mixer.get_init()
            if fmt != -16:
                return  # unexpected sample format, stay silent rather than crash
            self.rate = rate
            self.channels = channels
            self.sounds["jump"] = self._make([self._tone(300, 600, 0.12, 0.35)])
            self.sounds["score"] = self._make([self._tone(880, 1100, 0.10, 0.35)])
            self.sounds["game_over"] = self._make([
                self._tone(440, 400, 0.18, 0.4),
                self._tone(330, 300, 0.18, 0.4),
                self._tone(220, 120, 0.40, 0.4),
            ])
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def _tone(self, f_start, f_end, seconds, volume):
        """A sine tone that slides from f_start to f_end and fades out."""
        n = int(self.rate * seconds)
        out = []
        phase = 0.0
        for i in range(n):
            t = i / n
            freq = f_start + (f_end - f_start) * t
            phase += 2 * math.pi * freq / self.rate
            envelope = 1.0 - t
            out.append(int(32767 * volume * envelope * math.sin(phase)))
        return out

    def _make(self, parts):
        samples = [s for part in parts for s in part]
        if self.channels == 2:
            samples = [s for s in samples for _ in (0, 1)]
        return pygame.mixer.Sound(buffer=array.array("h", samples).tobytes())

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()
