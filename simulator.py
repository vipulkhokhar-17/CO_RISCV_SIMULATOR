import sys
import os

def par():
    drv['00000']='0'*32
    with open(output,'a') as f:
        f.write('0b'+sign_ext(signed_conv_down(str(reg_pc)))+' ')
        s=''
        for i in drv:
            s+=('0b'+drv[i]+' ')
        f.write(s)
        f.write('\n')


def pma():
    with open(output,'a') as f:
        s=''
        for i in dma:
            s+=(i+':0b'+dma[i]+'\n')
        f.write(s)


def signed_conv_down(imm_val):
    n=int(imm_val)
    if n<0:
        absval=abs(n)
        binary ='0'+bin(absval)[2:]
        inverted_bin_str = ''.join(['1' if bit=='0' else '0' for bit in binary])
        twos_complement=bin(int(inverted_bin_str, base=2)+1)[2:]
        return str(twos_complement)
    else:
        return '0'+str(bin(n)[2:])
 

def signed_conv_up(n):
    if(n[0]=='1'):
        reverse=''.join('1' if b=='0' else '0' for b in n)
        val=-(int(reverse,2)+1)
    else:
        val=(int(n,2))
    return val   

def htb(n):
    dhtb = {'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001','A':'1010','B':'1011','C':'1100','D':'1101','E':'1110','F':'1111'}
    n=''.join([dhtb[i] for i in n])
    return n


def sign_ext(imm_val):
    if(32-len(imm_val)<0): return imm_val[0:32]
    signed_bit=imm_val[0]
    k=(32-len(imm_val))*signed_bit
    imm_val=k+imm_val
    return imm_val


def add(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    value=sign_ext(signed_conv_down(signed_conv_up(drv[reg_source1])+signed_conv_up(drv[reg_source2])))
    drv[reg_dest]=value


def sub(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    value=sign_ext(signed_conv_down(signed_conv_up(drv[reg_source1])-signed_conv_up(drv[reg_source2])))
    drv[reg_dest]=value


def xor(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    value=sign_ext(signed_conv_down(signed_conv_up(drv[reg_source1])^signed_conv_up(drv[reg_source2])))
    drv[reg_dest]=value


def Or(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    value=sign_ext(signed_conv_down(signed_conv_up(drv[reg_source1])|signed_conv_up(drv[reg_source2])))
    drv[reg_dest]=value


def And(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    value=sign_ext(signed_conv_down(signed_conv_up(drv[reg_source1])&signed_conv_up(drv[reg_source2])))
    drv[reg_dest]=value


def lw(m_line):
    imm_val=m_line[0:12]
    reg_source=m_line[12:17]
    reg_dest=m_line[20:25]
    value=signed_conv_up(drv[reg_source])+signed_conv_up(sign_ext(imm_val))
    value=hex(value)
    value='0x'+(10-len(value))*'0'+value[2:]
    drv[reg_dest]=dma[value]


def bgeu(m_line):
    global reg_pc
    imm_val=m_line[0]+m_line[24]+m_line[1:7]+m_line[20:24]
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    if(int(drv[reg_source1],2)>=int(drv[reg_source2],2)):
        reg_pc=reg_pc+signed_conv_up(imm_val+'0')
        return 1
    return 0


def blt(m_line):
    global reg_pc
    imm_val=m_line[0]+m_line[24]+m_line[1:7]+m_line[20:24]
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    if(signed_conv_up(drv[reg_source1])<signed_conv_up(drv[reg_source2])):
        reg_pc=reg_pc+signed_conv_up(imm_val+'0')
        return 1
    return 0


def bltu(m_line):
    global reg_pc
    imm_val=m_line[0]+m_line[24]+m_line[1:7]+m_line[20:24]
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    if(int(drv[reg_source1],2)<int(drv[reg_source2],2)): 
        reg_pc=reg_pc+signed_conv_up(imm_val+'0')
        return 1
    return 0


def addi(m_line):
    imm_val=m_line[0:12]
    reg_source=m_line[12:17]
    reg_dest=m_line[20:25]
    drv[reg_dest]=sign_ext(signed_conv_down(signed_conv_up(drv[reg_source])+signed_conv_up(imm_val)))


def sltiu(m_line):
    imm_val=m_line[0:12]
    reg_source=m_line[12:17]
    reg_dest=m_line[20:25]
    drv[reg_dest]='0'*31+'1' if(int(drv[reg_source],2)<int(imm_val,2)) else drv[reg_dest]


def jalr(m_line):
    global reg_pc
    imm_val=m_line[0:12]
    reg_source=m_line[12:17]
    reg_dest=m_line[20:15]
    drv[reg_dest]=sign_ext(signed_conv_down(str((reg_pc+4))))
    reg_pc=(signed_conv_up(drv[reg_source])+signed_conv_up(sign_ext(imm_val)))


def sw(m_line):
    imm_val=m_line[0:7]+m_line[20:25]
    reg_source2=m_line[7:12]
    reg_source1=m_line[12: 17]
    value=hex(signed_conv_up(drv[reg_source1])+signed_conv_up(imm_val))
    value='0x'+(10-len(value))*'0'+value[2:]
    dma[value]=drv[reg_source2]


def slt(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    if(signed_conv_up(drv[reg_source1])<signed_conv_up(drv[reg_source2])): drv[reg_dest]='0'*31+'1'


def sll(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    value=sign_ext(signed_conv_down(int(drv[reg_source1],2)(2*int(drv[reg_source2][32-4-1:],2))))
    drv[reg_dest]=value


def sltu(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    if(int(drv[reg_source1],2)<int(drv[reg_source2],2)): drv[reg_dest]='0'*31+'1'


def srl(m_line):
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    reg_dest=m_line[20:25]
    value=sign_ext(signed_conv_down(int(drv[reg_source1],2)//(2**int(drv[reg_source2][32-4-1:],2))))
    drv[reg_dest]=value


def jal(m_line):
    global reg_pc
    imm_val=m_line[0]+m_line[12:20]+m_line[11]+m_line[1:9]
    reg_dest=m_line[20:25]
    drv[reg_dest]=sign_ext(signed_conv_down(str(reg_pc+4)))
    reg_pc+=signed_conv_up(imm_val+'0')


def beq(m_line):
    global reg_pc
    imm_val=m_line[0]+m_line[24]+m_line[1:7]+m_line[20:24]
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    if(signed_conv_up(drv[reg_source1])==signed_conv_up(drv[reg_source2])):
        reg_pc=reg_pc+signed_conv_up(imm_val+'0')
        return 1
    return 0


def bne(m_line):
    global reg_pc
    imm_val=m_line[0]+m_line[24]+m_line[1:7]+m_line[20:24]
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    if(signed_conv_up(drv[reg_source1])!=signed_conv_up(drv[reg_source2])):
        reg_pc=reg_pc+signed_conv_up(imm_val+'0')
        return 1
    return 0


def bge(m_line):
    global reg_pc
    imm_val=m_line[0]+m_line[24]+m_line[1:7]+m_line[20:24]
    reg_source2=m_line[7:12]
    reg_source1=m_line[12:17]
    if(signed_conv_up(drv[reg_source1])>=signed_conv_up(drv[reg_source2])):
        reg_pc=reg_pc+signed_conv_up(imm_val+'0')
        return 1
    return 0


def lui(m_line):
    imm_val=m_line[0:20]+12*'0'
    reg_dest=m_line[20:25]
    drv[reg_dest]=imm_val


def auipc(m_line):
    imm_val=m_line[0:20]+12*'0'
    reg_dest=m_line[20:25]
    drv[reg_dest]=sign_ext(signed_conv_down(str(reg_pc+signed_conv_up(imm_val))))


input = sys.argv[1]
output = sys.argv[2]
if not os.path.exists(input):
    sys.exit("Input file path does not exist")


lr= ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111", "01000", "01001", "01010", "01011", "01100", "01101", "01110", "01111", "10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111", "11000", "11001", "11010", "11011", "11100", "11101", "11110", "11111"]

lma=['0x00010000','0x00010004','0x00010008','0x0001000c','0x00010010','0x00010014','0x00010018','0x0001001c','0x00010020','0x00010024','0x00010028','0x0001002c','0x00010030','0x00010034','0x00010038','0x0001003c','0x00010040','0x00010044','0x00010048','0x0001004c','0x00010050','0x00010054','0x00010058','0x0001005c','0x00010060','0x00010064','0x00010068','0x0001006c','0x00010070','0x00010074','0x00010078','0x0001007c']

drv={key:'0'*32 for key in lr}

drv["00010"]='00000000000000000000000100000000'

dma={key:'0'*32 for key in lma}

dla={}

with open(input,'r') as f:
    lma=[i.rstrip('\n') for i in f.readlines()]
reg_pc=0
line_cntr=0

for i in lma:
    dla[line_cntr]=i
    line_cntr+=4

with open(output,'w') as f:
    {}

while(reg_pc<=line_cntr):
    m_line=dla[reg_pc]
    if(m_line[17:20]=='010' and m_line[25:]=='0000011'):
        lw(m_line)
        reg_pc+=4
        par()
   
    elif(m_line[0:7]=='0000000' and m_line[17:20]=='000' and m_line[25:]=='0110011') :
        add(m_line)
        reg_pc+=4
        par()

    elif(m_line[17:20]=='000' and m_line[25:]=='0010011'):
        addi(m_line)
        reg_pc+=4
        par()

    elif(m_line[17:20]=='011' and m_line[25:]=='0000011'):
        sltiu(m_line)
        reg_pc+=4
        par()
    
    elif(m_line[17:20]=='000' and m_line[25:]=='1100011'):
      flag=beq(m_line)
      if(flag==0): reg_pc+=4
      par()
      if(m_line[0:25]=='0'*25):
          break
      
    elif(m_line[17:20]=='000' and m_line[25:]=='1100111'):
        jalr(m_line)
        par()

    elif(m_line[17:20]=='010' and m_line[25:]=='0100011'):
        sw(m_line)
        reg_pc+=4
        par()

    elif(m_line[0:7]=='0100000' and m_line[17:20]=='000' and m_line[25:]=='0110011'):
        sub(m_line)
        reg_pc+=4
        par()

    elif(m_line[0:7]=='0000000' and m_line[17:20]=='001' and m_line[25:]=='0110011'):
        sll(m_line)
        reg_pc+=4
        par()

    elif(m_line[0:7]=='0000000' and m_line[17:20]=='010' and m_line[25:]=='0110011'):
        slt(m_line)
        reg_pc+=4
        par()
    
    elif(m_line[0:7]=='0000000' and m_line[17:20]=='101' and m_line[25:]=='0110011'):
        srl(m_line)
        reg_pc+=4
        par()


    elif(m_line[0:7]=='0000000' and m_line[17:20]=='100' and m_line[25:]=='0110011'):
        xor(m_line)
        reg_pc+=4
        par()

    elif(m_line[0:7]=='0000000' and m_line[17:20]=='110' and m_line[25:]=='0110011'):
        Or(m_line)
        reg_pc+=4
        par()

    elif(m_line[0:7]=='0000000' and m_line[17:20]=='111' and m_line[25:]=='0110011'):
        And(m_line)
        reg_pc+=4
        par()

    elif(m_line[17:20]=='001' and m_line[25:]=='1100011'):
      flag=bne(m_line)
      if(flag==0): reg_pc+=4
      par()
    
    elif(m_line[25:]=='0010111'):
        auipc(m_line)
        reg_pc+=4
        par()

    elif(m_line[17:20]=='100' and m_line[25:]=='1100011'):
      flag=blt(m_line)
      if(flag==0): reg_pc+=4
      par()

    elif(m_line[17:20]=='101' and m_line[25:]=='1100011'):
      flag=bge(m_line)
      if(flag==0): reg_pc+=4
      par()

    elif(m_line[17:20]=='110' and m_line[25:]=='1100011'):
      flag=bltu(m_line)
      if(flag==0): reg_pc+=4
      par()

    elif(m_line[17:20]=='111' and m_line[25:]=='1100011'):
      flag=bgeu(m_line)
      if(flag==0): reg_pc+=4
      par()

    elif(m_line[25:]=='0110111'):
        lui(m_line)
        reg_pc+=4
        par()

    elif(m_line[0:7]=='0000000' and m_line[17:20]=='011' and m_line[25:]=='0110011'):
        sltu(m_line)
        reg_pc+=4
        par()

    elif(m_line[25:]=='1101111'):
      jal(m_line)
      par()

pma()
