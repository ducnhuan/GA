import numpy
import pandas as pd
import algo
import os
#Get data from excel file data.xlsx
def Genetic_algorithm(path,num_gen,num_sol,selection):
    data=pd.read_excel(path).as_matrix()
    capacity=data[0:5,0:4]
    demand=data[6:11,0:6]
    plan_distance=data[13:17,1:5]
    customer_distance=data[17:23,1:5]
    transport_fee=data[24:25,0:5]
    center=data[26:30,0:4]
    best_result=[]
    number_generation=num_gen
    #Number of chromosome per population
    sol_per_pop =num_sol
    num_parents_mating=int(sol_per_pop/2)
    #Binary decision variable for center choose and center serve to customer
    num_weights= len(center[0])*len(demand[0])
    pop_size=(sol_per_pop,num_weights)
    binary_served=algo.generate_decsion_served(sol_per_pop)
    binary_center=algo.choose_center(binary_served)
    binary_population=numpy.append(binary_served,binary_center,axis=1)
    #Integer decision variable for transfer the commodity from plan to center
    num_weights=len(capacity[0])*len(capacity)*len(center[0])
    pop_size=(sol_per_pop,num_weights)
    integer_population=algo.integer_decsion(sol_per_pop,capacity,binary_center)
    #Merge two population in to innitiate population 
    new_population=numpy.append(binary_population,integer_population,axis=1)
    print(new_population)
    print(new_population[0])
    print("Selection: ",selection=="Linear")
    for generation in range(number_generation):
        print("Generation",generation)
        fitness = algo.cal_pop_fitness(new_population,demand,plan_distance,customer_distance,transport_fee,center)
        print("Value of cost:",fitness)
        if selection=="Linear":
            parents = algo.select_mating_pool(new_population, fitness,num_parents_mating,center,demand,capacity)
        else:
            parents = algo.select_mating_pool1(new_population, fitness,num_parents_mating,center,demand,capacity)
        offspring_crossover = algo.crossover(parents,offspring_size=(pop_size[0]-parents.shape[0],parents.shape[1]))
        offspring_mutation = algo.mutation(offspring_crossover)
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation
        print("Best result:",numpy.amin(algo.cal_pop_fitness(new_population,demand,plan_distance,customer_distance,transport_fee,center)))
        best_result.append(numpy.amin(algo.cal_pop_fitness(new_population,demand,plan_distance,customer_distance,transport_fee,center)))

    cost = algo.cal_pop_fitness(new_population,demand,plan_distance,customer_distance,transport_fee,center)
    fitness=algo.penalty(new_population,cost,center,demand,capacity)
    # Then return the index of that solution corresponding to the best fitness.
    best_match_idx = numpy.where(fitness == numpy.amin(fitness))
    if len(best_match_idx[0])>1:
        result=numpy.append(new_population[best_match_idx[0][0], :],cost[best_match_idx[0][0]])
    else:
        result=numpy.append(new_population[best_match_idx[0], :],cost[best_match_idx[0]])
    return result

    
result=Genetic_algorithm("data.xlsx",1,10,"Linear")
print(result)




def checkPath(path):
    print(path)
    return os.path.exists(path)


















'''pop=numpy.array([[0,0,0,1,
                      0,0,1,0,
                      0,0,0,1,
                      0,0,1,0,
                      0,0,0,1,
                      0,1,0,0,
                      0,1,1,1,
                      0,160,0,0,
                      0,100,0,0,
                      0,100,0,0,
                      0,50,0,50,
                      0,300,0,0,
                      0,0,400,0,
                      0,0,500,0,
                      0,0,200,0,
                      0,0,150,0,
                      0,0,550,0,
                      0,0,50,200,
                      0,0,0,350,
                      0,0,0,600,
                      0,0,0,200,
                      0,0,0,200,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,100,
                      0,0,0,200,
                      0,0,0,0],
                      [1,0,0,1,
                      0,0,1,0,
                      0,0,0,1,
                      0,0,1,0,
                      0,0,0,1,
                      0,1,0,0,
                      0,1,1,1,
                      0,160,0,0,
                      0,100,0,0,
                      0,100,0,0,
                      0,50,0,50,
                      0,300,0,0,
                      0,0,400,0,
                      0,0,500,0,
                      0,0,200,0,
                      0,0,150,0,
                      0,0,550,0,
                      0,0,50,200,
                      0,0,0,350,
                      0,0,0,600,
                      0,0,0,200,
                      0,0,0,200,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,100,
                      0,0,0,200,
                      0,0,0,0],
                      [0,0,1,1,
                      0,0,1,0,
                      0,0,0,1,
                      0,0,1,0,
                      0,0,0,1,
                      0,1,0,0,
                      0,1,1,1,
                      0,160,0,0,
                      0,100,0,0,
                      0,100,0,0,
                      0,50,0,50,
                      0,300,0,0,
                      0,0,400,0,
                      0,0,500,0,
                      0,0,200,0,
                      0,0,150,0,
                      0,0,550,0,
                      0,0,50,200,
                      0,0,0,350,
                      0,0,0,600,
                      0,0,0,200,
                      0,0,0,200,
                      0,0,0,0,
                      0,0,0,0,
                      0,0,0,100,
                      0,0,0,200,
                      0,0,0,0]])'''
