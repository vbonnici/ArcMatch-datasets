#nlabels="20 100 1000"
#nnodes="5 10 15 20 50"
#ntimes="100"

#for nl in $nlabels
#do
#echo $nl
#inet="dblp-rand-${nl}.gfd"
#qdir="dblp-rand-${nl}.gfd_queries"
#mkdir $qdir
#for ns in  $nnodes
#do
#echo $nl $ns
#python3 extract_large_fast.py  $inet true $ntimes $ns 1 "${qdir}/query_${ns}"
#done
#done

nnodes="5 10 15 20 50"
ntimes="100"

inet="dblp-comm-labels.gfd"
qdir="dblp-comm-labels.gfd_queries"
mkdir $qdir
for ns in  $nnodes
do
echo $nl $ns
python3 extract_large_fast.py  $inet true $ntimes $ns 1 "${qdir}/query_${ns}"
done



