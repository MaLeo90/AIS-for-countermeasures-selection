# Imports
import random
import copy

# Global variables
k=4
avg_affinity=10
cardinality_solution=0
N_antibodies=20
N_assets=5
N_cms_per_asset=10
N_cms=N_assets*N_cms_per_asset
N_threats=5
N_iterations=100

# Classes definition

class threat:
    def __init__(self, id, imp, prob, asset_id):
        super().__init__()
        self.id=id
        self.imp = imp
        self.prob = prob
        self.asset_id=asset_id

class asset:
    def __init__(self, id, criticality):
        super().__init__()
        self.id=id
        self.criticality = criticality


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

class antibody:
    def __init__(self, id, fitness=10):
        self._countermeasures = list()
        self.id = id
        self.fitness=fitness

    def addCountermeasure(self, cm):
        self._countermeasures.append(cm) 

# Functions definition

def generate_assets(N_assets):
    id = 0
    assets = []
    while(id<N_assets):
        a = asset(id,random.uniform(0.5,1))
        assets.append(a)
        id+=1
    return assets

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

def generate_threats(N_threats,assets):
    id = 0
    threats = []
    a_id = set()
    for a in assets:
        a_id.add(a.id)
    while (id<N_threats):
        x = random.sample(a_id,1)
        t = threat(id,random.uniform(5,10),random.uniform(0.5,1),x[0])
        a_id.remove(x[0])
        threats.append(t)
        id+=1
    return threats

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

def calculate_benefit(cm):
    cm.benefit=(9*cm.eff)**(1-(cm.imp+cm.cost)/2)+1
    
def calculate_combined_benefit(cm_list):
    max_value=0
    sum_value=0
    for cm in cm_list:
        sum_value+=cm.benefit
        if(cm.benefit>max_value):
            max_value=cm.benefit
    return (max_value+min(sum_value,10))/2

def calculate_risk(threat, asset, benefit=1):
    return (threat.prob*threat.imp*asset.criticality)/benefit

def calculate_fitness(risk, asset):
    return risk-10*(1-asset.criticality)

def calculate_benefit_prep(asset_dict,assets):
    asset_benefit=dict()

    for asset in assets:
        asset_benefit[asset.id]=1

    for asset_id in asset_dict.keys():
        asset_benefit[asset_id] = 0
        asset_benefit[asset_id]=calculate_combined_benefit(asset_dict[asset_id])

    return asset_benefit


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

def determine_affinity(threats, assets, antibodies):
    risk_dict = dict()
    global avg_affinity
    for t in threats:
        #print("Threat:", t.id)
        for ass in assets:
           if(t.asset_id == ass.id):
                #print("Asset:",ass.id)
                for ant in antibodies:
                    if (ant.fitness==10):
                        #print("Antibody:",ant.id)
                        for cm in ant._countermeasures:
                            if cm.benefit == 1:
                                calculate_benefit(cm)
                        asset_dict = has_equal_element(ant,assets)
                        asset_benefit=calculate_benefit_prep(asset_dict,assets)
                        #print(asset_benefit)
                        #print("Risk:",calculate_risk(t,ass,asset_benefit[ass.id])) 
                        if ant.id in risk_dict.keys():
                            risk_dict[ant.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
                        else:
                            risk_dict[ant.id]= []
                            risk_dict[ant.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
    
    #print(risk_dict)
    total_affinity=0
    for t in threats:
        for ass in assets:
            if(t.asset_id==ass.id):
                for ant.id in risk_dict.keys():
                    risk_dict[ant.id][ass.id]=abs(calculate_fitness(risk_dict[ant.id][ass.id],ass))
            #total_affinity+=risk_dict[ant.id][ass.id]
    for ant in antibodies:
        if(ant.fitness==10):
            ant.fitness=sum(risk_dict[ant.id])
        total_affinity+=ant.fitness
    print("total affinity:", total_affinity)
    #print(risk_dict)
    avg_affinity=total_affinity/len(antibodies)
    print("Avg affinity:",avg_affinity)

def myfunc(e):
    return e.fitness

def clone_antibodies(antibodies):
    antibodies.sort(key=myfunc)
    clones = copy.deepcopy(antibodies[0:k])
    return clones

def determine_affinity_clone(threats, assets, clone):
    risk_dict = dict()
    for t in threats:
        #print("Threat:", t.id)
        for ass in assets:
           if(t.asset_id == ass.id):
                #print("Asset:",ass.id)
                #print("Clone:",clone.id)
                for cm in clone._countermeasures:
                    if cm.benefit == 1:
                        calculate_benefit(cm)
                asset_dict = has_equal_element(clone,assets)
                asset_benefit=calculate_benefit_prep(asset_dict,assets)
                #print(asset_benefit)
                #print("Risk:",calculate_risk(t,ass,asset_benefit[ass.id])) 
                if clone.id in risk_dict.keys():
                    risk_dict[clone.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
                else:
                    risk_dict[clone.id]= []
                    risk_dict[clone.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
    
    #print(risk_dict)
    avg_affinity_clone=0
    for t in threats:
        for ass in assets:
            if(t.asset_id==ass.id):
                risk_dict[clone.id][ass.id]=abs(calculate_fitness(risk_dict[clone.id][ass.id],ass))
                avg_affinity_clone+=risk_dict[clone.id][ass.id]
    clone.fitness=sum(risk_dict[clone.id])
    #print(risk_dict)
    print("Avg affinity clone:", avg_affinity_clone)
    print("Avg affinity total:", avg_affinity) 
    return avg_affinity_clone

def add_random_cm(clone, cm_tot, threats):
    a=set()
    for t in threats:
            for cm in cm_tot:
                if cm.asset_id==t.asset_id and cm not in clone._countermeasures:
                    a.add(cm)
    cm_to_add=random.sample(a,1)
    clone.addCountermeasure(cm_to_add[0])

def remove_random_cm(clone):
    del clone._countermeasures[random.randint(0,len(clone._countermeasures)-1)]

def modify_random_cm(clone):
    pass

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
            print("remove clone")
            k = k-1
        else:
            print("add clone to solution set")
            clone.id=cardinality_solution
            antibodies.append(clone)
            cardinality_solution+=1

def replace_antibodies(antibodies, threats, cm_tot):
    antibodies.sort(key=myfunc)
    antibodies_reduced = copy.deepcopy(antibodies[0:(len(antibodies)-k)])
    antibodies_new = generate_antibodies(k, threats, cm_tot)
    return antibodies_reduced + antibodies_new



# Main program
random.seed()

assets = generate_assets(N_assets)
for ass in assets:
    print("Asset:", ass.id)
    print("Asset crit:", ass.criticality)

threats = generate_threats(N_threats,assets)
for t in threats:
    print("Threat:", t.id)
    print("Threat prob:", t.prob)
    print("Threat imp:", t.imp)
    print("Asset Threatened:", t.asset_id) 

countermeasures = generate_countermeasures(N_cms, assets) 
for cm in countermeasures:
    print("cm:", cm.id)
    print("cm eff:", cm.eff)
    print("cm imp:", cm.imp)
    print("cm cost:", cm.cost)
    print("cm asset:", cm.asset_id)

antibodies = generate_antibodies(N_antibodies, threats, countermeasures)
for ant in antibodies:
    print("antibody:", ant.id)
    for cm in ant._countermeasures:
        print("cm:", cm.id)
'''
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
tot = 0
for t in threats:
    for a in assets:
        tot+=calculate_risk(t,a)
print("Initial total risk:",tot)
i = 0
while (i<N_iterations):
    print("Iteration:", i)
    determine_affinity(threats, assets, antibodies)
    clones = clone_antibodies(antibodies)
    mutate_clones(antibodies, clones, countermeasures, threats, assets)
    solution = replace_antibodies(antibodies, threats, countermeasures)
    i+=1
    
print("Better solution:")
print(solution[0].fitness)
for cm in solution[0]._countermeasures:
    print(cm.id)