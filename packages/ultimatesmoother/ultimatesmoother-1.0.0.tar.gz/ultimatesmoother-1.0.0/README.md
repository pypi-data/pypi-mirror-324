# The Ultimate Smoother

This is a python implementation of the digital smoothing filter introduced by John Ehlers in his article ["The Ultimate Smoother"](https://www.mesasoftware.com/papers/UltimateSmoother.pdf).

## Concepts

The UltimateSmoother preserves low-frequency swings in the input time series while attenuating high-frequency variations and noise. The defining input parameter of the UltimateSmoother is the critical period, which represents the minimum wavelength (highest frequency) in the filter's pass band. In other words, the filter attenuates or removes the amplitudes of oscillations at shorter periods than the critical period.

According to Ehlers, one primary advantage of the UltimateSmoother is that it maintains **zero lag** in its pass band and minimal lag in its transition band, distinguishing it from other conventional digital filters (e.g., moving averages). One can apply this smoother to various input data series.

## Calculations

On a technical level, the UltimateSmoother's unique response involves subtracting a high-pass response from an all-pass response. At very low frequencies (lengthy periods), where the high-pass filter response has virtually no amplitude, the subtraction yields a frequency and phase response practically equivalent to the input data
At other frequencies, the subtraction achieves filtration through cancellation due to the close similarities in response between the high-pass filter and the input data.

## Usage

```python
from ultimatesmoother import ultimate_smoother

us = ultimate_smoother(data, period)
```