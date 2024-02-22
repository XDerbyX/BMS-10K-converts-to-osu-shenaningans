# BMS-10K-converts-to-osu-shenaningans
A fork from Hugged converter using GCS 10K BMS PACK as an Example

The `BMSconv Derby Edit.py` file works just like Hugged's with some modifications.

Firstly, I converted the 10K BMS files using this `BMSconv Derby Edit.py` script + Raindrop from 10K to 16K. I do this because Raindrop messes up the converts if I try to convert from BMS 10K straight to osu! 10K.

The `BMSconv 16 to 10.py` file changes the position of the notes from 16K to the correct coordinates to fit 10K, so no notes will overlap. It also changes the `CircleSize` or how many columns there are from 16 to 10. (the only problem I've encountered so far is that if there are any scratch chart that got converted by accident i.e. 10K2S, it will bug out.)

The `GCS Fix.py` file is used after converting a chart from soundsphere. (I use this if there are any missing charts.)
