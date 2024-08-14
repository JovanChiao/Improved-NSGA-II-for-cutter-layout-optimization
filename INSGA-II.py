import random
import pandas as pd
from deap import base, creator, tools, algorithms
import math

# Changeable variables
NUM_VARIABLES = 25  # Number of cutters
popu = 200  # Population size
gene = 500  # Iteration number
min_radius = 781.5
max_radius = 2808.5

# Fixed variables
NUM_OBJECTIVES = 4
futiao = 6
h = 8
o = 82.5
ot = 4
tao = 15
R = 216
p = 81 * 3.1415926 / 180
T = 17
v = 10 * 3.1415926 / 180
Fa = 250000
fai = math.acos((R - h) / R)
max_ob1 = 360000000
min_ob1 = 100000
max_ob2 = 100000
min_ob2 = 100
max_ob3 = 800
min_ob3 = 0.05
max_ob4 = 300000000
min_ob4 = 60000000
min_angle = 0
max_angle = 360 * 3.1415926 / 180
angle_an = 0
limit_angle = 5
limit_x = 20
limit_y = 20


# Building multi-objective optimization problems
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)


# Population initialization
def generate_individual():
    individual = []

    # Spiral arrangement
    for i in range(futiao):
        for r in range(int(NUM_VARIABLES/futiao)):
            individual.append(((max_radius - min_radius) / (int(NUM_VARIABLES/futiao) + 1)) * (r+1) + i*70 + min_radius)
            individual.append(i*360*3.14/(180*futiao))
        r = 0
    if NUM_VARIABLES % futiao != 0:
        for k in range(NUM_VARIABLES % futiao):
            individual.append(min_radius + (max_radius - min_radius) / int(NUM_VARIABLES/futiao + 1) * int(NUM_VARIABLES/futiao) + (k+1)*60)
            individual.append(k*360*3.14/(180*futiao))


    # # Concentric arrangement
    # for r in range(int(NUM_VARIABLES/futiao)):
    #     for i in range(futiao):
    #         individual.append((max_radius / (NUM_VARIABLES/futiao + 1)) * (r+1) + i*40)
    #         if i * 3 * 45 < 360:
    #             individual.append(i * 3 * 45 * 3.1415926 / 180)
    #         else: individual.append((i * 3 * 45 - 360) * 3.1415926 / 180)
    #     i = r


    # # random arrangement
    # for y in range(NUM_VARIABLES):
    #     individual.append(random.uniform(min_radius, max_radius))
    #     individual.append(random.uniform(min_angle, max_angle))

    return creator.Individual(individual)


# Define the fitness function
def evaluate_individual(individual):
    Vd = []
    radius = []
    for t in range(NUM_VARIABLES):
        radius.append(individual[0 + 2 * t])
    radius.sort()
    Mx = 0
    My = 0
    Fx = 0
    Fy = 0
    for i in range(NUM_VARIABLES):
        if i == 0:
            Ft = 2.12 * R * T * fai * ((radius[1] - radius[0]) * o * o * ot / (fai * math.sqrt(R * T))) ** (1 / 3) / 1.1
        elif i == NUM_VARIABLES - 1:
            Ft = 2.12 * R * T * fai * ((radius[NUM_VARIABLES - 1] - radius[NUM_VARIABLES - 2]) * o * o * ot / (
                        fai * math.sqrt(R * T))) ** (1 / 3) / 1.1
        else:
            Ft = 2.12 * R * T * fai * ((radius[i + 1] - radius[i - 1]) * o * o * ot / (fai * math.sqrt(R * T))) ** (
                        1 / 3) / 1.1
        Fr = Ft * math.sin(fai / 2)
        Fv = Ft * math.cos(fai)
        Fs = (tao / 2) * (R * fai) ** 2 * math.sin(R * fai / (2 * radius[i]))
        Mx += Fv * individual[0 + 2 * i] * math.cos(angle_an) * math.sin(individual[1 + 2 * i]) + \
              Fs * individual[0 + 2 * i] * math.sin(angle_an) * math.sin(individual[1 + 2 * i])
        My += Fv * individual[0 + 2 * i] * math.cos(angle_an) * math.cos(individual[1 + 2 * i]) + \
              Fs * individual[0 + 2 * i] * math.sin(angle_an) * math.cos(individual[1 + 2 * i])
        Fx += Fs * math.cos(angle_an) * math.cos(individual[1 + 2 * i]) + \
              Fr * math.sin(individual[1 + 2 * i]) - \
              Fv * math.sin(angle_an) * math.cos(individual[1 + 2 * i])
        Fy += Fs * math.cos(angle_an) * math.sin(individual[1 + 2 * i]) - \
              Fr * math.cos(individual[1 + 2 * i]) - \
              Fv * math.sin(angle_an) * math.sin(individual[1 + 2 * i])
        if i == 0:
            Vd.append(h * (radius[1] - radius[0]) - (radius[1] - radius[0]) ** 2 / (8 * math.tan(p)))
        elif i == NUM_VARIABLES - 1:
            Vd.append(h * (radius[NUM_VARIABLES - 1] - radius[NUM_VARIABLES - 2]) - (
                        radius[NUM_VARIABLES - 1] - radius[NUM_VARIABLES - 2]) ** 2 / (8 * math.tan(p)))
        else:
            Vd.append(h * (radius[i + 1] - radius[i - 1]) - (
                        (radius[i + 1] - radius[i]) ** 2 + (radius[i] - radius[i - 1]) ** 2) / (8 * math.tan(p)))

    objective1 = math.sqrt(Mx ** 2 + My ** 2)  # overturning moment
    objective2 = math.sqrt(Fx ** 2 + Fy ** 2)  # radial load
    fx3 = 0
    for k in range(NUM_VARIABLES):
        fx3 += (Vd[i] - sum(Vd) / len(Vd)) ** 2
    objective3 = math.sqrt(fx3 / NUM_VARIABLES)  # standard deviation of rock breakage
    objective4 = 0  # cutter dispersion
    r_a = dict()
    for j in range(NUM_VARIABLES):
        r_a["{}".format(individual[0 + j * 2])] = [individual[1 + j * 2]]
    for k in range(NUM_VARIABLES - 1):
        objective4 += radius[k] ** 2 + radius[k + 1] ** 2 - 2 * radius[k] * radius[k + 1] * math.cos(
            r_a["{}".format(radius[k + 1])][0] - r_a["{}".format(radius[k])][0])

    # Setting up constraints
    constrain = constrain_violaitons(individual)
    objective1_nor = (objective1 - min_ob1) / (max_ob1 - min_ob1)
    objective2_nor = (objective2 - min_ob2) / (max_ob2 - min_ob2)
    objective3_nor = (objective3 - min_ob3) / (max_ob3 - min_ob3)
    objective4_nor = (objective4 - min_ob4) / (max_ob4 - min_ob4)
    if False in constrain:
        return 1, 1, 1, 0
    else:
        return objective1_nor, objective2_nor, objective3_nor, objective4_nor

# Calculation of the degree of constraint violation
def constrain_violaitons(individual):
    cv = []
    radius = []
    r_ana = dict()
    for j in range(NUM_VARIABLES):
        r_ana["{}".format(individual[0 + j * 2])] = [individual[1 + j * 2]]
    for t in range(NUM_VARIABLES):
        radius.append(individual[0 + 2 * t])
    radius.sort()

    # Center of mass position deviation less than the allowable error
    X, Y = 0, 0
    for i in range(NUM_VARIABLES):
        X += individual[0 + 2 * i] * math.cos(individual[1 + 2 * i]) / NUM_VARIABLES
        Y += individual[0 + 2 * i] * math.sin(individual[1 + 2 * i]) / NUM_VARIABLES
    if abs(X) > limit_x or abs(Y) > limit_y:
        cv.append(False)
    else:
        cv.append(True)

    # Cutter spacing meets requirements
    for t in range(NUM_VARIABLES - 1):
        if radius[i+1]-radius[i] < T or radius[i+1]-radius[i] > 2*h*math.tan(p):
            cv.append(2)
        elif radius[t + 1] - radius[t] > 2 * h * math.tan(p):
            cv.append(False)
        else:
            cv.append(True)

    # Individual Cutter load capacity meets requirements
    Fv = 4 * o * h * math.sqrt(2 * R * h - h * h) * math.tan(v / 2)
    if Fv > Fa:
        cv.append(False)
    else:
        cv.append(True)

    # Cutter do not interfere with each other
    for i in range(NUM_VARIABLES - 1):
        if radius[i] * abs(r_ana["{}".format(radius[i + 1])][0] - r_ana["{}".format(radius[i])][0]) < limit_angle:
            cv.append(False)
        else:
            cv.append(True)

    return cv


# Creating Population
lower_bound = [min_radius, min_angle] * NUM_VARIABLES
upper_bound = [max_radius, max_angle] * NUM_VARIABLES
toolbox = base.Toolbox()
toolbox.register("individual", generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_individual)
individual = toolbox.individual()
toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta=20.0, low=lower_bound, up=upper_bound)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=20.0, low=lower_bound, up=upper_bound,
                 indpb=1.0 / len(individual))
toolbox.register("select", tools.selNSGA2)


# Execute the NSGA algorithm
pop = toolbox.population(n=popu)
invalid_ind = [ind for ind in pop if not ind.fitness.valid]
fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

for ind, fit in zip(invalid_ind, fitnesses):
    ind.fitness.values = fit

# Begin the generational process
for gen in range(1, gene):
    offspring = algorithms.varAnd(pop, toolbox, cxpb=0.6, mutpb=0.5)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Select the next generation population from parents and offspring
    pop = toolbox.select(pop + offspring, popu)

# Getting and saving Optimization Results
pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
objectvalue = []
decisionva = []
for ind in pop:
    objectvalue.append(ind.fitness.values)
    decisionva.append(ind)
dataout = pd.DataFrame(data={"object": objectvalue,
                             "decision": decisionva})
dataout.to_csv('..\INSGA2.csv')
