MAX_CONSTANTS = 10

propositions = ['p', 'q', 'r', 's']
connectives = ['/\\', '\\/', '=>']
universals = ['A']
existentials = ['E']
variables = ['x', 'y', 'z','w']
predicates = ['P', 'Q', 'R', 'S']

class Formula:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

def isAtom(fmla):
    if len(fmla) == 6:
        if fmla[0] in predicates and fmla[1] =='(' and fmla[2] in variables and fmla[3] == ',' and fmla[4] in variables and fmla[5] == ')':
            return True
    return False

def isNeg(fmla):
    if fmla[0] == '~' :
        return True
def isProp(fmla):
    if len(fmla) == 1 and fmla in propositions:
        return True
# Parse a formula, consult paseOutput for return values.

def parse(fmla):
    num_brackets =0
    num_connectives = 0
    num_propositions = 0
    num_variables = 0
    stack = []
    if isProp(fmla):
        return ('a proposition')
    
    for i in range(len(fmla)): 
        if fmla[i] == '(':
            stack.append(i)
            num_brackets+=1
            if not BracketChecker(i, fmla):
                return('not a formula')
        elif fmla[i] == ')':
            if stack:
                stack.pop()
                num_brackets+=1
            else:
                return('not a formula')
        elif fmla[i] in connectives: 
            if connectiveSyntaxChecker(fmla, i):
                num_connectives +=1
            else:
                return('not a formula')
        elif fmla[i] in propositions:
            if propositionSyntaxChecker(fmla, i):
                num_propositions +=1
            else:
                return('not a formula')

    #after loop finishes                    
    if len(stack) != 0 and ConnectivesBracketsPropsNumberchecker(num_connectives, num_brackets, num_propositions) and lhs is not None and con is not None and rhs is not None: 
   
        if isFo(fmla) and isNeg(fmla) and not isUniversal(fmla) and not isExistential(fmla):
            return ('a negation of a first order logic formula') 
        if isUniversal(fmla):
            return ('a universally quantified formula')
        if isExistential(fmla) :
            return ('an existentially quantified formula')
        if isFo(fmla) and not isNeg(fmla) and not isUniversal(fmla) and not isExistential(fmla):
            return ('a binary connective first order formula')
        else: 
            if isNeg(fmla): 
                return ('a negation of a propositional formula')
            else: 
                return ('a binary connective propositional formula')
   
    return ('not a formula')
    
def BracketChecker(i, fmla):
    if fmla[i+1] == ')': 
        return False
    return True

def propositionSyntaxChecker(fmla, i):
    if i !=0: 
        if fmla[i-1] == '(' or fmla[i-1] in connectives or fmla[i-1] == '~' :
            return True 
        return False
    return True

def connectiveSyntaxChecker(fmla, i): 
    if i != 0 and i != len(fmla)-1:
        if fmla[i-1] in propositions and fmla[i+1] in propositions:
            return True
    return False
  

def ConnectivesBracketsPropsNumberchecker(num_connectives, num_brackets, num_propositions):
    if (num_brackets !=2*num_connectives and num_connectives != 0) and (num_propositions != 2*num_connectives and num_connectives != 0) and (num_brackets != 0):
        return False
    return True

def isUniversal(fmla):
    if fmla[0] == 'A':
        return True
    elif fmla[0] == '~' and fmla[1] == 'E':
        return False
def isExistential(fmla):
    if fmla[0] == 'E':
        return True
    elif fmla[0] == '~' and fmla[1] == 'A':
        return False
def isFo(fmla):
    for pred in predicates:
        if pred in fmla:
            return True
    for var in variables:
        if var in fmla:
            return True

def lhs_Con_Rhs(fmla):
    stack = []
    lhs, con, rhs = None, None, None  
    if (isNeg(fmla)):
        fmla = convertNegativeBinary(fmla)
    for i in range(len(fmla)): 
        if fmla[i] == '(':
            stack.append(i)
        if fmla[i] == ')':
            if stack:
                stack.pop()
            else:
                print ("not a wiff 1")
                return None, None, None  # NOT A WFF
        if len(stack) == 1: 
            if i < len(fmla) - 1 and (fmla[i] + fmla[i+1] == '/\\' or fmla[i] + fmla[i+1] == '\\/' or fmla[i] + fmla[i+1] == '=>'):
                lhs, con, rhs = fmla[1:i], fmla[i:i+2], fmla[i+2:(len(fmla)-1)]

    if len(stack) != 0: 
        print ("not a wiff 3")
        return None, None, None  # NOT A WFF

    if lhs is not None and con is not None and rhs is not None:
        print(f'LHS : {lhs} Con : {con} Rhs : {rhs}')
        return lhs, con, rhs
    else: print ("print nah")
    
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

def convertNegativeBinary(formula):
    """
    Converts a negated binary connective formula into its equivalent by applying negation to each operand 
    and flipping the connective according to De Morgan's Laws.
    """
    # Remove the outer negation and parentheses
    inner_formula = formula[2:-1]

    if "/\\" in inner_formula:  
        connective = "/\\"
        replacement = "\\/"  
    elif "\\/" in inner_formula:  
        connective = "\\/"
        replacement = "/\\"  
    elif "=>" in inner_formula:
        connective = "=>"
        replacement = "/\\"

    # Split the formula into its operands based on the binary connective
    operands = inner_formula.split(connective)
    left_operand = operands[0].strip()
    right_operand = operands[1].strip()

    if connective != "=>": 
        negated_left = f"~{left_operand}"
        negated_right = f"~{right_operand}"
    else: 
        negated_left = left_operand
        negated_right = f"~{right_operand}"   

    return f"({negated_left} {replacement} {negated_right})"

lhs_Con_Rhs(r"(~p => ~q)")

# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    return None

#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    return 0
   
#------------------------------------------------------------------------------------------------------------------------------:
#                   DO NOT MODIFY THE CODE BELOW. MODIFICATION OF THE CODE BELOW WILL RESULT IN A MARK OF 0!                   :
#------------------------------------------------------------------------------------------------------------------------------:

# f = open('input.txt')

# parseOutputs = ['not a formula',
#                 'an atom',
#                 'a negation of a first order logic formula',
#                 'a universally quantified formula',
#                 'an existentially quantified formula',
#                 'a binary connective first order formula',
#                 'a proposition',
#                 'a negation of a propositional formula',
#                 'a binary connective propositional formula']

# satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



# firstline = f.readline()

# PARSE = False
# if 'PARSE' in firstline:
#     PARSE = True

# SAT = False
# if 'SAT' in firstline:
#     SAT = True

# for line in f:
#     if line[-1] == '\n':
#         line = line[:-1]
#     parsed = parse(line)

#     if PARSE:
#         output = "%s is %s." % (line, parseOutputs[parsed])
#         if parsed in [5,8]:
#             output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
#         print(output)

#     if SAT:
#         if parsed:
#             tableau = [theory(line)]
#             print('%s %s.' % (line, satOutput[sat(tableau)]))
#         else:
#             print('%s is not a formula.' % line)
