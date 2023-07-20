#!/bin/bash

ids="/media/data/datasets/RI-Datasets/PPI/udistr"
#nlabels="1 4 16 32 128 2048"
#nlabels="2048 128 32 16 4 1"
#elabels="1 2 8 32 128 1024"
#elabels="1024 128 32 8 2 1"
nlabels="1 16 32 128 256 1024"
elabels="1 16 32 128 256 1024"

ntimes="5"
qnnodes="4 8 12 16 20 24"

for nl in $nlabels
do

mkdir $nl

for el in $elabels
do

echo $nl $el
mkdir $nl/$el

for inet in `ls $ids/$nl/*.gfd`
do

bnet=`basename $inet | sed s/\.gfd/\.egfd/g`
onet="$nl/$el/$bnet"
echo $inet $bnet $onet

python3 add_edge_labels.py $inet $onet $el

qdir="$nl/$el/${bnet}_queries_ind"
rm -r $qdir
mkdir $qdir

for ns in $qnnodes
do

python3 extract_equeries_ind.py  $onet true $ntimes $ns "${qdir}/query_${ns}" ".egfd"

#exit

done

done

done

done
