#!/bin/bash

#https://www.lukinotes.com/2017/06/enabling-single-webcam-for-multiple-applications-in-linux.html
ffplay -fs -f lavfi "movie=/dev/video0[out0];movie=/dev/video2[out1];[out0]transpose=2[out0];[out1]vflip[out1];[out1]transpose[out1];[out1][out0]hstack"
