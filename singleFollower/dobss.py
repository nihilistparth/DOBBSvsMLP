import numpy as np
from docplex.mp.model import Model	

# m = input() #number of houses
# m = int(m)

# d = input() #number of houses to patrol in one pure strategy
# d = int(d)

# Vx = []  #value of goods in each house for leader

# for i in range(m):
# 	temp = input()
# 	Vx.append(int(temp))

# Vx = np.array(Vx)
# print(Vx)

# Vq = []  #value of goods in each house for follower

# for i in range(m):
# 	temp = input()
# 	Vq.append(int(temp))

# cx = input() #reward to the leader for catching the follower
# cx = int(cx) 

# cq = input() #cost to the follower for getting caught
# cq = int(cq)

m = 2 #number of houses
d = 1 #number of houses to patrol in one pure strategy

Vx = np.array([10,10]) #value of goods in each house for leader
Vq = np.array([10,10]) #value of goods in each house for follower
cx = 100 #reward to the leader for catching the follower
cq = 100 #cost to the follower for getting caught
py = np.array([0.50,0.25]) #probability of getting caught
X = np.array([1,2]) #leader routes
Q = np.array([1,2]) #follower routes

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

mdl_lead = Model(name='leader')

x = mdl_lead.continuous_var_list(R_l,0,1,'x')
q = mdl_lead.binary_var_list(R_f,name='q')

mdl_lead.add_constraint(mdl_lead.sum(i for i in x)==1)

mdl_lead.maximize(mdl_lead.sum(R[i][np.argmax(R[i][:][1])][0]*q[np.argmax(R[i][:][1])]*x[i] for i in range(R_l)))

sols_lead = mdl_lead.solve()
print(sols_lead)

x = [sols_lead['x_0'],sols_lead['x_1']] #leaders pure strategy

mdl_fol = Model(name='follower')

q = mdl_fol.binary_var_list(R_f,name='q')

mdl_fol.add_constraint(mdl_fol.sum(j for j in q)==1)

mdl_fol.maximize(mdl_fol.sum(R[i][j][0]*x[i]*q[j] for i in range(R_l) for j in range(R_f)))

sols_fol = mdl_fol.solve()
print(sols_fol)

