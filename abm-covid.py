from pylab import *
import pycxsimulator

import copy as cp


N = 1000 # Number of agents
I0 = 1 # Initial number of infected agents
m = 0.05 # magnitude of movement of agents
pd = 0.02 # probability of death in infected agent
pt = 0.18 # Probability of transmitting covid to a susceptible agent
it = 14 # max time agent can be of type 'I'
cd = 0.02 # radius for collision detection
cdsq = cd ** 2


class agent:
    pass

def initialize():
    global population,time, agents, infectedData, deathData
    population = N
    time = 0
    agents = []
    for i in range(N):
        ag = agent()
        ag.type = 'I' if i < I0 else 'S'
        ag.m = m
        ag.t = 0 # time in type state (i.e. 0 days infected -- all agents start at 0)
        ag.x = random()
        ag.y = random()
        agents.append(ag)

    infectedData = [I0]
    deathData = [N - len(agents)]

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

    subplot(1, 2, 2)
    cla()
    plot(infectedData, color = 'red')
    plot(deathData, color = 'black')
    title('Number of Infected agents and Deaths')

def update_one_agent():
    global agents
    if agents == []:
        return

    ag = choice(agents)

    ag.t += 1 #update agents time in current type state

    # simulating random movement
    m = ag.m ###
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating death or recovery
    neighbors = [nb for nb in agents if nb.type != ag.type
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]


    if ag.type == 'S':
        if len(neighbors) > 0: # if there are infected or recovered agents nearby
            infected_neighbors = [nb for nb in neighbors if nb.type == 'I']
            if len(infected_neighbors) > 0 and random() < pt:
                ag.type = 'I'
                ag.t = 0

    elif ag.type == 'I':
        if random() < pd:
            agents.remove(ag)
            return
        if ag.t > it: # if agent has been infected for more than 14 days and has not died they are considered recovered
            ag.type = 'R'
            ag.t = 0

def update():
    global population, agents, time, susceptibleData, infectedData, recoveredData
    population = len(agents)
    t = 0.
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        update_one_agent()
    time += 1
    infected = [ag for ag in agents if ag.type == 'I']

    infectedData.append(len(infected))
    deathData.append(population - len(agents))

pycxsimulator.GUI().start(func=[initialize, observe, update])