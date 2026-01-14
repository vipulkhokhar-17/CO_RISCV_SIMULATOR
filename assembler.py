def RType(m1):
    r1=line.split(",")[0]
    r1f=r1.split()[1].strip()
    r2=line.split(",")[1]
    r3=line.split(",")[2].strip()
    if (m1=='add'):
        radd= '1100110'+dict[r1f]+'000'+dict[r2]+dict[r3]+'0000000'
        return radd
    elif (m1=='sub' and r2=='00000'):
        rsubz= '1100110'+dict[r1f]+'000'+'00000'+dict[r3]+'0000010'
        return rsubz
    elif (m1=='sub' and r2!='00000'):
        rsub='1100110'+dict[r1f]+'000'+dict[r2]+dict[r3]+'0000010'
        return rsub
    elif (m1=='sll'):
        rsll= '1100110'+dict[r1f]+'001'+dict[r2]+dict[r3]+'0000000'
        return rsll
    elif (m1=='slt'):
        rslt= '1100110'+dict[r1f]+'010'+dict[r2]+dict[r3]+'0000000'
        return rslt
    elif (m1=='sltu'):
        rsltu= '1100110'+dict[r1f]+'011'+dict[r2]+dict[r3]+'0000000'
        return rsltu
    elif (m1=='xor'):
        rxor= '1100110'+dict[r1f]+'100'+dict[r2]+dict[r3]+'0000000'
        return rxor
    elif (m1=='srl'):
        rsrl= '1100110'+dict[r1f]+'101'+dict[r2]+dict[r3]+'0000000'
        return rsrl
    elif (m1=='or'):
        ror= '1100110'+dict[r1f]+'110'+dict[r2]+dict[r3]+'0000000'
        return ror
    elif (m1=='and'):
        rand= '1100110'+dict[r1f]+'111'+dict[r2]+dict[r3]+'0000000'
        return rand
    else:
        relse='error in line number: ',i 
        return relse
    
def posimm(mff):
    bsmff= bin(mff)[2:]
    ubsmff=bsmff.zfill(12) 
    return ubsmff

def negimm(mff):
    if mff >= 0:
        raise ValueError

    absmff= bin(abs(mff))[2:]
    tc= bin((int(absmff, 2) ^ ((1 << len(absmff)) - 1)) + 1)[2:]
    tc=tc[-12:].zfill(12)
    return tc


def posimmtt(n):
    bn= bin(n)[2:]
    ubn= bn.zfill(32)
    return ubn

def negimmtt(n):
    if n >= 0:
        raise ValueError

    abn= bin(abs(n))[2:]
    tc= bin((int(abn, 2) ^ ((1 << len(abn)) - 1)) + 1)[2:]
    tc=tc[-32:].zfill(32)
    return tc


    
def IType(m1):

    if (m1=='lw'):
        r1i=line.split(",")[0]
        r1=r1i.split(" ")[1]
        r2i=line.split(",")[1]
        r2=r2i.split("(")[0]
        r3i=r2i.split("(")[1]
        r3=r3i.split(")")[0]
        r2=int(r2)
        if(r2>0):
            mbb=posimm(r2)
        elif (r2<0):
            mbb=negimm(r2)
        else:
            mbb= '0000 0000 0000'

        Ilw='1100000'+dict[r1]+'010'+dict[r3]+mbb[0:12]
        return Ilw
    
    elif (m1=='addi'):
        r1i=line.split(",")[0]
        r1=r1i.split(" ")[1]
        r2=line.split(",")[1]
        r3=line.split(",")[2]
        r3=int(r3)
        if(r3>0):
            mbb=posimm(r3)
        elif (r3<0):
            mbb=negimm(r3)
        else:
            mbb= '0000 0000 0000'

        Iaddi='1100100'+dict[r1]+'000'+dict[r2]+mbb[0:12]
        return Iaddi
    
    elif (m1=='sltiu'):
        r1i=line.split(",")[0]
        r1=r1i.split(" ")[1]
        r2=line.split(",")[1]
        r3=line.split(",")[2]
        r3=int(r3)
        if(r3>0):
            mbb=posimm(r3)
        elif (r3<0):
            mbb=negimm(r3)
        else:
            mbb= '0000 0000 0000'

        Isltiu='1100100'+dict[r1]+'110'+dict[r2]+mbb[0:12]
        return Isltiu
    
    else:
        r1i=line.split(",")[0]
        r1=r1i.split(" ")[1]
        r2=line.split(",")[1]
        r3=line.split(",")[2]
        r3=int(r3)
        if(r3>0):
            mbb=posimm(r3)
        elif (r3<0):
            mbb=negimm(r3)
        else:
            mbb= '0000 0000 0000'

        Ijalr='1110011'+dict[r1]+'000'+dict[r2]+mbb[0:12]
        return Ijalr


def SType(m1):
    r1i=line.split(",")[0]
    r1=r1i.split(" ")[1]
    r2i=line.split(",")[1]
    r2=r2i.split("(")[0]
    r3i=r2i.split("(")[1]
    r3=r3i.split(")")[0]
    v=int(r2)

    if v>0:
        r2bin=posimm(v)
    elif v<0:
        r2bin=negimm(v)
    elif v==0:
        r2bin='000000000000'

    ssw= '1100010'+dict.get(r2bin[0:5], '00000')+'010'+dict.get(r3 , '00000')+dict.get(r1, '00000')+dict.get(r2bin[5:12], '00000')
    return ssw

def BType(m1):

    r1i=line.split(",")[0]
    r1=r1i.split(" ")[1]
    r2=line.split(",")[1]
    r3=line.split(",")[2]
    v=int(r3)
    if v>0:
        i=posimm(v)
    elif v<0:
        i=negimm(v)
    else:
        i='000000000000'
    
    if (m1=='beq'):
        bbeq= '1100011'+i[10]+i[1:5]+'000'+dict[r1]+dict[r2]+i[5:11]+i[11]
        return bbeq
    elif (m1=='bne'):
        bbne= '1100011'+i[10]+i[1:5]+'001'+dict[r1]+dict[r2]+i[5:11]+i[11]
        return bbne
    elif (m1=='blt'):
        bblt= '1100011'+i[10]+i[1:5]+'100'+dict[r1]+dict[r2]+i[5:11]+i[11]
        return bblt
    elif (m1=='bge'):
        bbge= '1100011'+i[10]+i[1:5]+'101'+dict[r1]+dict[r2]+i[5:11]+i[11]
        return bbge
    elif (m1=='bltu'):
        bbltu= '1100011'+i[10]+i[1:5]+'110'+dict[r1]+dict[r2]+i[5:11]+i[11]
        return bbltu
    elif (m1=='bgeu'):
        bbgeu= '1100011'+i[10]+i[1:5]+'111'+dict[r1]+dict[r2]+i[5:11]+i[11]
        return bbgeu
    else:
        relse='error in line number: ',i 
        return relse

def UType(m1):

    r1i=line.split(",")[0]
    r1=r1i.split(" ")[1]
    r2=line.split(",")[1]
    v=int(r2)
    if v>0:
        i=posimmtt(v)
    elif v<0:
        i=negimmtt(v)
    elif v==0:
        i='00000000000000000000000000000000'

    if (m1=='lui'):
        ului= '1110110'+dict[r1]+i[12:32]
        return ului
    elif (m1=='auipc'):
        uauipc= '1110100'+dict[r1]+i[12:32]
        return uauipc
    else:
        relse='error in line number: ',i 
        return relse

def JType(m1):

    r1i=line.split(",")[0]
    r1=r1i.split(" ")[1]
    r2=line.split(",")[1]
    v=int(r2)
    if v>0:
        i=posimmtt(v)
    elif v<0:
        i=negimmtt(v)
    elif v==0:
        i='00000000000000000000000000000000'

    jjal= '1111011'+dict[r1]+i[12:20]+i[11]+i[1:11]+i[20]
    return jjal


dict = {
    'zero':'00000',
    'sp':'01000',
    'a1':'11010',
    'gp':'11000',
    'a3':'10110',
    'tp':'00100',
    't0':'10100',
    't1':'01100',
    't2':'11100',
    's0':'00010',
    # 'fp':'01000',
    's1':'10010',
    'a0':'01010',
    'a2':'01110',
    'a5':'11110',
    'a6':'00001',
    'a7':'10001',
    's2':'01001',
    's3':'11001',
    's4':'00101',
    's5':'10101',
    's6':'01101',
    's7':'11101',
    's8':'00011',
    's9':'10111',
    's10':'01011',
    's11':'11011',
    't3':'00111',
    't4':'10111',
    't5':'01111',
    't6':'11111',
    'ra':'10000'
}


with open('file.txt','r') as input_file:
    
    i=0
    with open('output.txt','w') as output_file:
        while True:
            i=i+1
            line=input_file.readline()
            if not line:
                break
            
            m1=line.split(" ")[0]
            

            if m1 in ['add','sub','sll','slt','sltu','xor','srl','or','and']:
                result=RType(m1)
               
            
            elif m1 in ['lw','addi','sltin','jalr']:
                result= IType(m1)
                

            elif m1 in ['sw']:
                result= SType(m1)

            elif m1 in['beq','bne','blt','bge','bltu','bgeu']:
                result= BType(m1)

            elif m1 in ['lui','auipe']:
                result= result= UType(m1)
                

            elif m1 in ['jal']:
                result= JType(m1)
                

            else:
                result= f'error in line number: {i}'
            
            output_file.write(result + '\n')
