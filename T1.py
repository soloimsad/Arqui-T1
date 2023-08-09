#VARIABLES GLOBALES
count=0 #contador de operaciones suma

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

def sum(num1, num2):
    m1= num1[9:]
    m2= num2[9:]
    s1= num1[:1]
    s2= num2[:1]
    #ajustar cifras significativas
    e1= num1[1:9]
    e2= num2[1:9]
    compare= binario_int(e1)-binario_int(e2)
    if (compare > 0): #caso en el que e1 mayor que e2
        m2="1"+m2
        m2= "0."+"0"*(compare-1)+m2
        m1="1."+m1
    else:
        m1="1"+m1
        m1="0."+"0"*abs(compare-1)+m1
        m2="1."+m2
    
    #proceso de suma
    print(cortar_mantisa(m1),len(m2))
  



def binario_a_ieee754(numero):
    if float(numero) > 0:
        ss = "0"
    else:
        ss = "1"
        numero = numero[1:]
    cont = 0
    pos_punto = 0
    for char in numero:
        if char == ".":
            pos_punto = cont
            e = pos_punto - 1
        cont += 1
    nuevo_numero = numero[0] + "." + numero[1:pos_punto] + numero[pos_punto+1:]
    mantissa = nuevo_numero[2:]
    while len(mantissa) < 23:
        mantissa += "0"
    ee = e + 127
    ee = str(decimal_a_binario(ee))
    numero_ieee754 = ss + ee + mantissa
   
    lista1 = [ss,ee,mantissa]
    return lista1

        


"""
def binary_to_i3e754(number):
    if (binario >= 0):
        signo = 0
    else:
        signo = 1

    binario = abs(binario)

   
    parte_entera, parte_decimal = str(binario).split(".")
    parte_entera = int(parte_entera)
    parte_decimal = int(parte_decimal)

   
    entero_binario = ""
    while parte_entera > 0:
        entero_binario = str(parte_entera % 2) + entero_binario
        parte_entera //= 2

   
    decimal_binario = ""
    while parte_decimal > 0:
        parte_decimal *= 2
        decimal_binario += str(int(parte_decimal))
        parte_decimal -= int(parte_decimal)

  
    numero_binario = entero_binario + "." + decimal_binario

   
    exponente = 127 + len(entero_binario) - 1
    exponente_binario = format(exponente, '08b')

 
    mantisa_binaria = (entero_binario + decimal_binario)[:23].ljust(23, '0')

    
    return signo + exponente_binario + mantisa_binaria
"""

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
        while cont_digitos < len(str(parte_decimal))+1:
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

"""
def binary(number):
    if number < 0:
        sig= "-"
        number=abs(number)
    else:
        sig=""
    main = int(number)
    d = number - main
    binaryPart= bin(main)[2:]
    dPart= ""
    for _ in range(23):
        d *= 2
        bit= int(d)
        dPart += str(bit)
        d -= bit
        if d == 0:
            break 

    return f"{sig}{binaryPart}.{dPart}"
"""
def binario_int(num):
    decimal =0
    largo = len(num)
    for i, digito in enumerate(num):
        if digito=="1":
            exponente = largo- i - 1
            decimal += 2 ** exponente
    return decimal


def sum(num1, num2):
    m1= num1[9:]
    m2= num2[9:]
    s1= num1[:1]
    s2= num2[:1]
    #ajustar cifras significativas
    e1= num1[1:9]
    e2= num2[1:9]
    compare= binario_int(e1)-binario_int(e2)
    if (compare > 0): #caso en el que e1 mayor que e2
        m2="1"+m2
        m2= "0,"+"0" * (compare-1)+m2
        m1="1,"+m1
    else:
        m1="1"+m1
        m1="0,"+"0" * abs(compare-1)+m1
        m2="1,"+m2

"""
def float_to_binary(linea):
    pos = linea.index(";")
    Num1= linea[:pos]
    Num2= linea[pos+1:]
    Num2= Num2.replace("\n","")
    Num1= binary(float(Num1))
    Num2= binary(float(Num2))
    return 
"""

with open('operaciones.txt','r') as archivo:
    for linea in archivo:
        linea = linea.strip().split(";")
        num1 = decimal_a_binario(float(linea[0]))
        num2 = decimal_a_binario(float(linea[1]))
        
        #float_to_binary(linea)

b = decimal_a_binario(-118.625)

c = binario_a_ieee754(b)
