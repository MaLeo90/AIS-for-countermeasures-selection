# Imports
import random

# Global variables
k=1
avg_affinity=10

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
#        self._countermeasure += cm
        self._countermeasures.append(cm) 

#  def __iter__(self):
        ''' Returns the Iterator object '''
'''       
            return AntibodyIterator(self)

class AntibodyIterator:
    def __init__(self, antibody):
        self._antibody = antibody
        self._index = 0

    def __next__(self):
        if self._index < (len(self._antibody._countermeasure)):
            result = self._antibody._countermeasure[self._index]
            self._index +=1
            return result
        raise StopIteration
'''




# Functions definition

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
        if cm.asset_id.id in asset_dict.keys():
            asset_dict[cm.asset_id.id].append(cm)
        else:
            asset_dict[cm.asset_id.id] = []
            asset_dict[cm.asset_id.id].append(cm)
       
    #for key in [key for key in asset_dict if len(asset_dict[key]) == 1]: del asset_dict[key]
    return asset_dict

def determine_affinity(threats, assets, antibodies):
    risk_dict = dict()
    global avg_affinity
    for t in threats:
        print("Threat:", t.id)
        for ass in assets:
           if(t.asset_id == ass.id):
                print("Asset:",ass.id)
                for ant in antibodies:
                    print("Antibody:",ant.id)
                    for cm in ant._countermeasures:
                        if cm.benefit == 1:
                            calculate_benefit(cm)
                    asset_dict = has_equal_element(ant,assets)
                    asset_benefit=calculate_benefit_prep(asset_dict,assets)
                    print(asset_benefit)
                    print("Risk:",calculate_risk(t,ass,asset_benefit[ass.id])) 
                    if ant.id in risk_dict.keys():
                        risk_dict[ant.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
                    else:
                        risk_dict[ant.id]= []
                        risk_dict[ant.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
    
    print(risk_dict)
    total_affinity=0
    for ass in assets:
        for ant.id in risk_dict.keys():
            risk_dict[ant.id][ass.id]=abs(calculate_fitness(risk_dict[ant.id][ass.id],ass))
            total_affinity+=risk_dict[ant.id][ass.id]
    for ant in antibodies:
        ant.fitness=sum(risk_dict[ant.id])
    print("total affinity:", total_affinity)
    print(risk_dict)
    avg_affinity=total_affinity/len(risk_dict)
    print("Avg affinity:",avg_affinity)

def myfunc(e):
    return e.fitness

def clone_antibodies(antibodies):
    antibodies.sort(key=myfunc)
    return antibodies[0:k]

def add_random_cm(clone, cm_tot):
    print("Clone:",clone._countermeasures)
    a = set()
    b = set()
    c = set()
    d = []
    e = set()
    for cm in clone._countermeasures:
        a.add(cm.id)
        c.add(cm.asset_id.id)
        e.add(cm)
    for cm in cm_tot:
        b.add(cm.id)
    add_index=set(b-a)
    cm_to_add = cm_tot[random.choice(tuple(add_index))-1]
    clone.addCountermeasure(cm_to_add)
    '''
    if cm_to_add.benefit != 1:
        if cm_to_add.asset_id.id in c:
            for elem in e:
                if elem.asset_id.id == cm_to_add.asset_id.id:
                    d.append(elem)
            calculate_combined_benefit(d.append(cm_to_add))
    else:
        calculate_benefit(cm_to_add)
    
    print("Clone:",clone._countermeasures)
    '''
def determine_affinity_clone(threats, assets, clones):
    risk_dict = dict()
    for t in threats:
        print("Threat:", t.id)
        for ass in assets:
           if(t.asset_id == ass.id):
                print("Asset:",ass.id)
                for clone in clones:
                    print("Antibody:",clone.id)
                    for cm in clone._countermeasures:
                        if cm.benefit == 1:
                            calculate_benefit(cm)
                    asset_dict = has_equal_element(clone,assets)
                    asset_benefit=calculate_benefit_prep(asset_dict,assets)
                    print(asset_benefit)
                    print("Risk:",calculate_risk(t,ass,asset_benefit[ass.id])) 
                    if clone.id in risk_dict.keys():
                        risk_dict[clone.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
                    else:
                        risk_dict[clone.id]= []
                        risk_dict[clone.id].append(calculate_risk(t,ass,asset_benefit[ass.id]))
    
    print(risk_dict)
    total_affinity=0
    for ass in assets:
        for clone.id in risk_dict.keys():
            risk_dict[clone.id][ass.id]=abs(calculate_fitness(risk_dict[clone.id][ass.id],ass))
            total_affinity+=risk_dict[clone.id][ass.id]
    for clone in antibodies:
        clone.fitness=sum(risk_dict[clone.id])
    print("total affinity:", total_affinity)
    print(risk_dict)
    avg_affinity_clone=total_affinity/len(risk_dict)
    print("Avg affinity clone:", avg_affinity_clone)
    print("Avg affinity total:", avg_affinity) 
    return avg_affinity_clone

def remove_random_cm(clone):
    del clone._countermeasures[random.randint(0,len(clone._countermeasures)-1)]

def modify_random_cm(clone):
    pass

def mutate_clones(clones, cm_tot, threats, assets):
    global k
    for clone in clones:
        P=random.random()
        print(P)
        if(P>0):
            add_random_cm(clone,cm_tot)
        else:
            remove_random_cm(clone)
        if determine_affinity_clone(threats,assets,[clone])>avg_affinity:
            print("remove clone")
            k = k-1
        else:
            print("add clone to solution set")

def replace_antibodies(antibodies):
    antibodies.sort(key=myfunc)
    return antibodies[0:len(antibodies)-k]



# Main program

a1 = asset(0,0.85)
a2 = asset(1,0.7)
t1= threat(0,8.8,0.95,0)
t2= threat(1,7.5,0.7,1)
threats = [t1,t2]
assets = [a1,a2]


cm1 = countermeasure(1,0.7,0.4,0.2,a1)
cm2 = countermeasure(2,0.8,0.7,0.4,a2)
cm3 = countermeasure(3,0.6,0.5,0.5,a1)
cm4 = countermeasure(4,0.5,0.3,0.2,a2)
cm5 = countermeasure(5,0.3,0.1,0.2,a1)
cm6 = countermeasure(6,0.9,0.2,0.2,a2)

cm_a1 = [cm1, cm3, cm5]
cm_a2 = [cm2, cm4, cm6]
cm_tot = cm_a1 + cm_a2
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

antibodies = [ant2]
for ant in antibodies:
    print(ant.id)
    for cm in ant._countermeasures:
        print("cm",cm.id)
    print("___")


determine_affinity(threats, assets, antibodies)
clones = clone_antibodies(antibodies)
mutate_clones(clones,cm_tot, threats, assets)
#mutate_clones(clones,cm_tot)
#print(calculate_risk(t1,a1))
#print(calculate_risk(t1,a1,cm1.benefit))
#print(calculate_fitness(calculate_risk(t1,a1), a1))
