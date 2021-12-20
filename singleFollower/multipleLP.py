import numpy as np
from docplex.mp.model import Model

m = int(input()) #number of houses
d = int(input()) #number of houses to patrol in one pure strategy

Vx = np.array([int(x) for x in input().split()]) #value of goods in each house for leader
Vq = np.array([int(q) for q in input().split()]) #value of goods in each house for follower
cx = int(input()) #reward to the leader for catching the follower
cq = int(input()) #cost to the follower for getting caught
py = np.array([float(p) for p in input().split()]) #probability of getting caught

#leader pycx + (1−py)(−vy,x),
#follower −pycq + (1−py)(vy,q)
#		follower     (leader,follower)
#leader		1 	        2
#	1              (-V2x,V2q)
#	2 	(-V1x,V1q) 
R = np.zeros((2,2,2)) #payoff matrix
R_l = np.size(R,0) #dimension for leader
R_f = np.size(R,1)  #dimnesion for follower
for i in range(R_l):
	for j in range(R_f):
		if(i==j):
			R[i][j][0] = py[j]*cx + (1-py[j])*(-Vx[j])
			R[i][j][1] = -py[j]*cq + (1-py[j])*(Vq[j])
		else:
			R[i][j][0] = -Vx[j]
			R[i][j][1] = Vq[j]

print('PayOff Matrix: ')
print(R)

mdl = Model(name='LP')
strat_lead = mdl.continuous_var_list(R_l,0,1,'strat_lead')
strat_fol = mdl.binary_var_list(R_f,name='strat_fol')

mdl.add_constraint(mdl.sum(i for i in strat_lead)==1)
mdl.add_constraint(mdl.sum(j for j in strat_fol)==1)

for j in range(R_f):
	mdl.add_constraint(mdl.sum(strat_lead[i]*np.max(R[i][:][1]) for i in range(R_l)) >= mdl.sum(strat_lead[i]*R[i][j][1] for i in range(R_l)))

mdl.maximize(mdl.sum(strat_lead[i]*R[i][np.argmax(R[i][:][1])][0] for i in range(R_l)))

sols = mdl.solve()
print(sols)
