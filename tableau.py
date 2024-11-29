MAX_CONSTANTS = 10

propositions = ['p','q','r','s']
connectives = ['/\\', '\\/', '=>']
universals = ['A']
existentials = ['E']
variables = ['x', 'y', 'z','w']
predicates = ['P', 'Q', 'R', 'S']
constants  = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

def isAtom(fmla):
    if len(fmla) == 6:
        if fmla[0] in predicates and fmla[1] =='(' and fmla[2] in (variables+constants) and fmla[3] == ',' and fmla[4] in (variables+constants) and fmla[5] == ')':
            return True
def isAtom1(fmla): 
    if len(fmla) == 6:
        if fmla[0] in predicates and fmla[1] =='(' and fmla[2] in constants and fmla[3] == ',' and fmla[4] in constants and fmla[5] == ')':
            return True
    return False
def isNegAtom(fmla):
    if len(fmla) == 7:
        if fmla[0] == '~' and isAtom(fmla[1:7]):
            return True
    return False
def isNegAtom1(fmla):
    if len(fmla) == 7:
        if fmla[0] == '~' and isAtom1(fmla[1:7]):
            return True
    return False

def isNeg(fmla):
    fmla = fmla.replace('~~','')
    if fmla[0] == '~' :
        return True
    return False
    
def isProp(fmla):
    fmla = fmla.replace('~~','')
    if len(fmla) == 1 and fmla in propositions:
        return True
    return False
    
def isNegProp(fmla):
    fmla = fmla.replace('~~','')
    if fmla[0] == '~' and fmla[1] in propositions:
        return True
    return False
    
def isUniversal(fmla):
    if fmla[0] == 'A':
        return True
    elif fmla[0] == '~' and fmla[1] == 'E':
        return True
    return False

def isExistential(fmla):
    if fmla[0] == 'E':
        return True
    elif fmla[0] == '~' and fmla[1] == 'A':
        return True
    return False

def isFo(fmla):
    return any(pred in fmla for pred in predicates) or any(var in fmla for var in variables)

# Parse a formula, consult paseOutput for return values.
def parse(fmla):
    num_brackets =0
    num_connectives = 0
    num_propositions = 0
    num_variables = 0
    num_predicates = 0
    stack = []
    fmla = fmla.replace('~~','')
    if isProp(fmla):
        return (6)
    if(isAtom(fmla)): 
        return (1)
    for i in range(len(fmla)): 
        if fmla[i] == '(':
            stack.append(i)
            num_brackets+=1
            if fmla[i]+fmla[i+1] == '()':
                return(0)
        if fmla[i] == ')':
            if stack:
                stack.pop()
                num_brackets+=1
            else:
                return(0)
        if i+2<len(fmla) and fmla[i]+fmla[i+1] in connectives:
            if ( fmla[i+2] in ['(','~'] or fmla[i+2] in propositions or fmla[i+2] in predicates or fmla[i+2] in universals or fmla[i+2] in existentials):
                num_connectives +=1
            else: 
                return(0)     
        if fmla[i] in propositions:
            if propositionSyntaxChecker(fmla, i):
                num_propositions +=1
            else:
                return(0)
        if fmla[i] in predicates: 
            if (i+5<len(fmla)): 
                if isAtom(fmla[i:i+6]):
                    num_predicates +=1
                else: 
                    return(0)
            else: 
                return(0)
        if fmla[i] in existentials or fmla[i] in universals: 
            if (i+1<len(fmla)):
                if fmla[i] == 'A' and fmla[i+1] in (variables+constants):
                    num_variables +=1
                elif fmla[i] == 'E' and fmla[i+1] in (variables+constants):
                    num_variables +=1
                else:
                    return(0)
            else: 
                return(0)
        if fmla[i] in variables: 
            if(i != 0): 
                if fmla[i-1] == ',' or fmla[i-1] == '(' or fmla[i-1] == 'A' or fmla[i-1] == 'E':
                    num_variables +=1
                else: 
                    return(0)
            else:
                return(0)
        if fmla[i] =='~' and i!=0: 
                if (i>1 and fmla[i-2]+fmla[i-1] not in connectives)and fmla[i-1] != '(' and fmla[i-1] not in variables and fmla[i-1] not in constants:
                    return(0)                      
    if (len(stack)==0):
        if isFo(fmla) and isNeg(fmla) :
            return (2) 
        if isUniversal(fmla):
            return (3)
        if isExistential(fmla) :
            return (4)
        if isFo(fmla) and not isNeg(fmla) and not isUniversal(fmla) and not isExistential(fmla):
            return (5)
        else: 
            if isNeg(fmla): 
                return (7)
            else: 
                return (8)
    return (0)

def propositionSyntaxChecker(fmla, i):
    if (i==0): 
        return True
    elif (i<=2) and i< len(fmla)-1:
        if fmla[i-1] == '(' or fmla[i-1] == '~':
            return True
    elif fmla[i-1] == '(' or fmla[i-2]+fmla[i-1] in connectives or fmla[i-1] == '~' :
        return True 
    return False

def lhs_Con_Rhs(fmla):
    stack = []
    lhs, con, rhs = None, None, None  
    for i in range(len(fmla)): 
        if fmla[i] == '(':
            stack.append(i)
        if fmla[i] == ')':
            if stack:
                stack.pop()
            else:
                return None, None, None  # NOT A WFF
        if len(stack) == 1: 
            if i < len(fmla) - 1 and (fmla[i] + fmla[i+1] == '/\\' or fmla[i] + fmla[i+1] == '\\/' or fmla[i] + fmla[i+1] == '=>'):
                lhs, con, rhs = fmla[1:i], fmla[i:i+2], fmla[i+2:(len(fmla)-1)]
    if lhs is not None and con is not None and rhs is not None:
        return lhs.strip(), con.strip(), rhs.strip()

# Return the LHS of a binary connective formula
def lhs(fmla):
    lhs, _, _ = lhs_Con_Rhs(fmla)
    return lhs

# Return the connective symbol of a binary connective formula
def con(fmla):
    _, con, _ = lhs_Con_Rhs(fmla)
    return con

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    _, _, rhs = lhs_Con_Rhs(fmla)
    return rhs

def conConverter(fmla): 
    conHere = con(fmla)
    left = lhs(fmla)
    right = rhs(fmla)
    if (conHere == '=>'): 
        conHere = '\\/'
        left = '~' + lhs(fmla)
    formula =f"({left.strip()} {conHere.strip()} {right.strip()})"
    formula = formula.replace('~~','')
    return formula

def RecursiveNegation(formula): 
    if formula[0] != '~':
        return formula
    formula = formula[1:]
    parsedResult = parse(formula)

    if parsedResult in [7, 2]: 
        return RecursiveNegation(formula[1:])
    
    if parsedResult in [5, 8]:
        left, opp, right = lhs(formula), con(formula), rhs(formula)
        if opp == '=>':
            returner = f'({RecursiveNegation(left)}{'/\\'}{RecursiveNegation('~'+right)})'
        if opp== '/\\':
            returner = f'({RecursiveNegation('~'+left)}{'\\/'}{RecursiveNegation('~'+right)})'
        if opp == '\\/':   
            returner = f'({RecursiveNegation('~'+left)}{'/\\'}{RecursiveNegation('~'+right)})'
        return returner.replace('~~','')
    if parsedResult in [1, 6]:
        return '~'+formula
    if parsedResult in [3]:
        return 'E' + formula[1] + RecursiveNegation('~'+formula[2:])
    if parsedResult in [4]:
        return 'A' + formula[1] + RecursiveNegation('~'+formula[2:])


def theory(fmla):#initialise a theory with a single formula in it
    return fmla

def sat(tableau):
    tableauBranches = []
    tableauBranches.append(tableau)
    AllGammaFormulasAcrossBranches =[]
    constants_new = []
    current_constant= 0
    while len(tableauBranches)!=0:
        branch = tableauBranches.pop()
        if ExpPredicate(branch) and not is_closedPredicates(branch) or (ExpFirstOrder(branch) and not is_closedFirstOrder(branch)): 
            return 1
        else: 
            for i in range (len(branch)):
                branch[i] = branch[i].replace('~~','')
                parsingResult = parse(branch[i])
                if parsingResult == 8 or parsingResult == 7 or parsingResult == 6:
                    if isProp(branch[i]) or isNegProp(branch[i]):
                        if ExpPredicate(branch) and not is_closedPredicates(branch): 
                            return 1
                        continue
                    if isNeg(branch[i]):
                        branch[i] = RecursiveNegation(branch[i]).replace('~~','')
                    if isalpha(branch[i]):
                        original = branch[i]
                        branch[i] = lhs(original).replace('~~','')
                        branch.append(rhs(original).replace('~~',''))
                        tableauBranches.append(branch)
                        break
                    if isBeta(branch[i]):
                        # ##print("reached beta")
                        if(con(branch[i]) == '=>'):
                            branch[i] = conConverter(branch[i])
                        original = branch[i]
                        newBranch = branch.copy()
                        branch[i] = lhs(branch[i]).replace('~~','')
                        newBranch[i] = rhs(original).replace('~~','')
                        tableauBranches.append(branch)
                        tableauBranches.append(newBranch)
                        break
                else: 
                    if isAtom(branch[i]) or isNegAtom(branch[i]) or isAtom1(branch[i]) or isNegAtom1(branch[i]):
                        continue
                    if isNeg(branch[i]):
                        branch[i] = RecursiveNegation(branch[i])

                    if isDelta(branch[i]):
                        #print('Delta')
                        if current_constant+1 > MAX_CONSTANTS:
                            return 2
                        newfmla = DeltaExpansion(branch[i], current_constant)
                        constants_new.append(constants[current_constant])
                        current_constant+=1
                        branch[i] = newfmla
                        tableauBranches.append(branch)
                        #print(tableauBranches)
                        break

                    if isGamma(branch[i]):
                        if AllGammaFormulasAcrossBranches !=[]: 
                            GammaFormulasSeen = AllGammaFormulasAcrossBranches.pop()
                        else: 
                            GammaFormulasSeen = []
                        copyCheck = []
                        #print("Gamma")
                        for fmla_1 in branch:
                            if not isGamma(fmla_1): 
                                copyCheck.append(fmla_1)
                        if(ExpFirstOrder(copyCheck) and is_closedFirstOrder(copyCheck)):
                            continue
                        if len(copyCheck) != 0 and not ExpFirstOrder(copyCheck):
                            branch = [x for x in branch if x != branch[i]]+[branch[i]] #other formulas exist in the samd branch that we should expans first
                        elif current_constant ==0: 
                            constants_new.append(constants[current_constant])
                            branch = GammaExpansion(branch, branch[i], constants_new) # no Constants used by Gamma yet, and this is the only thing to expand
                            current_constant+=1
                            constants_new = []
                        else: #start Gamma Expansion
                                if  branch[i] in GammaFormulasSeen and constants_new == [] and (ExpFirstOrder(copyCheck) and not is_closedFirstOrder(copyCheck)) and (len(copyCheck)+len(GammaFormulasSeen) == len(branch)):
                                    ##print("here")
                                    return 1
                                else: 
                                    if(len(copyCheck)+len(GammaFormulasSeen) != len(branch)) and constants_new == [] and branch[i] not in GammaFormulasSeen: # there is another Gamma Formula in the branch that we need to expand
                                        for i in range (current_constant): 
                                            constants_new.append(constants[i])
                                    elif((len(copyCheck)+len(GammaFormulasSeen) != len(branch)) and branch[i] in GammaFormulasSeen): 
                                         branch = [x for x in branch if x != branch[i]]+[branch[i]] 
                                         continue
        
                                    branch = GammaExpansion(branch, branch[i], constants_new)
                                    constants_new = []
                                    if branch[i] not in GammaFormulasSeen: GammaFormulasSeen.append(branch[i]) 
                                    
                        AllGammaFormulasAcrossBranches.append(GammaFormulasSeen)
                        tableauBranches.append(branch)
                        #print(tableauBranches)
                        #print("GammaFormulasSeen", AllGammaFormulasAcrossBranches)
                        break

                    if isalpha(branch[i]):
                        ##print("Reached Alpha")
                        original = branch[i]
                        branch[i] = lhs(original).replace('~~','')
                        branch.append(rhs(original).replace('~~',''))
                        tableauBranches.append(branch)
                        #print("tab", tableauBranches)
                        break

                    if isBeta(branch[i]):
                        if AllGammaFormulasAcrossBranches !=[]: 
                            GammaFormulasSeen = AllGammaFormulasAcrossBranches.pop()
                        else: 
                            GammaFormulasSeen = []
                        #print("Reached Beta")
                        original = branch[i]
                        newBranch = branch.copy()
                        if(con(branch[i]) == '=>'):
                            branch[i] = conConverter(branch[i])
                        branch[i] = lhs(branch[i]).replace('~~','')
                        newBranch[i] = rhs(original).replace('~~','')
                        tableauBranches.append(branch)
                        tableauBranches.append(newBranch)
                        #print("tab", tableauBranches)
                        AllGammaFormulasAcrossBranches.append(GammaFormulasSeen)
                        AllGammaFormulasAcrossBranches.append(GammaFormulasSeen)
                        #print("GammaFormulasSee Here", AllGammaFormulasAcrossBranches)
                        break                        
    return 0
                        
def ExpPredicate(branch):
    Allprops = True
    for prossibleProp in branch:
        if not isProp(prossibleProp) and not isNegProp(prossibleProp): 
            Allprops = False
    return Allprops

def ExpFirstOrder(branch):
    allAtoms = True
    for possibleAtom in branch:
        if not isAtom(possibleAtom) and not isNegAtom(possibleAtom):
            allAtoms = False
    return allAtoms

def is_closedPredicates(branch):
    seen = set()
    for predicate in branch:
        if (isProp(predicate) or isNegProp(predicate)):
            if predicate.startswith("~"):  # Current predicate is a negation
                original = predicate[1:]  # Remove the negation symbol
                if original in seen:
                    return True
            else:  
                negated = f"~{predicate}"  
                if negated in seen:
                    return True
    
            seen.add(predicate)
    return False

def is_closedFirstOrder(branch):
    seen = set()
    for predicate in branch:
        if (isAtom1(predicate) or isNegAtom1(predicate)):
            if predicate.startswith("~"):  # Current predicate is a negation
                original = predicate[1:]  # Remove the negation symbol
                if original in seen:
                    return True
            else:  
                negated = f"~{predicate}"  
                if negated in seen:
                    return True
            seen.add(predicate)
    return False

def DeltaExpansion(fmla, current_constant):
    newfmla = fmla[2:]
    variable = fmla[1]
    if isinstance(current_constant, int):
        newfmla = newfmla.replace(variable, constants[current_constant])
    else: 
        newfmla = newfmla.replace(variable, current_constant)
    return newfmla

def GammaExpansion(branch,formula, constantsNew): 
    for constant in constantsNew:
            GammaExpandedFormula = DeltaExpansion(formula, constant)
            branch.append(GammaExpandedFormula)
    return branch

def isalpha(fmla): 
    if (con(fmla) == '=>'):
        fmla = conConverter(fmla)
    if (con(fmla) == '/\\'): 
        return True
    return False

def isBeta(fmla): 
     if con(fmla) == '=>':
        fmla  = conConverter(fmla) 
     if (con(fmla) == '\\/'):        
        return True
def isDelta(fmla): 
    if fmla[0] == 'E':
        return True
def isGamma(fmla): 
    if fmla[0] == 'A':
        return True 
#------------------------------------------------------------------------------------------------------------------------------:
#                   DO NOT MODIFY THE CODE BELOW. MODIFICATION OF THE CODE BELOW WILL RESULT IN A MARK OF 0!                   :
#------------------------------------------------------------------------------------------------------------------------------:

f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
