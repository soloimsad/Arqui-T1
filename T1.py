#VARIABLES GLOBALES

count=0 #contador de operaciones suma
from decimal import Decimal
import re


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
    
    if (binario_int(e1)>binario_int(e2)): # e1 mayor a e1, por lo tanto se debe mover e2 a la izquierda
       
        m2= "1."+m2 #num2 menor #1.1 -> 0.11 
        pos_punto=buscar_punto(m2)
        cantidad_decimales=  binario_int(e1)-binario_int(e2) #me muevo a la izquierda
        m2 ="0" + "." + "0"*(cantidad_decimales-1) + m2[:pos_punto] + m2[pos_punto+1:]
        m1 ="1."+m1

    elif (binario_int(e2)>binario_int(e1)): #el mayor es e1 e2 x lo tanto se debe mover el e1 a la izquierda compare veces
        
        m1= "1."+m1 
        pos_punto = buscar_punto(m1)  
        cantidad_decimales=  binario_int(e2)-binario_int(e1) #me muevo a la izquierda
        m1 ="0" + "." + "0"*(cantidad_decimales-1) + m1[:pos_punto] + m1[pos_punto+1:]
        m2 ="1."+ m2
    
    else:
        m1="1."+m1
        m2="1."+m2
    

    max_mantisa = max(len(cortar_mantisa(m1)),len(cortar_mantisa(m2)))
    
    
    m1 = cortar_mantisa(m1) +"0"*(-len(cortar_mantisa(m1))+max_mantisa)
    m2 = cortar_mantisa(m2) +"0"*(-len(cortar_mantisa(m2))+max_mantisa)
    
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

    pos_punto = buscar_punto(result) # nos retorna la pos del punto 1 o 2,
    result = result[0] + "." + result[1:pos_punto] + result[pos_punto+1:] 
    
    if (binario_int(e1) >= binario_int(e2)):

        if (pos_punto == 1):
            e = binario_int(e1)
        else:
            e = binario_int(e1)+1
            
    else:

        if (pos_punto == 1):
            e = binario_int(e2)
        else:
            e = binario_int(e2)+1
            
    e = decimal_a_binario(e)
    while len(e) < 8:
        e = "0" + e
    mantissa = result[2:]
    while len(mantissa) < 23:
        mantissa += "0"
    final = sig1 + e + mantissa

    return final[:32] 

def buscar_uno(num):
    cont=0
    for i in num:
        
        if (i == "0" or i =="."):
            cont+=1
        else:
            return cont - 2
        
def binario_a_ieee754(numero):
    
    cont = 0
    aux = numero[0]

    if float(numero) > 0:
        ss = "0"
    else:
        ss = "1"
        numero = numero[1:]

    pos_punto = buscar_punto(numero)

    if pos_punto == 0:
        pos_punto = len(numero)
    e = pos_punto - 1
    
    if (aux == "0"):       #busca el primer 1
        cont= buscar_uno(numero)
        e = -cont-1
   
    nuevo_numero = numero[0] + "." + numero[1:pos_punto] + numero[pos_punto+1:]
    
    if(e<0):

        mantissa= nuevo_numero[-e+2:]
    else:
        mantissa = nuevo_numero[2:]

    while len(mantissa) < 23:
        mantissa += "0"
    
    ee = e + 127
    ee = str(decimal_a_binario(ee))
    

    if binario_int(ee)>127:
        while len(ee)< 8:
            ee+="0"
    else:
        while len(ee)<8:
            ee= "0"+ee

    numero_ieee754 = ss + ee + mantissa
    

    if (len(numero_ieee754)>32):
        numero_ieee754= numero_ieee754[:32]

    
    #print(numero_ieee754[:1],numero_ieee754[1:9],numero_ieee754[9:])

    return numero_ieee754
        
def decimal_a_binario(numero):
    binario = ""
    if numero < 0:
        signo = "-"
        numero = abs(numero)
    else:
        signo = ""
    
    parte_entera = int(numero)
   
    if(parte_entera==0):
        binario="0"
    parte_decimal = numero - parte_entera
    aux= parte_entera
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
            parte_decimal=round(parte_decimal,5)
        
            if parte_decimal >= 1:
                p_d_b += "1"
                parte_decimal -= 1
            else:
                p_d_b += "0"
            cont_digitos += 1
        
        if aux != 0:
       
            numero_binario = signo + binario + "." + p_d_b
            return (numero_binario)
        else:
            #en este caso le agrego mas numeros a la mantissa para que no falten numeros al shiftear
            while cont_digitos < 23 + 10:
                parte_decimal = parte_decimal * 2
                parte_decimal=round(parte_decimal,5)
        
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

fallas=0
lista_escribir=[]

with open('operaciones.txt','r') as archivo:

    for linea in archivo:
        linea = linea.strip().split(";")
        
        if(len(linea)>=2):
            temp1 = (linea[0])
            temp2 = (linea[1])
            if(temp1!="" and temp2!= ""):

                temp1 = float(linea[0])
                temp2 = float(linea[1])
                num1 = decimal_a_binario(temp1)
                num2 = decimal_a_binario(temp2)
                num1 = binario_a_ieee754(num1)
                num2 = binario_a_ieee754(num2)

                if ((temp1 >= 0) and (temp2 >= 0)) or (((temp1 <= 0) and (temp2 <= 0))):

                    resultado = sum(num1,num2)
                    count += 1
                    string_salida = str(round(ieee754_a_decimal(resultado),3)) + "/" + resultado[:1]+" "+resultado[1:9]+" "+resultado[9:]
                    lista_escribir.append(string_salida)
                                
                else:

                    fallas+=1
                    string_salida= str(round(temp1,3)) + "/" + num1 + ";" + str(round(temp2,3)) + "/" + num2 
                    lista_escribir.append(string_salida)
            else:
                fallas+=1

        else:
            fallas+=1

with open('resultados.txt','w') as archivo:
   for i in lista_escribir:
       archivo.write(i+"\n")


if(count+fallas==0):
    print("No se pudieron procesar lineas")

else:
    print("Se pudieron procesar", count+fallas, "lineas")

if (count==0):
    print("No fue posible hacer sumas")

else:
    print("Fue posible hacer", count,"sumas")

if (fallas==0):
     print("No hubo problemas al procesar sumas")

else:
     print("No se pudo procesar", fallas, "sumas")



