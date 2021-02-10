# Imports
import random
import copy
import time
import sys


# Global variables
avg_affinity=10 # average affinity of the antibodies in the solution set
cardinality_solution=0 # number of individuals in the solution set
N_antibodies=20 # number of antibodies in the current run
N_assets=20 # number of affected assets in the current run
N_cms_per_asset=20 # number of countermeasures per asset in the current run
N_cms=N_assets*N_cms_per_asset # total number of countermeasures in the current run
N_threats=N_assets # number of threats in the current run (1 per asset)
N_iterations=200 # number of iterations of the algorithm in the current run
k=N_antibodies//3 # cloning factor in the current run

# Classes definition

# Class Threat(ID, impact, probability, associated asset)
class threat:
    def __init__(self, id, imp, prob, asset_id):
        super().__init__()
        self.id=id
        self.imp = imp
        self.prob = prob
        self.asset_id=asset_id

# Class Asset(ID, criticality)
class asset:
    def __init__(self, id, criticality):
        super().__init__()
        self.id=id
        self.criticality = criticality

# Class Countermeasure(ID, effectiveness, impact, cost, associated asset, benefit, maturity)
# Important: maturity calculation has not been implemented in the current version
class countermeasure:
    def __init__(self, id, eff, imp, cost, asset_id, benefit=1, maturity=0):
        super().__init__()
        self.id = id
        self.eff = eff
        self.imp = imp
        self.cost = cost
        self.asset_id = asset_id
        self.benefit = benefit
        self.maturity = maturity

# Class Antibody (ID, total fitness)
# Contains a support function to add countermeasure to the antibody object
class antibody:
    def __init__(self, id, fitness=10):
        self._countermeasures = list()
        self.id = id
        self.fitness=fitness

    def addCountermeasure(self, cm):
        self._countermeasures.append(cm) 

# Functions definition

# Function to generate random assets
# A low value of criticality forces low risk values
def generate_assets(N_assets):
    id = 0
    assets = []
    while(id<N_assets):
        a = asset(id,random.uniform(0.5,1))
        assets.append(a)
        id+=1
    return assets

# Function to generate random countermeasures
# Each generated countermeasures is assigned to a specific asset
def generate_countermeasures(N_countermeasures,assets):
    id = 0
    i = 0
    cms = []
    a_id = set()
    for a in assets:
        a_id.add(a.id)
    while (id<N_countermeasures):
        x = random.sample(a_id,1)
        while(i < N_cms_per_asset):
            cm = countermeasure(id,random.random(),random.random(),random.random(),x[0])
            cms.append(cm)
            id+=1
            i+=1
        i=0
        a_id.remove(x[0])
    return cms

# Function to generate random threats
# Each generated threat is associated to a specific asset
# Low values of probability/impact forces low risk values
def generate_threats(N_threats,assets):
    id = 0
    threats = []
    a_id = set()
    for a in assets:
        a_id.add(a.id)
    while (id<N_threats):
        x = random.sample(a_id,1)
        t = threat(id,random.uniform(0,10),random.uniform(0.5,1),x[0])
        a_id.remove(x[0])
        threats.append(t)
        id+=1
    return threats

# Function to generate random antibodies
# Each antibody contains at least one countermeasure for each asset associated with a threat
def generate_antibodies(num_antibodies, threats, cm_tot):
    i=0
    antibodies = []
    global cardinality_solution
    while(i<num_antibodies):
        ant = antibody(cardinality_solution)
        a = set()
        for t in threats:
            for cm in cm_tot:
                if cm.asset_id==t.asset_id:
                    a.add(cm)
            cm_to_add=random.sample(a,1)
            ant.addCountermeasure(cm_to_add[0])
            a = set()
        antibodies.append(ant) 
        i+=1
        cardinality_solution+=1
    return antibodies

# Function to calculate the benefit of a single countermeasure
def calculate_benefit(cm):
    cm.benefit=(9*cm.eff)**(1-(cm.imp+cm.cost)/2)+1
    
# Function to calculate the combined benefit of multiple countermeasures
def calculate_combined_benefit(cm_list):
    max_value=0
    sum_value=0
    for cm in cm_list:
        sum_value+=cm.benefit
        if(cm.benefit>max_value):
            max_value=cm.benefit
    return (max_value+min(sum_value,10))/2

# Function to calculate the current risk ratio
def calculate_risk(threat, asset, benefit=1):
    return (threat.prob*threat.imp*asset.criticality)/benefit

# Function to calculate the fitness
# In the current version, one asset can expose one threat at time
def calculate_fitness(risk, asset):
    return risk-10*(1-asset.criticality)

# Support function to calculate the combined benefit
def calculate_benefit_prep(asset_dict,assets):
    asset_benefit=dict()

    for asset in assets:
        asset_benefit[asset.id]=1

    for asset_id in asset_dict.keys():
        asset_benefit[asset_id] = 0
        asset_benefit[asset_id]=calculate_combined_benefit(asset_dict[asset_id])

    return asset_benefit

# Support function to calculate if an antibody has more than a countermeasure applied on the same asset
def has_equal_element(antibody, assets):
    asset_dict = dict() 

    for cm in antibody._countermeasures:
        if cm.asset_id in asset_dict.keys():
            asset_dict[cm.asset_id].append(cm)
        else:
            asset_dict[cm.asset_id] = []
            asset_dict[cm.asset_id].append(cm)
       
    #for key in [key for key in asset_dict if len(asset_dict[key]) == 1]: del asset_dict[key]
    return asset_dict

# Function to determine the affinity of the generated antibodies
def determine_affinity(threats, assets, antibodies):
    risk_dict = dict()
    global avg_affinity
    for t in threats:
        for ass in assets:
           if(t.asset_id == ass.id):
                for ant in antibodies:
                    if (ant.fitness==10): # if the antibody fitness has not been calculated before
                        for cm in ant._countermeasures:
                            if cm.benefit == 1: # if the countermeasure benefit has not been calculated before
                                calculate_benefit(cm)
                        asset_dict = has_equal_element(ant,assets)
                        asset_benefit=calculate_benefit_prep(asset_dict,assets) 
                        if ant.id in risk_dict.keys(): # risk calculation
                            risk_dict[ant.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
                        else:
                            risk_dict[ant.id]= []
                            risk_dict[ant.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
    
    # affinity calculation
    total_affinity=0
    for t in threats:
        for ass in assets:
            if(t.asset_id==ass.id):
                for ant.id in risk_dict.keys():
                    risk_dict[ant.id][ass.id]=abs(calculate_fitness(risk_dict[ant.id][ass.id],ass))
    for ant in antibodies:
        if(ant.fitness==10):
            ant.fitness=sum(risk_dict[ant.id])
        total_affinity+=ant.fitness
    avg_affinity=total_affinity/len(antibodies)

# Support function to sort antibodies based on the affinity
def myfunc(e):
    return e.fitness

# Function to clone the antibodies based on the affinity
def clone_antibodies(antibodies):
    antibodies.sort(key=myfunc)
    clones = copy.deepcopy(antibodies[0:k])
    return clones

# Function to determine the affinity of a clone (similar to the one for antibodies)
def determine_affinity_clone(threats, assets, clone):
    risk_dict = dict()
    for t in threats:
        for ass in assets:
           if(t.asset_id == ass.id):
                for cm in clone._countermeasures:
                    if cm.benefit == 1:
                        calculate_benefit(cm)
                asset_dict = has_equal_element(clone,assets)
                asset_benefit=calculate_benefit_prep(asset_dict,assets)
                if clone.id in risk_dict.keys():
                    risk_dict[clone.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
                else:
                    risk_dict[clone.id]= []
                    risk_dict[clone.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
    
    avg_affinity_clone=0
    for t in threats:
        for ass in assets:
            if(t.asset_id==ass.id):
                risk_dict[clone.id][ass.id]=abs(calculate_fitness(risk_dict[clone.id][ass.id],ass))
                avg_affinity_clone+=risk_dict[clone.id][ass.id]
    clone.fitness=sum(risk_dict[clone.id])
    return avg_affinity_clone

# Mutation functions
# Function to add a random countermeasure to the clone
def add_random_cm(clone, cm_tot, threats):
    a=set()
    for t in threats:
            for cm in cm_tot:
                if cm.asset_id==t.asset_id and cm not in clone._countermeasures:
                    a.add(cm)
    cm_to_add=random.sample(a,1)
    clone.addCountermeasure(cm_to_add[0])

# Function to remove a random countermeasure to the clone
def remove_random_cm(clone):
    del clone._countermeasures[random.randint(0,len(clone._countermeasures)-1)]

# Function to modify the parameters of a random countermeasure of the clone
# In the current version, it is not implemented yet
def modify_random_cm(clone):
    pass

# Function to mutate the clones
def mutate_clones(antibodies, clones, cm_tot, threats, assets):
    global k
    global cardinality_solution
    for clone in clones:
        P=random.random()
        if(P>0.50):
            add_random_cm(clone,cm_tot,threats)
        else:
            if(len(clone._countermeasures)>0):
                remove_random_cm(clone)
        if determine_affinity_clone(threats,assets,clone)>avg_affinity:
            pass
            # remove clone
        else:
            # add clone to solution set
            clone.id=cardinality_solution
            antibodies.append(clone)
            cardinality_solution+=1
            k=k+1

# Function to recalculate the antibodies set for the next iteration of the algorithm
def replace_antibodies(antibodies, threats, cm_tot):
    antibodies.sort(key=myfunc)
    antibodies_reduced = copy.deepcopy(antibodies[0:(N_antibodies-k)])
    antibodies_new = generate_antibodies(k, threats, cm_tot)
    return antibodies_reduced + antibodies_new


# Main program

random.seed()

assets = generate_assets(N_assets)
'''
for ass in assets:
    print("Asset:", ass.id)
    print("Asset crit:", ass.criticality)
'''

threats = generate_threats(N_threats,assets)
'''
for t in threats:
    print("Threat:", t.id)
    print("Threat prob:", t.prob)
    print("Threat imp:", t.imp)
    print("Asset Threatened:", t.asset_id) 
'''

countermeasures = generate_countermeasures(N_cms, assets) 
'''
for cm in countermeasures:
    print("cm:", cm.id)
    print("cm eff:", cm.eff)
    print("cm imp:", cm.imp)
    print("cm cost:", cm.cost)
    print("cm asset:", cm.asset_id)
'''

antibodies = generate_antibodies(N_antibodies, threats, countermeasures)
'''
for ant in antibodies:
    print("antibody:", ant.id)
    for cm in ant._countermeasures:
        print("cm:", cm.id)


# paper toy example (Section 4C)

a1 = asset(0,0.85)
a2 = asset(1,0.7)
#a3 = asset(2,0.5)
t1= threat(0,8.8,0.95,0)
t2= threat(1,7.5,0.7,1)
threats = [t1,t2]
assets = [a1,a2]


cm1 = countermeasure(1,0.7,0.4,0.2,0)
cm2 = countermeasure(2,0.8,0.7,0.4,1)
cm3 = countermeasure(3,0.6,0.5,0.5,0)
cm4 = countermeasure(4,0.5,0.3,0.2,1)
cm5 = countermeasure(5,0.3,0.1,0.2,0)
cm6 = countermeasure(6,0.5,0.3,0.5,1)
cm7 = countermeasure(7,0.8,0.5,0.8,0)
cm8 = countermeasure(8,0.7,0.3,0.7,1)
cm9 = countermeasure(9,0.3,0.3,0.1,0)
cm10 = countermeasure(10,1,0,0,1)
cm11 = countermeasure(11,1,0,0,0)

calculate_benefit(cm10)
calculate_benefit(cm11)

print("Benefit 10",cm10.benefit)
print("Benefit 11",cm11.benefit)

cm_a1 = [cm1, cm3, cm5, cm7, cm9, cm11]
cm_a2 = [cm2, cm4, cm6, cm8, cm10]
countermeasures = cm_a1 + cm_a2
#print(cm1.cost)
#print(calculate_combined_benefit([cm1.benefit,cm2.benefit,cm3.benefit]))

ant1 = antibody(0)

ant1.addCountermeasure(cm1)
ant1.addCountermeasure(cm2)

ant2 = antibody(1)
ant2.addCountermeasure(cm3)
ant2.addCountermeasure(cm4)
ant3 = antibody(2)
ant3.addCountermeasure(cm5)
ant3.addCountermeasure(cm6)

ant4 = antibody(3)
ant4.addCountermeasure(cm7)
ant4.addCountermeasure(cm8)

ant5 = antibody(4)
ant5.addCountermeasure(cm11)
ant5.addCountermeasure(cm10)

antibodies = [ant1,ant2,ant3,ant4,ant5]

for ant in antibodies:
    print("antibody:")
    for cm in ant._countermeasures:
        print(cm.id)
'''
# Calculating the parameters before the execution of the AIS algorithm
tot_risk = 0
tot_fitness = 0
risk=0
fitness=0
fit = []
e_time = []
for t in threats:
    for a in assets:
       if(t.asset_id==a.id):
            risk=calculate_risk(t,a)
            fitness=calculate_fitness(risk,a)
            tot_risk+=risk
            tot_fitness+=fitness

fit.append(tot_fitness/N_assets)
i = 0
start_time = time.time()

while (i<N_iterations):
    k=N_antibodies//3
    determine_affinity(threats, assets, antibodies)
    clones = clone_antibodies(antibodies)
    mutate_clones(antibodies, clones, countermeasures, threats, assets)
    solution = replace_antibodies(antibodies, threats, countermeasures)
    i+=1

exec_time= time.time() - start_time
'''
print("Better solution:")
print(solution[0].fitness) # solution[0] contains the best antibody
for cm in solution[0]._countermeasures:
    print(cm.id)
'''

# printing statement
#print(tot_risk, tot_fitness, solution[0].fitness,exec_time, N_assets, N_antibodies, N_threats, N_iterations, N_cms, N_antibodies//3, sep="," )
#print("Exec time: ",exec_time)
print("Fitness_best_solution: ",solution[0].fitness/N_assets) # To normalize fitness between [0,10], it is divided by the number of assets