#/bin/bash

OS_CONFIG_COMPARE_16=OpenSMILE/config/compare16/ComParE_2016.conf
OS_CONFIG=$OS_CONFIG_COMPARE_16
f=302_AUDIO_2.wav
output_file=test.csv

OpenSMILE/opensmile-3.0.0/build/progsrc/smilextract/SMILExtract -C $OS_CONFIG -I $f -csvoutput $output_file