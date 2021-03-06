import sys
# reserved word list
reserved = ['dim',
            'as',
            'string',
            'integer',
            'long',
            'single',
            'double',
            'print',
            'input',
            'if',
            'then',
            'end',
            'elseif',
            'else',
            'select',
            'case',
            'while',
            'wend',
            'do',
            'loop',
            'until',
            'for',
            'to',
            'next',
            'step',
            'sub',
            'shared',
            'function',
            'const',
            'not',
            'mod',
            'or',
            'and',
            'xor']
# Basic class for letter and digit detect
# #########################################
class Symbol(object):
    def letter(self, letter):
        if (ord(letter) >= 65 and ord(letter) < 91) or (ord(letter) >= 97 and ord(letter) < 123):
            return True
        else:
            return False

    def digit(self, digit):
        if ord(digit) >= 48 and ord(digit) < 58:
            return True
        else:
            return False
        
# identifier and reserved word detector
# #########################################
class Identifier(Symbol):
    
    def __init__(self):
    
        self.Idetected = ''
        self.ACCEPTK = 25
        self.ROLLBACK = 1
        self.current = [1]
        # it must start with a letter
        self.EDGES = {(1,'letter'):[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
                        (2,'letter'):[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
                        (3,'digit'):[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
                        (4,'_'):[2,3],
                        (5,'$'):[self.ACCEPTK],
                        (6,'%'):[self.ACCEPTK],
                        (7,'&'):[self.ACCEPTK],
                        (8,'!'):[self.ACCEPTK],
                        (9,'#'):[self.ACCEPTK],
                        (10,' '):[self.ACCEPTK],
                        (11,'='):[self.ACCEPTK],
                        (12,';'):[self.ACCEPTK],
                        (13,','):[self.ACCEPTK],
                        (14,'\n'):[self.ACCEPTK],
                        (15,'('):[self.ACCEPTK],
                        (16,'['):[self.ACCEPTK],
                        (17,')'):[self.ACCEPTK],
                        (18,']'):[self.ACCEPTK],
                        (19,'>'):[self.ACCEPTK],
                        (20,'<'):[self.ACCEPTK],
                        (21,'+'):[self.ACCEPTK],
                        (22,'-'):[self.ACCEPTK],
                        (23,'*'):[self.ACCEPTK],
                        (24,'/'):[self.ACCEPTK],
                        }
        self.ACCEPTING = [self.ACCEPTK]
         
    def fsm(self, character):
        patsymbol = character
        # general letter and digit patsymbol mapping
        if self.letter(character):
            patsymbol = 'letter'
        else:
           if self.digit(character):
               patsymbol = 'digit'
               
        stateXist = False
        
        for eachCurrSs in self.current:
            if self.EDGES.get((eachCurrSs, patsymbol)) != None:
                self.current = self.EDGES.get((eachCurrSs, patsymbol))
                stateXist = True
                for sst in  self.current:
                    if sst in self.ACCEPTING:
                        return "ACCEPTED"
                    else:
                        self.Idetected = self.Idetected + character
                        return "CONTINUE"
                    break
                   
        if stateXist == False:
            self.__reset()
            return "NO_ACCEPTED"
                        
    def getRollBack(self):
        # it must be read just after accepting
        return self.ROLLBACK

    def getLex(self):
        lex = self.Idetected
        self.__reset()
        # logic operators are checked at first
        if lex.lower() in reserved:
            if lex.lower() == 'not':
                return '<token_neg,f?,c?>'
            elif lex.lower() == 'mod':
                return '<token_mod,f?,c?>'
            elif lex.lower() == 'or':
                return '<token_o,f?,c?>'
            elif lex.lower() == 'and':
                return '<token_y,f?,c?>'
            elif lex.lower() == 'xor':
                return '<token_xor,f?,c?>'
            else:
                return "<%s,f?,c?>" % (lex.lower())
        else:
            return "<id,%s,f?,c?>" % (lex.lower())
        
    def __reset(self):
        self.Idetected = ''
        self.current = [1]

# number detector
# #########################################
class Numbers(Symbol):
    
    def __init__(self):
        self.SINGLEDEC = 6
        self.DOUBLEDEC = 15
        self.Idetected = ''
        self.ACCEPTK = 27
        self.ROLLBACK = 1
        self.current = [1,2,3]
        self.EDGES = {(1,'-'):[2,3],
                        (2,'.'):[4],
                        (3,'digit'):[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
                        (4,'digit'):[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
                        (5,'_'):[self.ACCEPTK],
                        (6,'$'):[self.ACCEPTK],
                        (7,'%'):[self.ACCEPTK],
                        (8,'&'):[self.ACCEPTK],
                        (9,'!'):[self.ACCEPTK],
                        (10,'#'):[self.ACCEPTK],
                        (11,' '):[self.ACCEPTK],
                        (12,'='):[self.ACCEPTK],
                        (13,';'):[self.ACCEPTK],
                        (14,','):[self.ACCEPTK],
                        (15,'\n'):[self.ACCEPTK],
                        (16,'('):[self.ACCEPTK],
                        (17,'['):[self.ACCEPTK],
                        (18,')'):[self.ACCEPTK],
                        (19,']'):[self.ACCEPTK],
                        (20,'>'):[self.ACCEPTK],
                        (21,'<'):[self.ACCEPTK],
                        (22,'+'):[self.ACCEPTK],
                        (23,'-'):[self.ACCEPTK],
                        (24,'*'):[self.ACCEPTK],
                        (25,'/'):[self.ACCEPTK],
                        (26,'letter'):[self.ACCEPTK],
                        }
        self.ACCEPTING = [self.ACCEPTK]
         
    def fsm(self, character):
        patsymbol = character
        # general letter and digit patsymbol mapping
        if self.letter(character):
            patsymbol = 'letter'
        else:
           if self.digit(character):
               patsymbol = 'digit'
               
        stateXist = False
        
        for eachCurrSs in self.current:
            if self.EDGES.get((eachCurrSs, patsymbol)) != None:
                self.current = self.EDGES.get((eachCurrSs, patsymbol))
                stateXist = True
                for sst in  self.current:
                    if sst in self.ACCEPTING:
                        return "ACCEPTED"
                    else:
                        self.Idetected = self.Idetected + character
                        # print self.Idetected
                        return "CONTINUE"
                    break
                   
        if stateXist == False:
            self.__reset()
            # print "NUMBER NO ACCEPTED"
            return "NO_ACCEPTED"
                        
    def getRollBack(self):
        # it must be read just after accepting
        return self.ROLLBACK

    def getLex(self):
        lex = self.Idetected
        self.__reset()
        if lex.find('.') >= 0:
            if len(lex[lex.find('.')+1:]) <= self.SINGLEDEC:
                return "<token_single,%s,f?,c?>" %(lex)
            else:
                return "<token_double,%s,f?,c?>" %(lex)
        else:
            if int(lex) >= -32767 and int(lex) < 32768:
                return "<token_integer,%s,f?,c?>" %(lex)
            else:
                return "<token_long,%s,f?,c?>" %(lex)

    def __reset(self):
        self.Idetected = ''
        self.current = [1,2,3]

# operand detector
# #########################################
class Relops(Symbol):
    
    def __init__(self):
        self.OPS = {'=':'token_igual',
                    '<>':'token_dif',
                    '<':'token_menor',
                    '>':'token_mayor',
                    '<=':'token_menor_igual',
                    '>=':'token_mayor_igual',
                    '+':'token_mas',
                    '-':'token_menos',
                    '/':'token_div',
                    '*':'token_mul',
                    '(':'token_par_izq',
                    ')':'token_par_der',
                    ';':'token_pyc',
                    ',':'token_coma',
                    '^':'token_pot',
                    '%':'token_porcentaje',
                    '&':'token_ampersand',
                    '!':'token_admiracion',
                    '#':'token_numeral',
                    '$':'token_pesos'
            }
        
        self.Idetected = ''
        self.ROLLBACK = 0
        self.current = 0
        
    def fsm(self, character):
        self.Idetected = self.Idetected + character
        self.current = self.current + 1
        # it is always two character consumed
        if self.current == 2:
            if self.Idetected in self.OPS:
                self.ROLLBACK = 0
                return "ACCEPTED"
            elif self.Idetected[0:1] in self.OPS:
                self.ROLLBACK = 1
                self.Idetected = self.Idetected[0:1]
                return "ACCEPTED"
            else:
                self.__reset()
                return "NO_ACCEPTED"
        else:
            return "CONTINUE"
            
            
    def getRollBack(self):
        # it must be read just after accepting
        return self.ROLLBACK

    def getLex(self):
        lex = self.Idetected
        self.__reset()
        return "<%s,f?,c?>" % (self.OPS[lex])

    def __reset(self):
        self.Idetected = ''
        self.ROLLBACK = 0
        self.current = 0

# string detector
# #########################################
class Stringk(Symbol):
    
    def __init__(self):
        self.Idetected = ''
        self.ACCEPTK = 25
        self.ROLLBACK = 0
        self.WHOLESSLST = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        self.current = [1]
        # it must start with a " symbol
        self.EDGES = {(1,'"'):self.WHOLESSLST,
                        (2,'letter'):self.WHOLESSLST,
                        (3,'digit'):self.WHOLESSLST,
                        (4,'_'):self.WHOLESSLST,
                        (5,'$'):self.WHOLESSLST,
                        (6,'%'):self.WHOLESSLST,
                        (7,'&'):self.WHOLESSLST,
                        (8,'!'):self.WHOLESSLST,
                        (9,'#'):self.WHOLESSLST,
                        (10,' '):self.WHOLESSLST,
                        (11,'='):self.WHOLESSLST,
                        (12,';'):self.WHOLESSLST,
                        (13,','):self.WHOLESSLST,
                        (14,'('):self.WHOLESSLST,
                        (15,'['):self.WHOLESSLST,
                        (16,')'):self.WHOLESSLST,
                        (17,']'):self.WHOLESSLST,
                        (18,'>'):self.WHOLESSLST,
                        (19,'<'):self.WHOLESSLST,
                        (20,'+'):self.WHOLESSLST,
                        (21,'-'):self.WHOLESSLST,
                        (22,'*'):self.WHOLESSLST,
                        (23,'/'):self.WHOLESSLST,
                        (24,'"'):[self.ACCEPTK]
                        }
        self.ACCEPTING = [self.ACCEPTK]
        
    def fsm(self, character):
        patsymbol = character
        # general letter and digit patsymbol mapping
        if self.letter(character):
            patsymbol = 'letter'
        else:
           if self.digit(character):
               patsymbol = 'digit'
               
        stateXist = False
        
        for eachCurrSs in self.current:
            if self.EDGES.get((eachCurrSs, patsymbol)) != None:
                self.current = self.EDGES.get((eachCurrSs, patsymbol))
                stateXist = True
                for sst in  self.current:
                    if sst in self.ACCEPTING:
                        self.Idetected = self.Idetected + character
                        return "ACCEPTED"
                    else:
                        self.Idetected = self.Idetected + character
                        return "CONTINUE"
                    break
                
        if stateXist == False:
            self.__reset()
            return "NO_ACCEPTED"
            
            
    def getRollBack(self):
        # it must be read just after accepting
        return self.ROLLBACK

    def getLex(self):
        lex = self.Idetected
        self.__reset()
        return "<token_string,%s,f?,c?>" % (lex)

    def __reset(self):
        self.Idetected = ''
        self.current =[1]

# Auxiliary function for token detection 
def detect(detector, baseIndex, code, colCtr):
    retVal = [None,None,None]
    for j in range(baseIndex,len(code)):
                   accepted = detector.fsm(code[j])
                   colCtr = colCtr + 1
                   if  (accepted == "NO_ACCEPTED") or (accepted == "ACCEPTED"):
                     retVal[0] = accepted
                     retVal[1] = j
                     retVal[2] = colCtr
                     
                     return retVal
    # if end of code is reached and token has not been optained
    # a delimiter is passed to current detector fsm
    accepted = detector.fsm(' ')
    if  (accepted == "NO_ACCEPTED") or (accepted == "ACCEPTED"):
        retVal[0] = accepted
        retVal[1] = len(code)
        retVal[2] = colCtr
        return retVal
                   
    
    
# MAIN LOOP
# ########################################
# reserved word and idetifiers tokec detector
lakey = Identifier()
# numerical token detector
numnum = Numbers()
# operand token detector
opss = Relops()
# string token detector
strTkn = Stringk()

"""
strTest = "\n"
lines = sys.stdin.readlines()

for line in lines:
   strTest = strTest + line


strTest = strTest + "\n"

"""
 
strTest ="""
SUB floyd_warsall (n%)
FOR k = 1 TO n%
    FOR i = 1 TO n%
        FOR j = 1 TO n%
            G(i, j) = min(G(i, j), G(i, k) + G(k, j))
        NEXT
    NEXT
NEXT
END SUB
"""



detectors = {0:lakey,1:opss,2:numnum,3:strTkn}
detIndex = 0
i = 0
rowCtr = 0
colCtr = 0

while i < len(strTest):
    if strTest[i] == "'":
        # print "Comment Catched"
        while strTest[i] != "\n":
            i = i + 1
    # new line counter increment
    if strTest[i] == '\n':
        rowCtr = rowCtr + 1
        # Column base offset 0 or -1
        colCtr = 0
    # before entering detection \n and space are ignored
    if strTest[i] != '\n' and strTest[i] != ' ':
        startI = i
        # Call current indexed detector fsm
        acceptxt = detect(detectors[detIndex], startI, strTest, colCtr)
        if acceptxt[0] == "ACCEPTED":
                   rollBack = detectors[detIndex].getRollBack()
                   acceptxt[1] = acceptxt[1] - rollBack
                   lex = detectors[detIndex].getLex()
                   lex = lex.replace('f?',str(rowCtr))
                   lex = lex.replace('c?',str(colCtr))
                   print lex
                   detIndex = 0
                   colCtr = acceptxt[2] - rollBack
                   i = acceptxt[1] + 1
        else:
                   if detIndex >=3:
                     print "Error lexico (linea: %s, posicion: %s)"  %(str(rowCtr),str(colCtr) )
                     break
                   else:
                     # Check next detector FSM
                     detIndex = detIndex + 1
                     i = startI
    else:
        # column counter increment
        colCtr = colCtr + 1
        i = i + 1
    
                   


