#Calculate Single Deep Groove Bearing
calculationFactor_singleDeepGroove = [
	#from Lecture
	#Fa/C0, Y, e
	(0.014,2.30,0.19),
	(0.028,1.99,0.22),
	(0.056,1.71,0.26),
	(0.084,1.55,0.28),
	(0.110,1.45,0.30),
	(0.170,1.31,0.34),
	(0.280,1.15,0.38),
	(0.420,1.04,0.42),
	(0.560,1.00,0.44)]

def find_Y_e(FaC0,calculationFactor):  #return X,Y,e
	#print("finding X,Y,e :")
	X = 0.56
	for i,element in enumerate(calculationFactor):
		FaC0_table = element[0]
		if i!=0: prev_element = calculationFactor[i-1]
		
		if FaC0_table == FaC0:
			Y = element[1]
			e = element[2]
			return X,Y,e 
			
		elif FaC0_table > FaC0:
			#assume
			if i==0: prev_element = (0.007,2.7,0.17)#; print("*")
			
			#print(element[0],prev_element[0])
			ratio = (FaC0-prev_element[0])/(element[0]-prev_element[0])
			Y = element[1] + (prev_element[1]-element[1])*ratio
			e = prev_element[2] + (element[2]-prev_element[2])*ratio
			return X,Y,e
	Y = 0
	e = 1000000
	return X,Y,e

def find_P(X,Y,Fa,Fr,V=1.0):  #return Pmax
	#print("finding P :")
	P1 = X*V*Fr + Y*Fa
	P2 = V*Fr
	return P1 if P1>P2 else P2

def find_L10(C,P,rpm,N=1.5,k=3.0):  #return L10
	#print("finding L10 :")
	L10 = (C/N/P)**3		#*10^6 round
	L10 = L10*1000000/rpm/60#in hr
	return L10

#Init
Fa = 2.8 #kN
Fr = 4.0 #kN
rpm = 3000
V = 1.2
singleDeepGroove_catalogue = [
	#[0]d	[1]C0	[2]C	[3]info
	(10,	3.4,	8.06,	"D=35 B=11"),
	(50,	23.2,	37.1,	"D=90 B=20"),
	(50,	52.0,	87.1,	"D=130 B=31"),
	(80,	125.0,	163.0,	"D=200 B=48"),
	(100,	140.0,	174.0,	"D=215 B=47"),
	(105,	153.0,	182.0,	"D=225 B=49"),
	(110,	180.0,	203.0,	"D=240 B=50"),
	(120,	186.0,	208.0,	"D=260 B=55"),
	(160,	285.0,	276.0,	"D=340 B=68"),
	(200,	310.0,	270.0,	"D=360 B=58")
]

#Run
requireHour = 20000 #hr

Ans = []
AllUseableInfo = []
choice = singleDeepGroove_catalogue
for eachC0andC in choice:
	
	d = eachC0andC[0]
	C0 = eachC0andC[1]
	C = eachC0andC[2]
	serie = eachC0andC[-1]
	
	i = Fa/C0
	X,Y,e = find_Y_e(i,calculationFactor_singleDeepGroove)
	if (Fa/V/Fr) > e:  #is able to be use
		P = find_P(X,Y,Fa,Fr,V)
		
		L10 = find_L10(C,P,rpm)
		if L10 > requireHour:  
			Ans.append("[ {} <{:2.0f}mm>] C0={:>6.2f}  C={:>6.2f}  L10={:9.2f}  P={:6.3f}  e={:5.2f}  X={:5.2f}  Y={:5.2f}".format(serie,d,C0,C,L10,P,e,X,Y))
		
		AllUseableInfo.append("[ {} <{:2.0f}mm>] C0={:>6.2f}  C={:>6.2f}  L10={:9.2f}  P={:6.3f}  e={:5.2f}  X={:5.2f}  Y={:5.2f}".format(serie,d,C0,C,L10,P,e,X,Y))
		
		if e < 0.19: 
			AllUseableInfo[-1] = AllUseableInfo[-1].replace("e","*e")
			Ans[-1] = Ans[-1].replace("e","*e")
	
	else: continue

for ans in AllUseableInfo:
	print(ans)

print("\nuseable :")
for ans in Ans:
	print(ans)
