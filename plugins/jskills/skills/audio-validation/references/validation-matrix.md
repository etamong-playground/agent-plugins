# Select validation by feature

| Feature | Controlled fixture and expected behavior | Additional evidence |
| --- | --- | --- |
| File inspection | Known header, frame count, channel layout and decoded normalization; reject corrupt/unsupported input without changing it | Real supported files and scoped sandbox access |
| Sample peak | Silence, single impulse, known-amplitude PCM tone, different channel peaks, block-boundary maximum; compare analytic maximum and agreed dBFS convention | Quantization-aware tolerance and displayed precision |
| RMS or loudness | Stated window/gating/channel weighting and independent reference output; do not reuse sample-peak expectations | Applicable algorithm/standard version and licensed reference corpus if compliance is claimed |
| Graph processing | Fixed input and parameters through bounded offline rendering; check duration, tails, clipping and cancellation as defined by the effect | Live graph/device behavior remains separate |
| File export | Reopen new output and inspect encoding, frames, channels and declared metadata; originals unchanged; interrupted write handled | Final signed app, destination permissions and available disk space |
| Live capture/playback | Controlled state-machine faults; no unbounded callback work; test denials and stop/restart behavior | Actual devices, rates/layouts, disconnect, sleep/wake, overruns and defined latency method |
| Native UI | State transitions, accessible values and testable controls | Real app keyboard, VoiceOver, resize, contrast and permission/device-state checks |
| Audio Unit | Saved/restored state, parameters, buses and offline output in the selected format | Actual supported hosts/DAWs, automation, architecture, signed installation and validation |

Use silence explicitly: logarithmic dBFS has no finite value at zero amplitude.
Choose and test a clear display representation without adding a small arbitrary constant to the underlying measurement.
A sine with amplitude 0.5 reaches approximately -6.0206 dBFS sample peak only if the sampled sequence actually includes a phase at its maximum; specify frequency, sample rate, phase, duration and sample format.
For a simple analytic test, an impulse of normalized amplitude 0.5 gives that maximum directly.
Specify any tolerance before running the implementation, and test a deliberately incorrect result when verifying a regression test.

For live audio, record callback timing/overruns separately from mean CPU usage and file-processing throughput.
Do not derive hardware round-trip latency solely from a configured buffer size.
Use low, controlled monitoring levels and authorized routing for human/device checks; offline tests should not produce sound.
