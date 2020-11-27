
# Classes definition

class threat:
    def __init__(self, imp, prob):
        super().__init__()
        self.imp = imp
        self.prob = prob

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
    def __init__(self):
        self._countermeasure = list()

    def addCountermeasure(self, cm):
        self._countermeasure += cm

    def __iter__(self):
        ''' Returns the Iterator object '''
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

# Functions definition

def func(antibody):
    antibody.sort(key=antibody._countermeasure.asset_id)

def calculate_benefit(cm):
    cm.benefit=(9*cm.eff)**(1-(cm.imp+cm.cost)/2)+1

def calculate_combined_benefit(*benefit):
    return (max(*benefit)+min(sum(*benefit),10))/2

def calculate_risk(threat, asset, benefit=1):
    return (threat.prob*threat.imp*asset.criticality)/benefit

def calculate_fitness(risk, asset):
    return risk-10*(1-asset.criticality)

def multiple_cms(antibody):
    i=0
    for cm in antibody:
        ant[i].asset.id

def has_equal_element(antibody1):
    a=[]
    occurences = []
    for cm in antibody1:
        a.append(cm.asset.id)
    for id in a:
        count=0
        for x in a:
            if x == a:
                count +=1
            occurences.append(count)
    duplicates = set()
    index=0
    while index < len(a):
        if occurences[index]!=1:
            duplicates.add(a[index])
        index +=1
    return duplicates

def determine_affinity(threat, asset, antibodies):
    i=0
    for t in threat:
        for ass in asset:
            for ant in antibodies:
                for cm in ant:
                    calculate_benefit(cm)
                if(has_equal_element(ant)!=0):
                    calculate_combined_benefit(ant)
            

# Main program

a1 = asset(1,0.85)
a2 = asset(2,0.7)
t1= threat(8.8,0.95)
t2= threat(7.5,0.7)

cm1 = countermeasure(1,0.7,0.4,0.2,a1)
cm2 = countermeasure(2,0.8,0.7,0.4,a2)
cm3 = countermeasure(3,0.6,0.5,0.5,a1)
cm4 = countermeasure(4,0.5,0.3,0.2,a2)
cm5 = countermeasure(5,0.3,0.1,0.2,a1)
cm6 = countermeasure(6,0.9,0.2,0.2,a2)
print(cm1.cost)
calculate_benefit(cm1)
calculate_benefit(cm2)
calculate_benefit(cm3)
print(calculate_combined_benefit([cm1.benefit,cm2.benefit,cm3.benefit]))
ant1 = antibody()
ant1.addCountermeasure([cm1,cm2])

ant2 = antibody()
ant2.addCountermeasure([cm3,cm4])
ant3 = antibody()
ant3.addCountermeasure([cm5,cm6])
ant4 = [cm1,cm1,cm2,cm2,cm1,cm1]
func(ant1)
antibodies = [ant1,ant2,ant3]
for ant in antibodies:
    for cm in ant:
        print(cm.cost)
for cm in ant4:
    print(cm.asset.criticality)
print(ant4[0].asset.criticality)

print(has_equal_element(ant4))

print(calculate_risk(t1,a1))
print(calculate_risk(t1,a1,cm1.benefit))
print(calculate_fitness(calculate_risk(t1,a1), a1))