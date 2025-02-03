import time
def sparta_40701f4843():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_40701f4843()
def sparta_effeacbab4(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_f2205a7c09():sparta_effeacbab4(False)