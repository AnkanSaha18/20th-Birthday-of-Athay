"""Composes and renders the site's background music: a music-box waltz in F major.

Romantic intro -> "Happy Birthday" (public-domain melody) -> an original love theme
-> "Happy Birthday" again, brighter -> soft outro that loops back to the start.

Run:  python3 tools/make_music.py   (writes assets/music.wav, then converts to assets/music.m4a with afconvert)
"""
import numpy as np, wave, subprocess, os

SR = 44100
BPM = 84
BEAT = 60 / BPM
rng = np.random.default_rng(31102006)

NOTE = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}
def hz(n):
    name, octv = n[:-1], int(n[-1])
    return 440 * 2 ** ((NOTE[name] + 12 * (octv + 1) - 69) / 12)

CHORDS = {
    'F': ['F', 'A', 'C'], 'C': ['C', 'E', 'G'], 'C7': ['C', 'E', 'Bb'], 'Dm': ['D', 'F', 'A'],
    'Bb': ['Bb', 'D', 'F'], 'Am': ['A', 'C', 'E'], 'Gm': ['G', 'Bb', 'D'], 'F7': ['F', 'A', 'Eb'],
}

def music_box(f, dur, vol):
    t = np.arange(int(SR * (dur + 2.2))) / SR
    env = np.exp(-t * 2.3) * np.minimum(1, t / .004)
    s = (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)
         + .12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 5) + .06 * np.sin(2 * np.pi * 4.2 * f * t) * np.exp(-t * 8))
    return s * env * vol

def harp(f, dur, vol):
    t = np.arange(int(SR * (dur + 1.6))) / SR
    env = np.exp(-t * 3.2) * np.minimum(1, t / .006)
    s = np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t) + .08 * np.sin(2 * np.pi * 3 * f * t)
    return s * env * vol

def bass(f, dur, vol):
    t = np.arange(int(SR * (dur + 1.0))) / SR
    env = np.exp(-t * 1.6) * np.minimum(1, t / .01)
    return (np.sin(2 * np.pi * f * t) + .2 * np.sin(2 * np.pi * 2 * f * t)) * env * vol

def pad(freqs, dur, vol):
    n = int(SR * (dur + 1.2)); t = np.arange(n) / SR
    env = np.minimum(1, t / .9) * np.where(t < dur, 1, np.exp(-(t - dur) * 3))
    s = np.zeros(n)
    for f in freqs:
        for d in (-.12, .12):  # gentle chorus
            s += np.sin(2 * np.pi * (f + d) * t) + .18 * np.sin(2 * np.pi * 2 * (f + d) * t)
    return s * env * vol / len(freqs)

class Song:
    def __init__(self, beats):
        self.L = np.zeros((int(SR * (beats * BEAT + 4)),))
        self.R = np.zeros_like(self.L)
    def add(self, sig, at_beat, pan=0.0):
        i = int(at_beat * BEAT * SR); j = min(len(self.L), i + len(sig)); sig = sig[:j - i]
        self.L[i:j] += sig * (1 - pan) * .5 * 2 ** .5 * .71
        self.R[i:j] += sig * (1 + pan) * .5 * 2 ** .5 * .71

def waltz_bar(song, b, chord, intensity=1.0, arp=False):
    """Accompaniment for one 3/4 bar starting at beat b."""
    root, third, fifth = CHORDS[chord]
    song.add(bass(hz(root + '2'), BEAT * 2, .55 * intensity), b, -.1)
    for k in (1, 2):
        for n in (third, fifth):
            o = '4' if NOTE[n] < NOTE['F'] else '3'
            song.add(harp(hz(n + o), BEAT, .16 * intensity), b + k, .25)
    song.add(pad([hz(root + '3'), hz(third + '4' if NOTE[third] < NOTE['F'] else third + '3'), hz(fifth + '4' if NOTE[fifth] < NOTE['F'] else fifth + '3')],
                 BEAT * 3, .22 * intensity), b, 0)
    if arp:
        seq = [root + '5', third + '5', fifth + '5', third + '5', fifth + '5', root + '6']
        for k, n in enumerate(seq):
            song.add(music_box(hz(n), BEAT / 2, .12 * intensity), b + k * .5, .35 - .12 * k)

def melody(song, b, notes, vol=.42, octave_up=0, pan=-.15):
    for n, d in notes:
        if n != 'r':
            name, o = n[:-1], int(n[-1]) + octave_up
            song.add(music_box(hz(f'{name}{o}'), d * BEAT, vol), b, pan)
        b += d
    return b

HB = [('C5', .75), ('C5', .25),
      ('D5', 1), ('C5', 1), ('F5', 1), ('E5', 2), ('C5', .75), ('C5', .25),
      ('D5', 1), ('C5', 1), ('G5', 1), ('F5', 2), ('C5', .75), ('C5', .25),
      ('C6', 1), ('A5', 1), ('F5', 1), ('E5', 1), ('D5', 1), ('Bb5', .75), ('Bb5', .25),
      ('A5', 1), ('F5', 1), ('G5', 1), ('F5', 3)]
HB_CHORDS = ['F', 'C', 'C', 'F', 'F7', 'Bb', 'F', 'F']
HB_SECOND_HALF_BAR7 = 'C'

LOVE = [('A5', 2), ('G5', .5), ('F5', .5),
        ('E5', 2), ('C5', 1),
        ('D5', 2), ('F5', 1),
        ('E5', 2), ('G5', 1),
        ('F5', 1.5), ('E5', .5), ('D5', 1),
        ('D5', 2), ('C5', 1),
        ('Bb4', 1), ('D5', 1), ('G5', 1),
        ('E5', 2.5), ('C5', .5)]
LOVE_CHORDS = ['F', 'Am', 'Bb', 'C', 'Dm', 'Bb', 'Gm', 'C7']

INTRO_CHORDS = ['F', 'F', 'Dm', 'Dm', 'Bb', 'Bb', 'C', 'C']

def build():
    bars = 8 + 1 + 8 + 8 + 8 + 1 + 8 + 4
    song = Song(bars * 3)
    b = 0.0
    # Intro: music-box arpeggios over a soft pad
    for i, c in enumerate(INTRO_CHORDS):
        waltz_bar(song, b, c, intensity=.55 + .05 * i, arp=True); b += 3
    # Happy Birthday #1 (pickup bar is a quiet F bar)
    waltz_bar(song, b, 'F', .7); b += 2
    start = b
    melody(song, b, HB, vol=.45)
    for i, c in enumerate(HB_CHORDS):
        waltz_bar(song, start + 1 + i * 3, c, .9)
    b = start + 1 + 8 * 3
    # Love theme, twice (second time with sparkle arps)
    for rep in range(2):
        melody(song, b, LOVE, vol=.4 if rep == 0 else .44, octave_up=rep)
        for i, c in enumerate(LOVE_CHORDS):
            waltz_bar(song, b + i * 3, c, 1.0, arp=(rep == 1))
        b += 24
    # Happy Birthday #2, an octave higher with arps
    waltz_bar(song, b, 'C7', .8); b += 2
    start = b
    melody(song, b, HB, vol=.36, octave_up=1, pan=.1)
    melody(song, b, HB, vol=.22, octave_up=0, pan=-.2)
    for i, c in enumerate(HB_CHORDS):
        waltz_bar(song, start + 1 + i * 3, c, 1.0, arp=(i % 2 == 1))
    b = start + 1 + 8 * 3
    # Outro: gentle F arps fading out
    for i in range(4):
        waltz_bar(song, b, 'F' if i % 2 == 0 else 'Bb', .6 - .12 * i, arp=True); b += 3
    total = int((b * BEAT + 2.5) * SR)
    return song.L[:total], song.R[:total]

def reverb(x, seconds=2.4, mix=.28):
    n = int(SR * seconds)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.0)
    ir[0] = 0
    ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    wet = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
    return x * (1 - mix) + wet * mix * 1.6

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, '..', 'assets')
    L, R = build()
    L, R = reverb(L), reverb(R)
    # fade edges so the loop is seamless
    fi, fo = int(SR * .05), int(SR * 2.5)
    for ch in (L, R):
        ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo)
    peak = max(np.abs(L).max(), np.abs(R).max())
    L, R = L / peak * .85, R / peak * .85
    pcm = (np.stack([L, R], 1) * 32767).astype('<i2')
    wav = os.path.join(out, 'music.wav')
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    m4a = os.path.join(out, 'music.m4a')
    subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '160000', wav, m4a], check=True)
    os.remove(wav)
    print('wrote', m4a, f'{len(L) / SR:.1f}s')

if __name__ == '__main__':
    main()
