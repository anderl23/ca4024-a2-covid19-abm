from pylab import *
import pycxsimulator
import sys
import random 

random.seed(4)

# set m - agents magnitude of movement
if len(sys.argv) > 1:
    m = float(sys.argv[1]) # custom m read from command line
else:
    m = 0.05 # default m

# check if infected agents should be isolated (frozen)
if len(sys.argv) > 2 and sys.argv[2] == 'isolate':
    isolated = 'y'
else:
    isolated = 'n'

N = 1000 # Number of agents
I0 = 1 # Initial number of infected agents
pd = 0.02 # probability of death in infected agent
pt = 0.18 # Probability of transmitting covid to a susceptible agent
it = 14 # max time agent can be of type 'I'
cd = 0.02 # radius for collision detection
cdsq = cd ** 2

class agent:
    pass

def initialize():
    global population,time, agents, infectedData, deathData, infectedDataCum, deathDataCum
    population = N
    time = 0
    agents = []
    for i in range(N):
        ag = agent()
        ag.type = 'I' if i < I0 else 'S'
        ag.m = 0 if i < I0 and isolated == 'y' else m
        ag.t = 0 # time in type state (i.e. 0 days infected -- all agents start at 0)
        ag.x = random.random()
        ag.y = random.random()
        agents.append(ag)

    infectedData = [I0]
    deathData = [N - len(agents)]
    infectedDataCum = [I0]
    deathDataCum = [N - len(agents)]

def observe():
    subplot(1, 2, 1)    
    cla()
    susceptible = [ag for ag in agents if ag.type == 'S']
    if len(susceptible) > 0:
        x = [ag.x for ag in susceptible]
        y = [ag.y for ag in susceptible]
        scatter(x, y, color = 'blue')
    infected = [ag for ag in agents if ag.type == 'I']
    if len(infected) > 0:
        x = [ag.x for ag in infected]
        y = [ag.y for ag in infected]
        scatter(x, y, color='red')
    recovered = [ag for ag in agents if ag.type == 'R']
    if len(recovered) > 0:
        x = [ag.x for ag in recovered]
        y = [ag.y for ag in recovered]
        scatter(x, y, color='green')
    axis('scaled')
    axis([0, 1, 0, 1])
    title('t = ' + str(time))

    subplot(2, 2, 2)
    cla()
    plot(infectedData, color = 'red')
    plot(deathData, color = 'black')
    title('Number of Infected Agents and Deaths at Time "t"')

    subplot(2, 2, 4)
    cla()
    plot(infectedDataCum, color = 'red')
    plot(deathDataCum, color = 'black')
    title('Cumulative No. Infections & Deaths')

def update_one_agent():
    global agents
    if agents == []:
        return

    ag = random.choice(agents)


    # simulating random movement
    m = ag.m ###
    ag.x += random.uniform(-m, m)
    ag.y += random.uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision
    neighbors = [nb for nb in agents if nb.type != ag.type
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]


    # case when agent is type susceptible
    if ag.type == 'S':
        if len(neighbors) > 0: # if there are infected or recovered agents nearby
            infected_neighbors = [nb for nb in neighbors if nb.type == 'I']
            if len(infected_neighbors) > 0 and random.random() < pt: #check if infected nearby and if random probability is less than probability of transmission
                ag.type = 'I' #update agent to infected
                if isolated == 'y': #if isolate is y set m to zero
                    ag.m = 0
                ag.t = 0 # reset t to zero as agent in new type state

    # case when agent  is type infected
    elif ag.type == 'I':
        if random.random() < pd: # check is random probability is less than probabilty of death
            agents.remove(ag) # remove agent because of death
            return
        if ag.t > it: # check if agent has been infected for more than 14 days
            ag.type = 'R' #update agent to recovered
            if isolated == 'y': # if isolated is y allow agent freedom of movement again
                ag.m = 0.05
            ag.t = 0 # reset t to zero as agent in new type state

def update():
    global population, agents, time, susceptibleData, infectedData, recoveredData
    population = len(agents) # current number of agents at time
    for ag in agents:
        ag.t += 1 #update agents time in current type state
    i = 0.
    while i < 1. and len(agents) > 0:
        i += 1. / len(agents)
        update_one_agent()
    time += 1 #increase global time by 1

    susceptible = [ag for ag in agents if ag.type == 'S']
    infected = [ag for ag in agents if ag.type == 'I']
    recovered = [ag for ag in agents if ag.type == 'R']
    
    infectedData.append(len(infected))
    deathData.append(population - len(agents))
    infectedDataCum.append(N - len(susceptible))
    deathDataCum.append(N - len(agents))

    if len(infected) == 0:
        print('T = ' + str(time))
        print('No. Deaths = ' + str(deathDataCum[-1]))
        print('No. Infections = ' + str(infectedDataCum[-1]))
        print('Highest No. Deaths per Day = ' + str(max(deathData)))
        print('Highest No. Infections per Day = ' + str(max(infectedData)))
    return
pycxsimulator.GUI().start(func=[initialize, observe, update])
