import random


inetfile = "com-dblp.ungraph.txt"
icomfile = "com-dblp.all.cmty.txt"
ofile = "dblp-comm-labels.gfd"


coms = dict()
comid = 1
for line in open(icomfile,'r'):
	for cc in line.strip().split('\t'):
		coms[ int(cc) ] = comid
	comid += 1



edges = list()
nodes = dict()

for line in open(inetfile,'r'):
	if line[0] != '#':
		cc = line.strip().split('\t')
		if len(cc) == 2:

			n1 = int(cc[0])
			n2 = int(cc[1])

			edges.append( (n1,n2) )

			if n1 not in nodes:
				nodes[n1] = len(nodes)
			if n2 not in nodes:
				nodes[n2] = len(nodes)
		else:
			print(line)


print(len(edges))
print(len(nodes), max(nodes.keys()), max(nodes.values()))
print(comid)



off = open(ofile,'w')

off.write("#dblp-rand-comm\n")
off.write(str(len(nodes))+"\n")

invn = dict()
for k,v in nodes.items():
	invn[v] = k
for k,v in sorted(invn.items()):
	if v in coms:
		off.write( str( coms[v] )+"\n"  )
	else:
		off.write("0\n")

off.write(str(len(edges))+"\n")
for e in edges:
	off.write( str(nodes[e[0]]) +" "+str(nodes[e[1]])+"\n"  )

off.flush()
off.close()
