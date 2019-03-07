"""
Python3 code for determining if two nodes are d-separated, given
a matrix representation of a DAG and a set of conditioned nodes.

The algorithm is based on Algorithm 3.1 in Koller and Friedman.

Author: Desh Raj (draj2@jhu.edu) 2019
"""

import numpy as np
import copy
import argparse

def readMatrix(filename):
	data = np.loadtxt(filename, delimiter=' ', skiprows=1, usecols=range(1,100))
	return data

def addNodesToList(A, B):
	"""
	Given a list of nodes A, and a list of nodes B
	to be added to A, this function returns a union
	of A and B.
	"""
	return list(set(A)|set(B))

def findParents(X, G):
	"""
	Given a matrix representation G of a DAG and a node
	Y, this returns all the parents of X in G.
	"""
	X_col = np.take(G, [X])
	parents = (np.where(X_col == 1)[0]).tolist()
	return parents

def findChildren(X, G):
	"""
	Given a matrix representation G of a DAG and a node
	Y, this returns all the children of X in G.
	"""
	X_row = G[X,:]
	children = (np.where(X_row == 1)[0]).tolist()
	return children


def findReachableNodes(G, X, Z):
	"""
	This function finds all nodes reachable (i.e. d-connected) from a source
	node, given a list of conditioned nodes.
	Inputs:
	G: an nxn matrix where the (i,j)th element is 1 if there is 
		directed edge from i to j, and 0 otherwise
	x: the source node
	Z: list of known (or conditioned) nodes (Python list)
	"""
	
	# Phase 1: insert all ancestors of Z into A

	L = copy.deepcopy(Z)	# nodes to be visited
	A = []					# ancestors of Z
	
	while (len(L) != 0):
		Y = L.pop(0)
		if (Y not in A):
			L = addNodesToList(L, findParents(Y, G))
		A = addNodesToList(A, [Y])

	# Phase 2: traverse active trails starting from X
	# Note: 0 denotes traversing in leaf to root direction
	# and 1 denotes root to leaf.

	L = [(X, 0)]			# (node, direction) to be visited
	V = []
	R = []

	while (len(L) != 0):
		(Y, d) = L.pop(0)
		if ((Y, d) not in V):
			if (Y not in Z):
				R = addNodesToList(R, [Y])		# Y is reachable
			V = addNodesToList(V, [(Y, d)])		# Mark (Y,d) as visited
			
			if (d==0) and (Y not in Z):	# Trail up through Y active if Y not in Z
				for z in findParents(Y, G):
					L = addNodesToList(L, [(z,0)])	# Y's parents to be visited from bottom
				for z in findChildren(Y, G):
					L = addNodesToList(L, [(z,1)])	# Y's children to be visited from top
			
			elif (d==1):	# Trail down through Y
				if Y not in Z:
					# Downward trails to Y's children are active
					for z in findChildren(Y, G):
						L = addNodesToList(L, [(z,1)])
				if Y in A:	# v-structure trails are active
					for z in findParents(Y, G):
						L = addNodesToList(L, [(z,0)])	# Y's parents to be visited from bottom

	return R

def checkIfDSeparated(G, X, Y, Z):
	"""
	This function checks if two nodes X and Y are d-separated
	in a graph G, when we have conditioned on a set of nodes Z.
	"""
	R = findReachableNodes(G, X, Z)
	return (Y not in R) # Y is d-separated from X if it is not reachable from X

def main():
	"""
	Driver code for the algorithm
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', "--graph-file", 
		help="File containing DAG in matrix form")
	parser.add_argument('-s', "--source", 
		help="source node", type=int)
	parser.add_argument('-t', "--target", 
		help="target node", type=int)
	parser.add_argument('-g', "--given", 
		help="list of conditioned nodes", type=int, nargs='*')
	args = parser.parse_args()

	G = readMatrix(args.graph_file)
	X = args.source - 1
	Y = args.target - 1
	Z = [z-1 for z in args.given]
	print (str(checkIfDSeparated(G, X, Y, Z)).upper())


if __name__=="__main__":
	main()






