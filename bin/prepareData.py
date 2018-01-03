## Series of functions to munge the data and add features to the dataset
##
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
        # men
        'Master':   '0',
        'Mr':       '0',
        'Don':      '0',
        'Dr':       '0',
        'Rev':      '0',

        # ladies
        'Mrs':      '1',
        'Mme':      '1',
        'Dona':     '1',

        # young ladies
        'Miss':     '2',
        'Mlle':     '2',
        'Ms':       '2',

        # military
        'Major':    '3',
        'Capt':     '3',
        'Col':      '3',

        # poshos
        'Jonkheer': '4',
        'Sir':      '4',
        'Lady':     '4',
        'Countess': '4',
    }

    m = re.search(r' ([a-zA-Z]+)\.', n)
    t = m.group(1)
    return titles[t]


##  ------------------------------------------
##  take the whole dataset and calculate the fares 
##  if missing.
##  return a list of values.
def normaliseFares(ds):

    # we'll return a list of the fares once they have been normalised
    normalisedFares = []

    # average out the ticket fares that appear twice.
    # count up how many duplicated tickets are there:
    ticket_count = {}
    for ticket_number in ds['Ticket']:
        # add tickets to ticket_count...
        if ticket_number not in ticket_count:
            ticket_count[ticket_number] = 0
        # ...and count them
        ticket_count[ticket_number] += 1

    # fill NaN (Not a Number) with zeros
    ds = ds.fillna(value={'Fare': 0})

    # loop through our dataset
    for index, row in ds.iterrows():
        
        fare   = row['Fare']
        ticket = row['Ticket']
        pclass = row['Pclass']

        # if there is a value, divide it by the number of corresponding 
        # tickets to get average ticket price
        if fare > 0:
            normalisedFare = fare / ticket_count[ticket]
        else:
            normalisedFare = fare

        # normalise to approx ticket bands:
        if normalisedFare <= 7.91:
            nf = 1
        elif normalisedFare <= 14.454:
            nf = 2
        elif normalisedFare <= 31:
            nf = 3
        else:
            nf = 4

        normalisedFares.append(nf)

    return normalisedFares


##  ----------------
##  do all the things and return the dataSets
def prepare(dataSets):

    ##  -------------------------------------------
    ##  add some features to the dataSets
    for dataSet in dataSets:
        
        dataSet['Deck'] = dataSet['Cabin'].map(lambda x: deck(x))

        # fill missing data in Embarked with an X so we can find them.
        dataSet['Embarked'] = dataSet['Embarked'].fillna('X')
        dataSet['Port']     = dataSet['Embarked'].map({'C': 0, 'Q': 1, 'S': 2, 'X':-1})

        dataSet['Title']    = dataSet['Name'].map(lambda n: passengerTitle(n))
        dataSet['Gender']   = dataSet['Sex'].map({'female': 0, 'male': 1})
        
        dataSet['AgeGroup'] = dataSet['Age'].map(lambda x: ageGroup(x))
        dataSet['Class']    = dataSet['Pclass']

        # calculate family size and use to determine if passenger is alone
        dataSet['FamilySize'] = dataSet['Parch'] + dataSet['SibSp'] + 1
        dataSet['IsAlone']    = 0
        dataSet.loc[dataSet['FamilySize'] == 1, 'IsAlone'] = 1
        
        dataSet['NormalisedFare']  = normaliseFares(dataSet)
        

    return dataSets