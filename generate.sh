#!/bin/bash

pip3 install . || echo "Unable to install. Run this in a python virtualenv!" >&2

hanzigrid -a --pinyinorder --rows 14 --columns 13 -o output/hsk1_pinyinorder_a4 hsk1.txt
hanzigrid -a --pinyinorder --nolevels --rows 14 --columns 13 -o output/hsk2_pinyinorder_a4 --minlevel 2 --maxlevel 2 hsk1.txt hsk2.txt
hanzigrid -a --pinyinorder --nolevels --rows 16 --columns 17 -o output/hsk3_pinyinorder_a4 --minlevel 3 --maxlevel 3 hsk1.txt hsk2.txt hsk3.txt
hanzigrid -a --pinyinorder --nolevels --rows 16 --columns 16 -o output/hsk4_pinyinorder_a4 --minlevel 4 --maxlevel 4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid -a --pinyinorder --nolevels --rows 16 --columns 16 -o output/hsk5_pinyinorder_a4 --minlevel 5 --maxlevel 5 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt
hanzigrid -a --pinyinorder --nolevels  --rows 16 --columns 16 -o output/hsk6_pinyinorder_a4 --minlevel 6 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt

#frequency order
hanzigrid -a --rows 14 --columns 13 -o output/hsk1_freqorder_a4 hsk1.txt
hanzigrid -a --nolevels --rows 14 --columns 13 -o output/hsk2_freqorder_a4 --minlevel 2 --maxlevel 2 hsk1.txt hsk2.txt
hanzigrid -a --nolevels --rows 16 --columns 17 -o output/hsk3_freqorder_a4 --minlevel 3 --maxlevel 3 hsk1.txt hsk2.txt hsk3.txt
hanzigrid -a --nolevels --rows 16 --columns 16 -o output/hsk4_freqorder_a4 --minlevel 4 --maxlevel 4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid -a --nolevels --rows 16 --columns 16 -o output/hsk5_freqorder_a4 --minlevel 5 --maxlevel 5 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt
hanzigrid -a --nolevels  --rows 16 --columns 16 -o output/hsk6_freqorder_a4 --minlevel 6 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt


#multiple levels
hanzigrid -a --rows 16 --columns 20 -o output/hsk1to3_a4 hsk1.txt hsk2.txt hsk3.txt
hanzigrid -a --pinyinorder --rows 16 --columns 20 -o output/hsk1to3_pinyinorder_a4 hsk1.txt hsk2.txt hsk3.txt
hanzigrid -a --rows 16 --columns 20 -o output/hsk1to4_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid -a --pinyinorder --rows 16 --columns 20 -o output/hsk1to4_pinyinorder_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid -a --rows 16 --columns 20 -o output/hsk1to6_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt
hanzigrid -a --pinyinorder --rows 16 --columns 20 -o output/hsk1to6_pinyinorder_a4 hsk1.txt hsk2.txt hsk3.txt hsk4.txt hsk5.txt hsk6.txt

hanzigrid -a --rows 32 --columns 36 -o output/hsk1to4_a1 hsk1.txt hsk2.txt hsk3.txt hsk4.txt
hanzigrid -a --pinyinorder --rows 32 --columns 36 -o output/hsk1to4_pinyinorder_a1 hsk1.txt hsk2.txt hsk3.txt hsk4.txt

#confusibles
hanzigrid -a --rows 16 --columns 20 -o output/confusibleorder_a4 hanzi_confusibles.txt
hanzigrid -a --rows 34 --columns 34 -o output/confusibleorder_a1 hanzi_confusibles.txt
