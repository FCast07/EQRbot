import schemes # explanation schemes (templates)
from helpers import parse_extension # helper functions
import sys
import re
import subprocess

"""
S: semantics for reasoning
params: list of dl files that will be processed by the algorithm
@return set of pairs of acceptable arguments and attacks
"""
def computeAFaccepted(params,S):
    ACC = list()
    # semantics added to the parameters
    if S == 'preferred':
        params.append('prefex.dl')
    elif S == 'grounded':
        params.append('ground.dl')
    #the following strip sys.argv from the evalaf_expaf.py file and add the other files
    for i,para in enumerate(sys.argv):
        if i!=0:
            params.append(para)

    params.insert(0,'./dlv') # requires dlv to run from terminal
    output = subprocess.check_output(params)
    exts = list(filter(lambda a: a != b'', output.split(b"\n")))
    exts = exts[1:len(exts)]

    for i,ext in enumerate(exts):
        if ext == b'\r':
            continue
        a = ext.replace(b'\n', b'').replace(b'\r', b'')
        text = '{'+str(a)+'}'
        res = parse_extension(text)
        ACC.append((res[1],res[4]))
    return ACC

""""
filename: the name of the file including the scheme definitions
        The format for each rule is as follows: schemename; c :- P.
        c is the conclusion, and P is the set of premises.
path: location of the file
@return a dictionary of domain-specific rules
"""
def getSchemeDefs(filename,path):
    f = open(path + filename, "r")
    domain_rules = dict()

    for rule in f:
      sname,r = rule.split(';')
      domain_rules[sname] = r

    f.close()
    return domain_rules

"""
args: the set of arg scheme rules to include during reasoning
@return path of the generated file
"""
def prepareArgs(args,path):
    import os

    args_rules = ''

    f= open(path + 'scheme-args.dl','w+')

    for arg in args:
        args_rules = args_rules + arg + '\n'

    f.write(args_rules)
    f.close()
    return path+'scheme-args.dl'

"""
X: initial set of schemes to initialise arguments
S: semantics to be used to evaluate argumentation frameworks
@return set of pairs of acceptable arguments and attacks
"""
def evalaf(X,S):
    # domain knowledge regarding schemes and their critical questions
    ascq = {'eqr': set(['se', 'sf', 'sexp'])}
    rel_schemes = set() # all relevant scheme names that should be considered to initialise arguments

    # collection of the relevant schemes
    def instantiateSchemes(x):
        rel_schemes.add(x)
        if x in ascq.keys():
            for value in ascq[x]:
                instantiateSchemes(value)

    for x in X:
        instantiateSchemes(x)
    # end of collection
    all_schemes = getSchemeDefs('scheme-rules.txt', '')
    scheme_args = set()

    for s in rel_schemes:
        #conclusion (c) and premises (P) are the two elements obtained from splitting in two (on :-)
        c,P = all_schemes[s].split(' :- ')
        scheme_args.add('arg('+ c + ') :- ' + P)

    # create a new file to include relevant arg rules
    arg_rules_path = prepareArgs(scheme_args, '')
    ACC = computeAFaccepted([arg_rules_path],S)
    return ACC

"""
A: the acceptable set of arguments (acc_arg)
R: the acceptable set of attacks (acc_att)
@return text explanations for the input arguments and attacks
"""
def expaf(A,R):
    earg = set()
    eatt = set()

    objects = A.union(R)


    for o in objects:
        sname = o.split("(")[0] #extract argument schemes name
        exp = getattr(schemes, sname)(o)[1]
        if o in A:
            earg.add(exp)
        else:
            eatt.add(exp)

    return [earg,eatt]

################################ MAIN PROGRAM
# initialise the argumentation framework with eqr arguments.
exts = evalaf(['eqr'],S='preferred')

#print("******************** There are "+str(len(exts))+ " extensions. ********************\n")
explanations = set()
for i,ext in enumerate(exts):
    acc_arg = ext[0]
    acc_att = ext[1]
    exp_arg,exp_att = expaf(acc_arg,acc_att)
    #group each exp_arg in a unique set
    explanations = explanations.union(exp_arg)

#remove unnecessary characters from explanations
explanations = list(explanations)
explanations_polished = []
for e in explanations:
    explanations_polished.append(e.replace("\n", "").replace("_", " "))
explanations_polished = set(explanations_polished)

print("\n")
print("******************** Results ********************")
#print(">>>>> ARGUMENTS")
#print("Acceptable arguments are: \n",acc_arg) #optional: display all the acceptable arguments devoided of explanations
print("\n")
print("Explanations for acceptable arguments are as follows:")
print(explanations_polished)
print("\n")

#################optional lines for generating general explanations concerning acceptable attacks (notice that the chatbot does not take such explanations into account)

#print("Explanations for acceptable attacks are as follows: \n",exp_att)
#print("\n")
