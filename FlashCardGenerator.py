import json, random, os, sys

class container():
    """Container class used when creating auto-sorted catagories and sub-catagories"""
    pass


def dumbdumbprotection(func):
    """Completely Pointless Error Handling"""
    def inner(*args):
        try:
            return func(*args)
        except Exception as e:
            print(f'We have a bit of a predicament here\nSend a pic of this to Jack: \n{e}\n')
            exit()
        return func(*args)
    return inner


@dumbdumbprotection
def yena(say, options):
    """Loop until a valid input is given"""
    correctornot = None
    while correctornot not in options:
        correctornot = input(say).lower()
    return correctornot


@dumbdumbprotection
def stuff(dictt):
    """Return keys of dict"""
    return [x for x in dictt]


@dumbdumbprotection
def hasdict(thing):
    """Check if the current dict has another dict in it (if so it means this is a dict of more catagories rather than questions)"""
    lst = []
    for x in list(thing.values()):
        if isinstance(x, dict):
            lst.append(x)
    return lst


@dumbdumbprotection
def creation(dictt):
    """The extremely epic part that makes all of this flexible, automatically sorts the json into catagories and sub-catagories"""
    thing = container()
    current = stuff(dictt)
    for x,y in enumerate(current):
        if hasdict(dictt[y]) != []:
            result = creation(dictt[y])
            setattr(thing, str(x), [y, result])
        else:
            setattr(thing, str(x), [y, dictt[y]])
    return thing


@dumbdumbprotection
def isallcat(q):
    """If they choose all"""
    thing = yena(f'Would you like to choose how many questions are given? If no is chosen you will be dealt {len(q)} questions: ', ['y','n'])
    if thing == 'y':
        amount = int(input(f'Enter an amount less than or equal to {len(q)}: '))
        q = {x:y for x,y in random.sample(q.items(), amount)}
    os.system('clear')
    return q


@dumbdumbprotection
def createall(stuff):
    """Create an all category (not yet done will make better at some point)"""
    al = {}
    options = [getattr(stuff,x) for x in dir(stuff) if '__' not in x]
    for x in options:
        if isinstance(x[1], dict):
            al.update(x[1])
            continue
        for y in [b for b in dir(x[1]) if b.isdigit()]:
            if getattr(x[1], y[0])[0] == 'All':
                al.update(getattr(x[1], y[0])[1])

    return al


@dumbdumbprotection
def dothething(path):
    """Get user to pick which topic they would like to pull questions from"""
    with open(path, 'r') as f:
        data = json.load(f)
    stuff = creation(data)
    al = createall(stuff)
    
    newstuff = container()
    for x in [x for x in dir(stuff) if '__' not in x]:
        setattr(newstuff, f'{int(x) + 1}', getattr(stuff, x))
    setattr(newstuff, '0', ['All', al])

    while True:
        options = [x for x in dir(newstuff) if '__' not in x] # Create list of attributes to choose from
        options.sort(key=lambda x: int(x)) # Because i have no idea why but sometimes the order got messed up
        print('\n'.join([f'{y}: {getattr(newstuff, x)[0]}' for y,x in enumerate(options)])) # Print out name of options next to corresponding number
        
        hmm = yena('Choose: ', options)
        newstuff = getattr(newstuff, hmm)[1]
        if isinstance(newstuff, dict):
            os.system('clear')
            if hmm == '0':
                return isallcat(newstuff)
            return newstuff
        os.system('clear')


@dumbdumbprotection
def torandomise(d):
    """Shuffle order questions will appear in"""
    keys = list(d)
    random.shuffle(keys)
    hmmm = {x: d[x] for x in keys}
    return hmmm


@dumbdumbprotection
def previouspath():
    """Take an already existing path from the json"""
    with open(f'{os.path.dirname(sys.argv[0])}/previousjsons.json', 'r') as f:
        data = json.load(f)
    dct = {y:x for y,x in enumerate(data)}
    for y,x in dct.items():
        print(f'{y}: {x}')
    choice = yena('Choose: ',[str(x) for x in dct])
    return data[dct[int(choice)]]


@dumbdumbprotection
def newpath(name, path):
    """Store a new path in json for user recollection"""
    with open(f'{os.path.dirname(sys.argv[0])}/previousjsons.json', 'r+') as f:
        data = json.load(f)
        data[name] = path
        f.seek(0)
        json.dump(data, f, indent=4)


@dumbdumbprotection
def getQuestions():
    """Get file, user inputs which topic they will practise, return dict of shuffled questions"""
    if yena('Would you like to use a previous path or a new one?\n1: New\n2: Old\nChoose: ', ['1', '2']) == '2':
        os.system('clear')
        path = previouspath()
    else:
        os.system('clear')
        path = input('Enter a path: ')
        name = input('Enter a filename: ')
        newpath(name, path)
    os.system('clear')
    questions = dothething(path)
    randomised_questions = torandomise(questions)
    return randomised_questions


@dumbdumbprotection
def questionDisplay(q, a):
    """Display question await input and answer"""
    print(f'Question: \n{q}\nYour Answer:')
    input()
    print(f'\nAnswer: \n{a}')


@dumbdumbprotection
def again(wrong, c, i):
    """See if they would like to practise ones they got wrong"""
    print(f'You scored {c}/{c+i}')
    if len(wrong) == 0:
        return
    print("-----------What you got wrong-----------\n")
    for key, value in wrong.items():
        print(f'Question:\n{key}\nAnswer:\n{value}\n')
    return yena('Would you like to practise what you got wrong?: ', ['y','n'])


@dumbdumbprotection
def improveing(questions):
    """To display questions previously wrong"""
    q = {}
    c = 0
    i = 0
    questions = torandomise(questions)
    for x in questions:
        os.system('clear')
        questionDisplay(x, questions[x])
        if yena('Correct or Incorrect y/n: ', ['y', 'n']) == 'n':
            i+=1
            q[x] = questions[x]
        else:
            c+=1

    os.system('clear')
    if again(q, c, i) == 'y':
        improveing(q)



@dumbdumbprotection
def main():
    """Main function"""
    correct = 0
    incorrect = 0
    toImprove = {}

    questions = getQuestions()
    for x in questions:
        questionDisplay(x, questions[x])
        if yena('Correct or Incorrect y/n: ', ['y', 'n']) == 'n':
            toImprove[x] = questions[x]
            incorrect+=1
        else:
            correct+=1
        os.system('clear')
    
    if again(toImprove, correct, incorrect) == 'y':
        improveing(toImprove)


# Create file to store json paths if the file does not already exist
if not os.path.exists(f'{os.path.dirname(sys.argv[0])}/previousjsons.json'):
    with open(f'{os.path.dirname(sys.argv[0])}/previousjsons.json', 'w+') as f:
        data = {}
        json.dump(data, f, indent=4)


# Main Loop
main()
while True:
    if yena('Would you like to continue?: ', ['y','n']) == 'y':
        os.system('clear')
        main()
    else:
        break