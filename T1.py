#VARIABLES GLOBALES
count=0 #contador de operaciones suma
from decimal import Decimal

def binario_int(num):
    decimal =0
    largo = len(num)
    for i, digito in enumerate(num):
        if digito=="1":
            exponente = largo- i - 1
            decimal += 2 ** exponente
    return decimal

def cortar_mantisa(num):
    slicer = 0
    for i in range(len(num) - 1, -1, -1):
        if num[i] == "0":
            slicer += 1
        else:
            break
    return num[:len(num)-slicer]

def buscar_punto(num):
    cont = 0
    pos_punto = 0
    for char in num:
        if char == ".":
            pos_punto = cont
        cont += 1    
    
    return pos_punto 

def sum(num1, num2):
    m1= num1[9:]
    m2= num2[9:]
    e1= num1[1:9]
    e2= num2[1:9]
    sig1= num1[:1]
    compare= binario_int(e1)-binario_int(e2)

    if (compare > 0): # e1 mayor a e1, por lo tanto se debe mover e2 a la izquierda
        
        
        m2= "0" + "." +"0"*(compare-1)+ "1" + m2
        m1= "1." + m1
        m2= m2[:25]

    else: #el mayor es e1 e2 x lo tanto se debe mover el e1 a la izquierda compare veces
        
        m1= abs(compare)*"0" + "." + "0"*(compare-1) +"1" + m1
        m2= "1." + m2
        m1=m1[:25]
    
    max_mantisa = max(len(cortar_mantisa(m1)),len(cortar_mantisa(m2)))
    
    
    m1 = cortar_mantisa(m1) +"0"*(-len(cortar_mantisa(m1))+max_mantisa)
    m2 = cortar_mantisa(m2) +"0"*(-len(cortar_mantisa(m2))+max_mantisa)
    #ya aqui quedan del mismo porte 

    
    result= ''
    carry = 0

    for i in range(max_mantisa - 1, -1, -1):

        if (m1[i] != "."):
            r = carry
            r += 1 if m1[i] == '1' else 0
            r += 1 if m2[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result
        
            carry = 0 if r < 2 else 1
        else:
            result =  "." + result 
            
    if carry != 0:
        result = '1' + result

    
    pos_punto = buscar_punto(result) # nos retorna la pos del punto
    result = result[0] + "." + result[1:pos_punto] + result[pos_punto+1:] 
    

    if (binario_int(e1) - 127 == 0):
        
        e = binario_int(e2)+1
        
    elif (binario_int(e2) -127 == 0):
        
        e = binario_int(e1)+1

    elif (binario_int(e1) >= binario_int(e2)):
        e = binario_int(e1)

    else:
        e = binario_int(e2)
    
    e = decimal_a_binario(e)
    
    mantissa = result[2:]
    while len(mantissa) < 23:
        mantissa += "0"
    
    final = sig1 + e + mantissa
    
    return final 



def binario_a_ieee754(numero):
    if float(numero) > 0:
        ss = "0"
    else:
        ss = "1"
        numero = numero[1:]

    pos_punto = buscar_punto(numero)
    
    if pos_punto == 0:
        pos_punto = len(numero)
    e = pos_punto - 1

    nuevo_numero = numero[0] + "." + numero[1:pos_punto] + numero[pos_punto+1:]
    mantissa = nuevo_numero[2:]
    while len(mantissa) < 23:
        mantissa += "0"
    
    ee = e + 127
    ee = str(decimal_a_binario(ee))
    while len(ee)< 8:
        ee="0"+ee
    
    numero_ieee754 = ss + ee + mantissa
    
    if (len(numero_ieee754)>32):
        numero_ieee754= numero_ieee754[:32]
    return numero_ieee754

        
def decimal_a_binario(numero):
    binario = ""
    if numero < 0:
        signo = "-"
        numero = abs(numero)
    else:
        signo = ""
    
    parte_entera = int(numero)
    parte_decimal = numero - parte_entera
    while parte_entera > 0:
        if parte_entera % 2 != 0:
            binario = "1" + binario 
        else:
            binario = "0" + binario 
        parte_entera = parte_entera // 2
    if parte_decimal != 0:
        p_d_b = ""
        cont_digitos = 0
        while cont_digitos < 23:
            parte_decimal = parte_decimal * 2
            if parte_decimal >= 1:
                p_d_b += "1"
                parte_decimal -= 1
            else:
                p_d_b += "0"
            cont_digitos += 1
        
        numero_binario = signo + binario + "." + p_d_b
        
        return (numero_binario)
    else:
        numero_binario = signo +  binario
        
        return numero_binario


def binario_int(num):
    decimal = 0
    largo = len(num)
    for i, digito in enumerate(num):
        if digito=="1":
            exponente = largo- i - 1
            decimal += 2 ** exponente
    return decimal

def ieee754_a_decimal(numero):
    m1 = numero[9:]
    s1 = numero[:1]
    e1 = numero[1:9]
    cont = 1
    sum = 1
    while cont < len(m1) + 1:
        sum += int(m1[cont-1]) * 1/(2**cont)
        cont += 1
    exponente = binario_int(e1) - 127
    numero2 = (2**exponente) * sum * (-1)**int(s1)
    return numero2



with open('operaciones.txt','r') as archivo:

    for linea in archivo:
        linea = linea.strip().split(";")
        temp1 = float(linea[0])
        temp2 = float(linea[1])

        if ((temp1 >= 0) and (temp2 >= 0)) or (((temp1 <= 0) and (temp2 <= 0))):
            
            num1 = decimal_a_binario(temp1)
            num2 = decimal_a_binario(temp2)
            num1 = binario_a_ieee754(num1)
            num2 = binario_a_ieee754(num2)
            
            resultado = sum(num1,num2)
            count += 1
            

        else:
            print("Buenas")



