#!/usr/bin/env python2

import array
import subprocess

import wave_gen, sequencer
from note_gen import ChromaticSeries, ChromaticHalfStep, get_frequency

seq = sequencer.Sequencer()

seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.C, 0, 4)), 0.0, 0.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.C, 0, 4)), 0.5, 0.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 1.0, 1.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 1.5, 1.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.A, 0, 5)), 2.0, 2.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.A, 0, 5)), 2.5, 2.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 3.0, 3.9)

seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 4.0, 4.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 4.5, 4.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 5.0, 5.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 5.5, 5.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.D, 0, 4)), 6.0, 6.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.D, 0, 4)), 6.5, 6.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.C, 0, 4)), 7.0, 7.9)

seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 8.0, 8.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 8.5, 8.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 9.0, 9.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 9.5, 9.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 10.0, 10.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 10.5, 10.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.D, 0, 4)), 11.0, 11.9)

seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 12.0, 12.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 12.5, 12.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 13.0, 13.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 13.5, 13.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 14.0, 14.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 14.5, 14.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.D, 0, 4)), 15.0, 15.9)

seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.C, 0, 4)), 16.0, 16.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.C, 0, 4)), 16.5, 16.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 17.0, 17.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 17.5, 17.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.A, 0, 5)), 18.0, 18.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.A, 0, 5)), 18.5, 18.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.G, 0, 4)), 19.0, 19.9)

seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 20.0, 20.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.F, 0, 4)), 20.5, 20.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 21.0, 21.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.E, 0, 4)), 21.5, 21.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.D, 0, 4)), 22.0, 22.4)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.D, 0, 4)), 22.5, 22.9)
seq.insert(wave_gen.SineWave(get_frequency(ChromaticSeries.C, 0, 4)), 23.0, 23.9)

seq_iter = seq.into_discrete_iter(8000)

ffplay = subprocess.Popen(["ffplay", "-f", "f32le", "-ar", "8000", "-ac", "1", "-nodisp", "-autoexit", "-"], stdin = subprocess.PIPE)

for i in seq_iter:
    b = array.array("f")
    b.append(i * 2.0)
    b.tofile(ffplay.stdin)

ffplay.stdin.close()
ffplay.wait()
