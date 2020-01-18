#!/usr/bin/env bash

# turns off auto-exposure
v4l2-ctl --set-ctrl exposure_auto=1
# sets exposure value to 20
v4l2-ctl --set-ctrl exposure_absolute=15

# disable auto white-balance, set to 5000K
v4l2-ctl --set-ctrl white_balance_temperature_auto=0
v4l2-ctl --set-ctrl white_balance_temperature=2800

# set contrast
v4l2-ctl --set-ctrl contrast=255
