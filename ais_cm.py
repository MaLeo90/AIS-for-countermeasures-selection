#Global variables
k=1
#avg_fitness=10

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
    for t in threats:
        print("Threat:", t.id)
        for ass in assets:
           if(t.asset_id == ass.id):
                print("Asset:",ass.id)
                for ant in antibodies:
                    print("Antibody:",ant.id)
                    for cm in ant._countermeasures:
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
            risk_dict[ant.id][ass.id-1]=abs(calculate_fitness(risk_dict[ant.id][ass.id-1],ass))
            total_affinity+=risk_dict[ant.id][ass.id-1]
    for ant.id in risk_dict.keys():
        antibodies[ant.id].fitness=sum(risk_dict[ant.id])
    print(total_affinity)
    print(risk_dict)
    avg_affinitity=total_affinity/len(risk_dict)
    print("Avg affinity:",avg_affinitity)
    for ant in antibodies:
        print(ant.id)
        print(ant.fitness)

def myfunc(e):
    return e.fitness

def clone_antibodies(antibodies):
    for ant in antibodies:
        print(ant.fitness)
    antibodies.sort(key=myfunc)
    for ant in antibodies:
        print(ant.fitness)
    

# Main program

a1 = asset(1,0.85)
a2 = asset(2,0.7)
t1= threat(1,8.8,0.95,1)
t2= threat(2,7.5,0.7,2)
threats = [t1,t2]
assets = [a1,a2]


cm1 = countermeasure(1,0.7,0.4,0.2,a1)
cm2 = countermeasure(2,0.8,0.7,0.4,a2)
cm3 = countermeasure(3,0.6,0.5,0.5,a1)
cm4 = countermeasure(4,0.5,0.3,0.2,a2)
cm5 = countermeasure(5,0.3,0.1,0.2,a1)
cm6 = countermeasure(6,0.9,0.2,0.2,a2)
#print(cm1.cost)
#print(calculate_combined_benefit([cm1.benefit,cm2.benefit,cm3.benefit]))
ant1 = antibody(1)

ant1.addCountermeasure(cm1)
ant1.addCountermeasure(cm2)

ant2 = antibody(2)
ant2.addCountermeasure(cm3)
ant2.addCountermeasure(cm4)
ant3 = antibody(3)
ant3.addCountermeasure(cm5)
ant3.addCountermeasure(cm6)

antibodies = [ant2,ant1,ant3]
for ant in antibodies:
    print(ant.id)
    for cm in ant._countermeasures:
        print("cm",cm.id)
    print("___")

determine_affinity(threats, assets, antibodies)
clone_antibodies(antibodies)
#print(calculate_risk(t1,a1))
#print(calculate_risk(t1,a1,cm1.benefit))
#print(calculate_fitness(calculate_risk(t1,a1), a1))