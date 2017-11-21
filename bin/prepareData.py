import re

##  --------------------------------- 
##  ages-group: per decade.  
##  for someone in their 20s, return "20"
##  -1 if no age known
def ageGroup(n):
    try:
        return int(int(n/10)*10)
    except ValueError:
        return -1

##  -------------------------------------------
##  convert deck letter to numerical value 
##  (A closer to deck than G).
##  -1 if not known
def deck(c):
    cabin_list = ['A', 'B', 'C', 'D', 'E', 'F', 'T', 'G']
    try:
        return cabin_list.index(c[0])
    except:
        return -1

##  -------------------------------------------
##  stipped out with regex and normalised
def passengerTitle(n):
    titles = {
        'Capt': '0',       'Col': '0',
        'Don': '0',        'Dr': '0',
        'Jonkheer': '0',   'Lady': '1',
        'Major': '0',      'Master': '0',
        'Miss': '2',     'Mlle': '2',
        'Mme': '1',       'Mr': '0',
        'Mrs': '1',       'Ms': '2',
        'Rev': '0',        'Sir': '0',
        'Countess': '1',  'Dona': '1'
    }

    m = re.search(r' ([a-zA-Z]+)\.', n)
    t = m.group(1)
    return titles[t]

##  -------------------------------------------
##  normalise genders
##  -1 if not known
def passengerGender(s):
    if s == 'male':
        return 1
    elif s == 'female':
        return 0
    else:
        return -1

##  -------------------------------------------
##  normalise the ports of embarkation.
def normalisePort(p):
    ports = {
        'C':0,
        'Q':1,
        'S':2
    }
    try:
        return ports[p]
    except KeyError:
        return -1


##  ----------------
##  do all the things and return the dataSets
def prepare(dataSets):

    ##  -------------------------------------------
    ##  add some features to the dataSets
    for dataSet in dataSets:
        dataSet['AgeGroup']   = dataSet['Age'].map(lambda x: ageGroup(x))
        dataSet['Deck']       = dataSet['Cabin'].map(lambda x: deck(x))
        dataSet['Title']      = dataSet['Name'].map(lambda n: passengerTitle(n))
        dataSet['Gender']     = dataSet['Sex'].map(lambda s: passengerGender(s))
        dataSet['FamilySize'] = dataSet['Parch'] + dataSet['SibSp']
        dataSet['Port']       = dataSet['Embarked'].map(lambda p: normalisePort(p))
        dataSet['Class']      = dataSet['Pclass']

    return dataSets