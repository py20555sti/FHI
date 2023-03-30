#!/bin/python3

from subprocess import PIPE, run
import subprocess

right = ''
left = ''

# ffplay
# https://www.lukinotes.com/2017/06/enabling-single-webcam-for-multiple-applications-in-linux.html
# usb
# https://superuser.com/questions/902012/how-to-identify-usb-webcam-by-serial-number-from-the-linux-command-line

command = ['v4l2-ctl', '--list-devices']
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

for dev in result.stdout.split('HD 720P webcam: '):
    pair = dev.split('):')
    if len(pair) != 2:
        continue
    if pair[0].split(':')[2] == '1a.0-1.3':
        left = pair[1].split()[0]
    if pair[0].split(':')[2] == '1d.0-1.3':
        right = pair[1].split()[0]

command = ['ffplay', '-fs', '-f', 'lavfi',
           'movie={0}[out0];movie={1}[out1];[out0]transpose=2[out0];[out1]vflip[out1];[out1]transpose[out1];[out1][out0]hstack'.format(left, right)]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
print('retcode: {0}\n\nstdout:\n{1}\nstderr:\n{2}'.format(
    result.returncode, result.stdout, result.stderr))
