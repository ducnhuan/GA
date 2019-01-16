import numpy
import pandas as pd
import random
#Each sol have more than center will get penalty 10 000 000
#Each sol have violated to the constraint <M*Zk get penalty 1 000 000
#Each sol have customer no served or have more than 1 center served get 1000 000 
#Each center have not pass the min and max through will get 1000 000 
def integer_decsion(number_sol,capacity,decision):
    result=numpy.empty((0,80),int)
    for j in range(number_sol):
        temp=numpy.empty((0),int)
        for a in range(len(capacity[0])):
            for b in range(len(capacity)):
                sum_capacity=numpy.random.randint(10,high=capacity[b][a]/10,size=1)*10            
                #print(sum_capacity),
                for i in range(4):
                    k=numpy.random.randint(sum_capacity/10,size=1)
                    if decision[j][i] !=0:
                        temp=numpy.append(temp,k*10)
                        sum_capacity=sum_capacity-k*10
                    else:
                        temp=numpy.append(temp,0)
        result=numpy.append(result,[temp],axis=0)
    return result
def choose_center(decision):
    result=numpy.empty((0,4),int)
    for i in range(len(decision)):
        temp=numpy.array([0,0,0,0])
       # print(decision[i])
        center1=0
        center2=0
        center3=0
        center4=0
        for j in range(len(decision[0])):
                if divmod(j,4)[1]==0:
                    center1+=decision[i][j]
                elif divmod(j,4)[1]==1:
                   center2+=decision[i][j]
                elif divmod(j,4)[1]==2:
                    center3+=decision[i][j]
                else: 
                    center4+=decision[i][j]
        if center1>0:
            temp[0]=int(1)
        if center2>0:
            temp[1]=int(1)
        if center3>0:
            temp[2]=int(1)
        if center4>0:
            temp[3]=int(1)
        result=numpy.append(result,[temp],axis=0)
    return result
def generate_decsion_served(number_sol):
    result=numpy.empty((0,24),int)
    for k in range(number_sol):
        temp1=numpy.empty((0),int)
        for i in range(6):
            temp=numpy.random.choice([0,0,0,1],size=(4),replace=False)
            for j in range(len(temp)):
                temp1=numpy.append(temp1,temp[j])
        result=numpy.append(result,[temp1],axis=0)
    return result
def cal_pop_fitness(pop,demand,plan_distance,customer_distance,transport_fee,center): 
    fixed_cost=center[0]
    variable_cost=center[1]
    plan_fee=numpy.empty((0),int)
    customer_fee=numpy.empty((0,5),int)
    total_demand=numpy.empty((0),int)
    result=numpy.empty((0),int)
    for i in range(len(plan_distance)):
        for j in range(len(transport_fee[0])):
            plan_fee=numpy.append(plan_fee,plan_distance[i]*transport_fee[0][j],axis=0)
    for i in range(len(customer_distance)):
        for j in range(len(customer_distance[i])):
            customer_fee=numpy.append(customer_fee,[customer_distance[i][j]*transport_fee[0]],axis=0)
    demand_new=numpy.empty((0,5),int)
    for i in range(len(demand[0])):
        temp=numpy.empty((0),int)
        sum_temp=0
        for j in range(len(demand)):
            temp=numpy.append(temp,demand[j][i])
            sum_temp+=demand[j][i]
        demand_new=numpy.append(demand_new,[temp], axis=0)
        total_demand=numpy.append(total_demand,sum_temp)
   #Calculate the fee to transport the commodity from plan to center
    for i in range(len(pop)):
        temp=numpy.empty((0),int)
        center_serve=numpy.empty((0,6),int)
        amount_plan=numpy.empty((0),int)
        decision_serve=numpy.empty((0,4),int)
        chosen_center=numpy.empty((0,4),int)
        for j in range (24):
            temp=numpy.append(temp,pop[i][j])
            if divmod(j,4)[1]==3:
                decision_serve=numpy.append(decision_serve,[temp],axis=0)
                temp=numpy.empty((0),int)
        amount_plan=numpy.append(amount_plan,pop[i][28:],axis=0)
        #Calculate the fee to transport the commodity from plan to center
        plan_center_fee=numpy.sum(amount_plan*plan_fee,axis=0)
        #===>Result is plan_center_fee
        #Calculate the cost for transporting commodity from center to customer
        center_customer_fee=0
        for k in range(len(customer_fee)):
            z=divmod(k,4)
            center_customer_fee+=numpy.sum(customer_fee[k]*decision_serve[z[0]][z[1]]*demand_new[z[0]])
        #====> Result is center_customer_fee
        #Calculate for fixing the distribution center
        chosen_center=numpy.append(chosen_center,[pop[i][24:28]],axis=0)
        fixed_fee=numpy.sum(fixed_cost*chosen_center,axis=1)
        #===> Result is fixed_fee[0]
        #Calculate the fee for the commodity through the center
        for k in range(len(decision_serve[0])):
            temp=numpy.empty((0),int)
            for h in range(len(decision_serve)):
                temp=numpy.append(temp,decision_serve[h][k])
            center_serve=numpy.append(center_serve,[temp],axis=0)
        variable_fee=0
        for k in range(len(center_serve)):
            for h in range(len(center_serve[0])):
                variable_fee+=variable_cost[k]*center_serve[k][h]*total_demand[h]    
        #====>Result is variable_fee
        result=numpy.append(result,int(plan_center_fee+center_customer_fee+variable_fee+fixed_fee[0]))
    
    return result    
def penalty(pop,fitness,center,demand,capacity):
    min_through=center[2]
    max_through=center[3]
    chosen_center=numpy.empty((0,4))
    plant_amount=numpy.empty((0,80),int)
    decision_serve=numpy.empty((0,24),int)
    result=numpy.empty((0),int)
    for i in range(len(fitness)):
        result=numpy.append(result,fitness[i])
    for i in range(len(pop)):
        chosen_center=numpy.append(chosen_center,[pop[i][24:28]],axis=0)
        decision_serve=numpy.append(decision_serve,[pop[i][0:24]],axis=0)
        plant_amount=numpy.append(plant_amount,[pop[i][28:]],axis=0)
    for i in range(len(pop)):
        sum_center=int(numpy.sum(chosen_center[i]))
        if sum_center > 3 or sum_center==0:
            result[i]=result[i]+10000000
        center1=0
        center2=0
        center3=0
        center4=0
        for j in range(len(decision_serve[0])):
            if divmod(j,4)[1]==0:
                center1+=decision_serve[i][j]
            elif divmod(j,4)[1]==1:
                center2+=decision_serve[i][j]
            elif divmod(j,4)[1]==2:
                center3+=decision_serve[i][j]
            else: 
                center4+=decision_serve[i][j]
        if center1 > chosen_center[i][0]*7:
            result[i]=result[i]+ 1000000
        if center2 > chosen_center[i][1]*7:
            result[i]=result[i]+ 1000000
        if center3 > chosen_center[i][2]*7:
            result[i]=result[i]+ 1000000 
        if center4 > chosen_center[i][3]*7:
            result[i]=result[i]+ 1000000
        customer=numpy.array([0,0,0,0,0,0])
        for j in range(len(decision_serve[0])):
            if j<4:
                customer[0]+=decision_serve[i][j]
            elif j<8:
                customer[1]+=decision_serve[i][j]
            elif j<12:
                customer[2]+=decision_serve[i][j]
            elif j<16:
                customer[3]+=decision_serve[i][j]
            elif j<20:
                customer[4]+=decision_serve[i][j]
            else:
                customer[5]+=decision_serve[i][j]
        
        for k in range(len(customer)):
            if customer[k]!=1:
                result[i]=result[i]+100000000
        center1=numpy.array([0,0,0,0,0,0])
        center2=numpy.array([0,0,0,0,0,0])
        center3=numpy.array([0,0,0,0,0,0])
        center4=numpy.array([0,0,0,0,0,0])
        for j in range(len(decision_serve[0])):
            z=divmod(j,4)
            if z[1]==0:
                center1[z[0]]=decision_serve[i][j]
            elif z[1]==1:
                center2[z[0]]=decision_serve[i][j]
            elif z[1]==2:
                center3[z[0]]=decision_serve[i][j]
            else:
                center4[z[0]]=decision_serve[i][j]
        total_demand=numpy.empty((0),int)
        for j in range(len(demand[0])):
            sum_demand=0
            for k in range(len(demand)):
                sum_demand+=demand[k][j]
            total_demand=numpy.append(total_demand,sum_demand)
        through_center=numpy.array([0,0,0,0])
        through_center[0]=numpy.sum(center1*total_demand)
        through_center[1]=numpy.sum(center2*total_demand)
        through_center[2]=numpy.sum(center3*total_demand)
        through_center[3]=numpy.sum(center4*total_demand)
        a=numpy.greater_equal(through_center,min_through*chosen_center[i])
        b=numpy.less_equal(through_center,max_through*chosen_center[i])
        pen_temp=0
        for y in range(len(a)):
            if a[y] == False:
                pen_temp+=100000
        for y in range(len(b)):
            if b[y] == False:
                pen_temp+=100000
        decision=a.all() and b.all()
        if decision== False:
            result[i]=result[i]+pen_temp
        capacity_temp=numpy.empty((0),int)
        temp_sum=0
        for j in range(len(plant_amount[0])):
            temp_sum+=plant_amount[i][j]
            if divmod(j,4)[1]==3:
                capacity_temp=numpy.append(capacity_temp,temp_sum)
                temp_sum=0
        for j in range(len(capacity_temp)):
            z=divmod(j,5)
            if capacity_temp[j]> capacity[z[1]][z[0]]:
                result[i]=result[i]+100000000
        center_receive=numpy.empty((0),int)
        for k in range(20):
            j=k
            temp_sum=0
            while j< len(plant_amount[i]):
                temp_sum+=plant_amount[i][j]
                j+=20
            center_receive=numpy.append(center_receive,temp_sum)
        for k in range(len(center_receive)):
            z=divmod(k,4)
            if z[1]==0 and numpy.sum(center1*demand[z[0]])>center_receive[k]:
                result[i]=result[i]+10000000
            elif z[1]==1 and numpy.sum(center2*demand[z[0]])>center_receive[k]:
                result[i]=result[i]+10000000
            elif z[1]==2 and numpy.sum(center3*demand[z[0]])>center_receive[k]:
                result[i]=result[i]+10000000
            elif z[1]==3 and numpy.sum(center4*demand[z[0]])>center_receive[k]:
                result[i]=result[i]+10000000        
    return result
    ## The sum of chosen_center is  less or euqal to 3
    ## The format of decision_serve: [6,4] 6 customers, 4 center. The original structure is [len(pop), 24]
    ## The number of customer server by center must less than 7*Zk with Zk is the chosen center decision variable
    ## Each customer must only served by 1 center
    ## The through put of center must be less or equal to max through and large or equal with the min through if the center is chosen
    ## The commodity provide from the plan must be less or equal with the capacity of the plant
    ##The provide commodity must be large or equal to the served commodities by the center
def select_mating_pool(pop, fitness, num_parents,center,demand,capacity):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    fit_constraint=penalty(pop,fitness,center,demand,capacity)
    for parent_num in range(num_parents):
        min_fitness_idx = numpy.where(fit_constraint == numpy.amin(fit_constraint))
        min_fitness_idx = min_fitness_idx[0][0]
        parents[parent_num, :] = pop[min_fitness_idx, :]
        fitness[min_fitness_idx] =2147483647
    return parents
def select_mating_pool1(pop, fitness, num_parents,center,demand,capacity):
    parents=numpy.empty((num_parents, pop.shape[1]))
    fit_constraint=penalty(pop,fitness,center,demand,capacity)
    sum_array=numpy.sum(fit_constraint)
    p=sum_array/num_parents
    start = random.random()*p
    select_idx=numpy.empty((0),int)
    k=0
    sum_temp=fit_constraint[k]
    for i in range(num_parents):
        pointer=start+i*p
        if(sum_temp >= pointer):
            select_idx=numpy.append(select_idx,k)
        else:
            for k in range(k+1,len(fit_constraint)):
                sum_temp+=fit_constraint[k]
                if(sum_temp >= pointer):
                    select_idx=numpy.append(select_idx,k)
                    break
    for parent_num in range(num_parents):
        fitness_idx = select_idx[parent_num]
        parents[parent_num, :] = pop[fitness_idx, :]
    return parents
        





def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:12] = parents[parent1_idx, 0:12]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k,12:24] = parents[parent2_idx,12:24]
        offspring[k,24:26] = parents[parent1_idx, 24:26]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k,26:28] = parents[parent2_idx,26:28]
        offspring[k,28:67] = parents[parent1_idx,28:67]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k,67:108] = parents[parent2_idx,67:108]
    return offspring

def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        random_value = numpy.random.randint(0,28)
        for i in range (random_value,28):
            if int(offspring_crossover[idx,i])==0:
                offspring_crossover[idx,i]=1
            else:
                offspring_crossover[idx,i]=0
        random_index=numpy.random.randint(28,67)
        random_index1=numpy.random.randint(68,108)
        for i in range(random_index1-random_index+1):
            random_val=numpy.random.randint(-10,10)
            offspring_crossover[idx,random_index+i]+=random_val*10
            if offspring_crossover[idx,random_index+i] <0:
                offspring_crossover[idx,random_index+i]=offspring_crossover[idx,random_index+i]*-1
    print(offspring_crossover[idx])
    return offspring_crossover
