nlabels="20 100 1000"
nnodes="5 10 15 20 50"
ntimes="100"

for nl in $nlabels
do
echo $nl
inet="emaileu-rand-${nl}.gfd"
qdir="emaileu-rand-${nl}.gfd_queries"
mkdir $qdir
for ns in  $nnodes
do
echo $nl $ns
python3 extract_large_fast.py  $inet true $ntimes $ns 1 "${qdir}/query_${ns}"
done
done
