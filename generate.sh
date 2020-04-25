#!/bin/bash

#this is the shell script that produced all the output in the output directory/


pip3 install . || echo "Unable to install. Run this in a python virtualenv!" >&2

if [ ! -z "$1" ]; then
    FONT=$1
    if [ ! -z "$2" ]; then
        SUBFONT=$2
    else
        SUBFONT="sans"
    fi
else
    FONT="sans"
    SUBFONT="sans"
fi

hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --rows 14 --columns 13 -o output/hsk1_pinyinorder_a4 hsk1.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --nolevels --rows 14 --columns 13 -o output/hsk2_pinyinorder_a4 --minlevel 2 --maxlevel 2 hsk1.txt hsk2.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --nolevels --rows 16 --columns 17 -o output/hsk3_pinyinorder_a4 --minlevel 3 --maxlevel 3 hsk1.txt hsk2.txt hsk3.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --nolevels --rows 16 --columns 16 -o output/hsk4_pinyinorder_a4 --minlevel 4 --maxlevel 4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --nolevels --rows 16 --columns 16 -o output/hsk5_pinyinorder_a4 --minlevel 5 --maxlevel 5 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --nolevels  --rows 16 --columns 16 -o output/hsk6_pinyinorder_a4 --minlevel 6 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt

#frequency order
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --rows 14 --columns 13 -o output/hsk1_freqorder_a4 hsk1.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --nolevels --rows 14 --columns 13 -o output/hsk2_freqorder_a4 --minlevel 2 --maxlevel 2 hsk1.txt hsk2.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --nolevels --rows 16 --columns 17 -o output/hsk3_freqorder_a4 --minlevel 3 --maxlevel 3 hsk1.txt hsk2.txt hsk3.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --nolevels --rows 16 --columns 16 -o output/hsk4_freqorder_a4 --minlevel 4 --maxlevel 4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --nolevels --rows 16 --columns 16 -o output/hsk5_freqorder_a4 --minlevel 5 --maxlevel 5 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --nolevels  --rows 16 --columns 16 -o output/hsk6_freqorder_a4 --minlevel 6 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt


#multiple levels
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --rows 16 --columns 20 -o output/hsk1to3_a4 hsk1.txt hsk2.txt hsk3.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --rows 16 --columns 20 -o output/hsk1to3_pinyinorder_a4 hsk1.txt hsk2.txt hsk3.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --rows 16 --columns 20 -o output/hsk1to4_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --rows 16 --columns 20 -o output/hsk1to4_pinyinorder_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --rows 16 --columns 20 -o output/hsk1to6_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --rows 16 --columns 20 -o output/hsk1to6_pinyinorder_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt

hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --rows 32 --columns 36 -o output/hsk1to4_a1 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --pinyinorder --rows 32 --columns 36 -o output/hsk1to4_pinyinorder_a1 hsk1.txt hsk2.txt hsk3.txt hsk4.txt

#confusibles
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --subrows 3 --rows 14 --columns 18 -o output/confusibleorder_a4 hanzi_confusibles.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --subrows 3 --rows 11 --columns 14 -o output/confusibleorder_large_a4 hanzi_confusibles.txt
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --rows 29 --subrows 3 --columns 38 -o output/confusibleorder_a1 hanzi_confusibles.txt

#narrow version for mobile
hanzigrid --font "$FONT" --subfont "$SUBFONT" -a --rows 34 --subrows 3 --columns 8 -o output/confusibleorder_narrow hanzi_confusibles.txt
