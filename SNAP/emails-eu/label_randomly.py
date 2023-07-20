import random


inetfile = "Email-EuAll.txt"
nlabels = 20
ofile = "emaileu-rand-"+str(nlabels)+".gfd"

random.seed(nlabels)

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



off = open(ofile,'w')

off.write("#emaileu-rand-"+str(nlabels)+"\n")
off.write(str(len(nodes))+"\n")
for i in range(len(nodes)):
	off.write( str(random.randint(0,nlabels-1)) +"\n" )
off.write(str(len(edges))+"\n")
for e in edges:
	off.write( str(nodes[e[0]]) +" "+str(nodes[e[1]])+"\n"  )

off.flush()
off.close()
