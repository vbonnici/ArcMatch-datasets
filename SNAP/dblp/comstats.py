import statistics

ifile = "com-dblp.all.cmty.txt"

csize = dict()
clist = list()

for line in open(ifile,'r'):
	cc = line.strip().split('\t')
	s = len(cc)
#	print(s)
	csize[s] = csize.get(s,0)+1
	clist.append(int(s))

for k,v in sorted(csize.items()):
	print(k,v)

print(statistics.mean(clist))
