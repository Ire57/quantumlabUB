import numpy as np
import matplotlib.pyplot as plt
from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel

#Number of cities
n = 10


#Set one decimal random coordinates for the cities in a 100x100 map
cities = np.random.randint(0,1000,(n,2))/10.
cities_list = list(range(n))
time_list = list(range(n))
print(cities_list)

#Create the variables
x = [[[[f'x_{i}_{j}_{t}'] for t in time_list] for j in cities_list] for i in cities_list]

#Calculate the distance between cities
distance = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        distance[i][j] = np.sqrt((cities[i][0]-cities[j][0])**2 + (cities[i][1]-cities[j][1])**2)
        
#Give the diagonal a big value
for i in range(n):
    distance[i][i] = 10000


#Represent the cities in a map and save it to png file
plt.plot(cities[:,0],cities[:,1],'o')
plt.xlim(0,100)
plt.ylim(0,100)
plt.savefig('cities.png')

bqm = BinaryQuadraticModel('BINARY')

#Solving the TSP problem with the D-Wave system
#Add the variables to the BQM
for i in range(n):
    for j in range(n):
        for t in range(n):
            bqm.add_variable(x[i][j][t], distance[i][j])

#Add the constraints to the BQM
for i in range(n):
    c1 = [(x[i][j][t],1) for j in range(n) for t in range(n)]
    bqm.add_linear_equality_constraint(c1,
                                    constant = -1,
                                    lagrange_multiplier = 1000)
    
for j in range(n):
    c2 = [(x[i][j][t],1) for i in range(n) for t in range(n)]
    bqm.add_linear_equality_constraint(c2,
                                    constant = -1,
                                    lagrange_multiplier = 1000)
    
#Once the traveller has visited a city, he can't visit it again
for i in range(n):
    c3 = [( ((x[i][j][t])*(x[k][i][l])), 1 ) for j in range(n) for k in range(n) for t in range(n) for l in range(t+1,n)]
    bqm.add_linear_equality_constraint(c3,
                                    constant = -1,
                                    lagrange_multiplier = 1000)

#Set the D-Wave system
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(bqm, num_reads=1000)

#Print the results
for datum in response.data(['sample', 'energy', 'num_occurrences']):
    print(datum.sample, "Energy: ", datum.energy, "Occurrences: ", datum.num_occurrences)

#Save the final results in a matrix
final = np.zeros((n,n))
for datum in response.data(['sample', 'energy', 'num_occurrences']):
    for i in range(n):
        for j in range(n):
            for t in range(n):
                if datum.sample[x[i][j][t]] == 1:
                    final[i][j] = t+1

#Print the final matrix
print(final)

#Plot the final route
plt.plot(cities[:,0],cities[:,1],'o')
for i in range(n):
    for j in range(n):
        if final[i][j] == 1:
            plt.plot([cities[i][0],cities[j][0]],[cities[i][1],cities[j][1]],'k-')
plt.xlim(0,100)
plt.ylim(0,100)
plt.savefig('route.png')
