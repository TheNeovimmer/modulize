#!/usr/bin/env python3
"""Synthesized SFX bed for the modulize 60s promo — stdlib only."""
import math, struct, wave

SR = 44100
DUR = 60.0
N = int(SR * DUR)
out = bytearray(n := 0) if False else bytearray()

# scene ping times (matching the 8 cuts, 7.5s each)
pings = [0.4, 7.9, 15.4, 22.9, 30.4, 37.9, 45.4, 52.9]

def ping(t, freq=880.0, decay=1.2, amp=0.18):
    """soft sine ping with exponential decay"""
    v = math.sin(2 * math.pi * freq * t) * math.exp(-t * decay) * amp
    return v

samples = []
for i in range(N):
    t = i / SR
    # low drone + gentle warmth
    v = 0.05 * math.sin(2 * math.pi * 55 * t) + 0.03 * math.sin(2 * math.pi * 110 * t) + 0.012 * math.sin(2 * math.pi * 220 * t)
    # pings
    for p in pings:
        dt = t - p
        if 0 <= dt < 2.0:
            v += ping(dt, 880 * (1.0 + 0.05 * (pings.index(p) % 3)))
    # final warm chord swell 53-60s
    if 53 <= t:
        k = (t - 53) / 7.0
        v += 0.06 * k * (math.sin(2*math.pi*220*t) + math.sin(2*math.pi*330*t) + math.sin(2*math.pi*440*t)) / 3
    # overall fade out last 2s
    if t > 58:
        v *= (60 - t) / 2
    v = max(-0.9, min(0.9, v))
    samples.append(struct.pack("<hh", int(v * 32767), int(v * 32767)))

with wave.open("/home/theneovimmer/Documents/Modulize/assets/promo/audio.wav", "wb") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes(b"".join(samples))
print("wrote audio.wav", DUR, "s")
