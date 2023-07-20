#!/bin/bash

ids="/media/data/datasets/RI-Datasets/PPI/udistr"
#nlabels="1 4 16 32 128 2048"
#elabels="2 8 32 128 1024"
#nlabels="1 4 8 16 32 64 128"
#elabels="1 4 8 16 32 64 128"


nlabels="1 16 32 128 256 1024"
elabels="8"


nlabels="2 4 8 16"
elabels="1 2 4 8 16 32 128 256 1024"


nlabels="1 16 32 128 256 1024"
elabels="2 4 8"


nlabels="1 2 4 8 16 32 64 128 1024"
elabels="64"


nlabels="64"
elabels="1 2 4 8 16 32 64 128 256 1024"


nlabels="1 2 4 8 16 32 64 128 256 1024"
elabels="64"


nlabels="1"
elabels="2"



ntimes="5"
qnnodes="4 8 12 16 32"

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

qdir="$nl/$el/${bnet}_queries"
rm -r $qdir
mkdir $qdir

for ns in $qnnodes
do

python3 extract_equeries.py  $onet true $ntimes $ns 1 "${qdir}/query_${ns}" ".egfd"

#exit

done

done

done

done
