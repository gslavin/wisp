import sys
#http://docs.python.org/3.3/library/math.html
import math
import copy
import sys
#input = "(* (+ 2 3) (+ 3 3))"

class ParseError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Node():
    def __init__(self, op = None, argList = None):
        self.op = op
        self.argList = argList

#Binary Functions
def add(a,b):
    return a + b

def subtract(a,b):
    return a - b

def multiply(a,b):
    return a * b
    
def divide(a,b):
    return a / b

def power(a,b):
    return a**b

def mod(a,b):
    return a % b

def floor(a):
    return math.floor(a)

def ceil(a):
    return math.ceil(a)
 

    
def factorial(a):
    try:
        a = int(a)
        if a < 0:
            raise ValueError()
    except ValueError:
        err_string = "argument to factorial must be a positive integer"
        raise ParseError(err_string)
    product = 1
    while a > 0:
        product = product * a
        a -= 1
    return product
 
#uneeded function? 
def if_statement(conditional, true_value, false_value):
    if conditional:
        return true_value
    else:
        return false_value

def cond_greater_than(a, b):
    return a > b

def cond_less_than(a, b):
    return a < b
    
def cond_equal_to(a,b):
    return a == b
    
def cond_not(a):
    return not a

    
numeric_ops = ['+','-','*','/','**','mod','fact','floor','ceil','gt','lt','eq','not']

conditional_ops = ['gt', 'lt', 'eq', 'not']


#TODO: define functions for 'or','and','nor','nand'
op_dict = {'+': add, '-': subtract,'*': multiply, '/': divide, '**': power, 'mod': mod, \
           'fact': factorial, 'if':if_statement, 'gt': cond_greater_than, 'lt': cond_less_than, \
           'eq': cond_equal_to, 'not': cond_not, 'floor': floor, 'ceil': ceil}
arg_num_dict = {'1': ['fact','floor','ceil','not'], \
                '2': ['+','-','*','/','**','mod','gt','lt','eq','or','and','nor','nand'], \
                '3': ['if']
               }

def get_arg_num(op):
    for k in arg_num_dict.keys():
        if op in arg_num_dict[k]:
            return int(k)
    err_string = "ERROR op '%s' not in arg_num_dict" % (op,) 
    raise ParseError(err_string)
    #exit()
#top level parser
#creates user defines [and functions]
def top_level_parse(input):
   #get defines and then body as final expression
   tree = parse(input)
   print("Top leve parse tree")
   print_tree(tree,0)
   macro_dict = {}
   func_dict = {}
   for node in tree.argList[:-1]:
       if node.op == "define":
            collect_macro(macro_dict, node)
       elif node.op == "func":
            collect_func(func_dict, node)
       else:
            err_string = "Only defines and funcs can precede the body of the program"
            raise ParseError(err_string)
   return macro_dict, func_dict, tree.argList[-1]

def collect_macro(macro_dict,node):
    if len(node.argList) != 2:
        err_string = "Invalid define.  define must be of the form (define name value)"
        raise ParseError(err_string)
    if node.argList[0].isalpha() != True:
        err_string = "invalid define name: %s. Define name must be an alphabetic character" \
            % (node.argList[0])
        raise ParseError(err_string)
    macro_dict[node.argList[0]] = node.argList[1]

def collect_func(func_dict, node):
    if len(node.argList) < 3:
        err_string = "func must be of the form (define name args body)"
        raise ParseError(err_string)
    func_dict[node.argList[0]] = node.argList[1:]
    
#main tokenization and parsing function
def parse(input):
    print("PARSE INPUT")
    print(input)
    i = 0
    token = ""
    tokenFirst = True
    expr = Node(None,[])
    while ( i <= len(input)):
        # If whitespace or end of file set token and continue
        if i == len(input) or input[i] == ' ':
            if token != '' and token != ' ':
                if tokenFirst:
                    tokenFirst = False
                    expr.op = token
                else:
                    expr.argList.append(token)
            token = ""
            i += 1
        # If '(' parse sub expression and start new node
        elif input[i] == '(':
            substring,i = get_expression(input,i)
            new_expr = parse(substring)
            # place the subexpression as the curren token
            # This current requires there to be a space between
            # a sub expression and the next argument
            token = new_expr
        else:
            #add char to token
            token += input[i]
            i += 1
    return expr
    
def get_expression(input,i):
    i += 1 
    substring = ""
    startParen = 1
    endParen = 0
    while startParen != endParen:
        if input[i] == '(':
            startParen += 1
        elif input[i] == ')':
            endParen += 1
            if startParen == endParen:
                i += 1
                break
        else:
            pass
        substring += input[i]
        i += 1
    return substring,i

def substitute_macros(macro_dict,tree):
    for i in range(len(tree.argList)):
        if isinstance(tree.argList[i],Node):
            substitute_macros(macro_dict, tree.argList[i])
        else:
            if tree.argList[i] in macro_dict.keys():
                tree.argList[i] = macro_dict[tree.argList[i]]
    
def print_tree(tree,indent = 0):
    space = ""
    for i in range(indent):
        space += ' '
    print(space,"op",tree.op)
    for a in tree.argList:
        if isinstance(a,Node):
            print_tree(a,indent + 4)
        else:
            print(space,"arg:", a)

def eval_tree(tree, func_dict):
   
    #numeric ops
    if tree.op in numeric_ops:
        #check that number of arguments is 2
        if len(tree.argList) == get_arg_num(tree.op):
            #evaluation args that are not primitives
            for i in range(len(tree.argList)):
                if isinstance(tree.argList[i], Node):
                    tree.argList[i] = eval_tree(tree.argList[i], func_dict)
            #check that all args are numeric
            args = []
            for a in tree.argList:
                try:
                    args.append(float(a))
                except ValueError:
                    err_string = "ERROR:invalid arg %s for operator %s" % (a,tree.op)
                    raise ParseError(err_string)
            func = op_dict[tree.op]
            #give elements of list of args
            ans = func(*args)
            return(int(ans) if ans == int(ans) else ans)
        else:
            err_string = "ERROR: wrong number of arguments for %s operator" % (tree.op,)
            raise ParseError(err_string)
    #if statement
    elif tree.op == 'if':
        if (len(tree.argList) == get_arg_num(tree.op)):
            if isinstance(tree.argList[0], Node):
                    tree.argList[0] = eval_tree(tree.argList[0], func_dict)
                    
            if tree.argList[0] == 1:
                i = 1
            elif tree.argList[0] == 0:
                i = 2
            else:
                err_string = "ERROR:arg %s (condition arg) must eval to 0 or 1 for %s" % (tree.argList[0],tree.op)
                raise ParseError(err_string)
            #eval only the correct body of the if statement
            if isinstance(tree.argList[i], Node):
                    tree.argList[i] = eval_tree(tree.argList[i], func_dict)
            try:
                ans = float(tree.argList[i])
            except ValueError:
                err_string = "ERROR:invalid arg %s for operator %s" % (a,tree.op)
                raise ParseError(err_string)
            #give elements of list of args
            return(int(ans) if ans == int(ans) else ans)
        else:
            err_string = "ERROR: wrong number of arguments for %s operator" % (tree.op,)
            raise ParseError(err_string)
    #or statement
    #check that a 1 is not present
    #then eval nodes in order
    elif tree.op == 'or':
        #check that number of arguments is 2
        if len(tree.argList) == get_arg_num(tree.op):
            if "1" in tree.argList:
                return 1
            #evaluation args that are not primitives
            #check if 1 is result of evaluation
            for i in range(len(tree.argList)):
                if isinstance(tree.argList[i], Node):
                    tree.argList[i] = eval_tree(tree.argList[i], func_dict)
                if tree.argList[i] == "1":
                    return 1
            #check that all args are numeric
            args = []
            for a in tree.argList:
                try:
                    args.append(float(a))
                except ValueError:
                    err_string = "ERROR:invalid arg %s for operator %s" % (a,tree.op)
                    raise ParseError(err_string)
            return 0
        else:
            err_string = "ERROR: wrong number of arguments for %s operator" % (tree.op,)
            raise ParseError(err_string)

    #user defined functions
    elif tree.op in func_dict.keys():
        #argument substitution 
        func_args = func_dict[tree.op][:-1]
        func_body = copy.deepcopy(func_dict[tree.op][-1])
        body = func_sub_args(func_args, func_body, tree.argList)
        #evaluation args that are not primitives
        for i in range(len(tree.argList)):
            if isinstance(tree.argList[i], Node):
                tree.argList[i] = eval_tree(tree.argList[i], func_dict)
        return eval_tree(body, func_dict)
    else:
        err_string = "ERROR: unknown function '%s'" % (tree.op,)
        raise ParseError(err_string)
                
def func_sub_args(func_args, func_body, args):
    if len(func_args) != len(args):
        err_string = "Incorrect number of arguments given to user function"
        raise ParseError(err_string)
    arg_map = {}
    for i in range(len(func_args)):
        arg_map[func_args[i]] = args[i]
    substitute_macros(arg_map, func_body)
    return func_body

def match_parens(input):
    line_num = 0
    open_paren = 0
    close_paren = 0
    for i in range(len(input)):
        if input[i] == '(':
            open_paren += 1
        elif input[i] == ')':
            close_paren += 1
        elif input[i] == '\n':
            line_num += 1
        else:
            continue
        if close_paren > open_paren:
            raise ParseError("mismatched parenthesis at line %d" % (line_num,))
    if open_paren != close_paren:
            raise ParseError("mismatched parenthesis")
            
def remove_comments(input):
    i = 0
    j = 0
    i = input.find(';', j)
    j = input.find('\n',i)
    while i != -1 and j != -1:
        input = input[:i] + input[j+1:]
        i = input.find(';', j)
        j = input.find('\n',i)
    #comment on last line of file might not have a newline
    if i != -1:
        input = input[:i]
    
    return input

def remove_newlines(input):
    input = input.replace("\r",' ')
    input = input.replace("\n",' ')
    return input
    
#run program
def main(input):
    
    input = "start " + input
    try:
        match_parens(input)
        input = remove_comments(input)
        input = remove_newlines(input)
        macro_dict, func_dict,tree = top_level_parse(input)
        substitute_macros(macro_dict,tree)
        print("tree to eval...")
        print_tree(tree,0)
        print("Func Dict: \n",func_dict)
        print()
        return eval_tree(tree,func_dict)
    except Exception as e:
        return "ERROR: " + e.value

if __name__ == "__main__":
    #initial syntax check
    input = " ".join(sys.argv[1:])
    print(main(input))
