

#!/usr/bin/python3
# -*- coding:LATIN-1 -*-

def lambdaPE(angstrom):
	"lambdaPE() calcule la partie entiÃ¨re de la longueur d'onde choisie"
	if(angstrom>10000 or angstrom<=0):
		print("choix de longueur d'onde hors limite")
		return None
	else:
		angstrom = angstrom//256
	
	return angstrom
	
	
def lambdaModulo(angstrom):
	"lambdaModulo() calcule la longueur d'onde choisie modulo 256"	
	if(angstrom>10000 or angstrom<=0):
		print("choix de longueur d'onde hors limite")
		return None
	else:
		angstrom = angstrom%256
	
	return angstrom
	

def convBin(angstrom):
	"convBin() converts angstroms en binaries"
	angstromPE = lambdaPE(angstrom)
	angstromMod = lambdaModulo(angstrom)
	
	binPE = []; binMod = []
	
	for i in [0,1,3,4,5,6,7]:
		binMod.append(angstromMod & 1)
		binPE.append(angstromPE & 1)
		#print(binMod); print(binPE); print()	
		angstromMod = angstromMod >> 1;
		angstromPE = angstromPE >> 1
	
	print(binMod); print(binPE)
	
	return binMod,binPE
