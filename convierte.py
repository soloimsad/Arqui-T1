from decimal import Decimal

def binario_int(num):
    """
    binario_int(num)
    --------------------------
    num: numero binario
    --------------------------
    Funcion que transforma un numero binario en su forma decimal (base 10), retorna el numero transformado.
    """
    decimal =0
    largo = len(num)
    for i, digito in enumerate(num):
        if digito=="1":
            exponente = largo- i - 1
            decimal += 2 ** exponente
    return decimal

def cortar_mantisa(num):
    """
    cortar_mantisa(num): Esta funcion se encarga de cortar la mantisa hasta el ultimo 1 que encuentre 
    ---------------
    num: Es el numero que de la mantisa, este numero debe venir en codificacion binaria de punto flotante
    ----------------------------
    return num[:len(num)-slicer]: Corresponde a la nueva mantissa hasta el ultimo 1
    """
    slicer = 0
    for i in range(len(num) - 1, -1, -1):
        if num[i] == "0":
            slicer += 1
        else:
            break
    return num[:len(num)-slicer]

def buscar_punto(num):
    """
    buscar_punto(num)
    -------------------------
    num: numero binario
    -------------------------
    Funcion que recibe un numero binario y retorna la posicion del punto que separa la parte entera y decimal de este.
    En caso de no encontrar punto (que corresponderia a que el numero solo tiene parte entera) retorna 0.
    """
    cont = 0
    pos_punto = 0
    for char in num:
        if char == ".":
            pos_punto = cont
        cont += 1    
    
    return pos_punto 

def sum(num1, num2):
    """
    sum(num1,num2)
    -----------------------------------
    num1: primero numero en formato ieee754 precision simple (32 bits) a sumar
    num2: segundo numero en formato ieee754 precision simple (32 bits) a sumar
    -----------------------------------
    Se encarga de sumar ambos numeros siguiendo los siguientes pasos:
        1. Revisar exponente mayor para igualar exponentes
        2. De acuerdo a lo obtenido en el paso anterior se "shiftea" al exponente de la mayor y se le suma 1 a ambas mantissas
        3. Se realiza la suma binaria 
        4. Se normaliza el resultado
        5. Se chequea el exponente del resultado
        6. De ser necesario se rellena la mantissa y se ajusta a 32 bits
        7. Se retorna el el numero transformado

    """
    
    m1= num1[9:]
    m2= num2[9:]
    e1= num1[1:9]
    e2= num2[1:9]
    sig1= num1[:1]
    
    #revision de exponentes
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
    
    #se encuentra la mayor mantissa en funcion del ultimo uno de cada mantissa
    max_mantisa = max(len(cortar_mantisa(m1)),len(cortar_mantisa(m2)))
    
    m1 = cortar_mantisa(m1) +"0"*(-len(cortar_mantisa(m1))+max_mantisa)
    m2 = cortar_mantisa(m2) +"0"*(-len(cortar_mantisa(m2))+max_mantisa)

    #suma binaria    
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

    #normalizacion resultado
    pos_punto = buscar_punto(result) # nos retorna la pos del punto 1 o 2,
    result = result[0] + "." + result[1:pos_punto] + result[pos_punto+1:] 
    
    #chequeo exponente resultante de la suma
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

    #se ajusta la mantissa y se expresa el numero transformado
    mantissa = result[2:]
    while len(mantissa) < 23:
        mantissa += "0"
    final = sig1 + e + mantissa

    return final[:32] 

def buscar_uno(num):
    """
    buscar_uno(num)
    ------------------
    num: numero binario (con parte entera 0)
    ------------------
    Funcion que retorna la posicion del primer uno que encuentra restandole 2, y retorna 0 en caso de no encontrar ninguno.
    Esta funcion ayuda a encontrar el valor del exponente en numeros que tienen exponente menor a 127.  
    """
    cont=0
    for i in num:
        if (i == "0" or i =="."):
            cont+=1
        else:
            return cont - 2
    return 0

def binario_a_ieee754(numero):
    """
    binario_a_ieee754(numero):
    ------------------------------
    numero: numero binario
    ------------------------------
    funcion que transforma un numero binario a su forma ieee754 precision simple (32 bits) y lo retorna.
    """
    cont = 0
    aux = numero[0]
    if aux == "-" and numero[1] == "0":
        aux = "0"

    if float(numero) > 0:
        signo = "0"
    else:
        signo = "1"
        numero = numero[1:]
      
    pos_punto = buscar_punto(numero)
    if pos_punto == 0: #cuando no hay punto
        pos_punto = len(numero)
    e = pos_punto - 1

    if aux == "0": #busca el primer 1
        cont= buscar_uno(numero)
        e = -cont-1
    nuevo_numero = numero[0] + "." + numero[1:pos_punto] + numero[pos_punto+1:]
    
    if(e<0):
        mantissa= nuevo_numero[-e+2:]
    else:
        mantissa = nuevo_numero[2:]

    while len(mantissa) < 23:
        mantissa += "0"
    
    exponente = e + 127
    exponente = str(decimal_a_binario(exponente))
    

    if binario_int(exponente)>127:
        while len(exponente)< 8:
            exponente+="0"
    else:
        while len(exponente)<8:
            exponente= "0"+ exponente

    numero_ieee754 = signo + exponente + mantissa
    

    if (len(numero_ieee754)>32):
        numero_ieee754= numero_ieee754[:32]
    return numero_ieee754
        
def decimal_a_binario(numero):
    """
    decimal_a_binario(numero)
    ---------------------------------
    numero: numero en base 10 o decimal
    ---------------------------------
    Funcion que transforma un numero en base 10 a formato binario  y lo retorna
    """
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
        
        if aux != 0:
            n = 0
        else:
            n = 10
        
        #el while para numeros mayores a 1 tiene 23 operaciones, esto con el objetivo de estar a la par con la
        #proxima mantissa, en caso de que el numero sea mayor a 0 y menor a uno realizara 10 iteraciones extra
        while cont_digitos < 23 + n and parte_decimal != 0:
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
    """
    binario_int(num)
    ---------------------------------
    num: numero binario
    ---------------------------------
    Funcion que transforma un numero binario a su forma decimal y lo retorna
    """
    decimal = 0
    largo = len(num)
    for i, digito in enumerate(num):
        if digito=="1":
            exponente = largo- i - 1
            decimal += 2 ** exponente
    return decimal

def ieee754_a_decimal(numero):
    """
    ieee754_a_decimal(num)
    ---------------------------------
    numero: numero en formato ieee754 precision simple (32 bits)
    ---------------------------------
    Funcion que transforma un numero en formato ieee754 precision simple (32 bits) a su forma decimal
    """
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
count = 0

#se lee el archivo operaciones.txt y se realiza la transformacion o suma segun corresponda
with open('operaciones.txt','r') as archivo:

    for linea in archivo:
        linea = linea.strip().split(";")
        if(len(linea)>=2):
            temp1 = (linea[0])
            temp2 = (linea[1])
            if (float(temp1) == 0.0 and float(temp2)== 0.0):
                string_salida = "0.0/" + "0"*32
                lista_escribir.append(string_salida)
                fallas += 1

            elif(float(temp1) == 0.0):
                
                temp2=float(temp2)
                num2=decimal_a_binario(temp2)
                num2=binario_a_ieee754(num2)
                count += 1
                string_salida = str(round(ieee754_a_decimal(num2),3)) + "/" + num2
                lista_escribir.append(string_salida)
            
            elif(float(temp2) == 0.0):

                temp1=float(temp1)
                num1=decimal_a_binario(temp1)
                num1=binario_a_ieee754(num1)
                count += 1
                string_salida = str(round(ieee754_a_decimal(num1),3)) + "/" + num1
                lista_escribir.append(string_salida)


            elif(temp1!="" and temp2!= ""):

                temp1 = float(linea[0])
                temp2 = float(linea[1])
                num1 = decimal_a_binario(temp1)
                num2 = decimal_a_binario(temp2)
                num1 = binario_a_ieee754(num1)
                num2 = binario_a_ieee754(num2)

                if ((temp1 >= 0) and (temp2 >= 0)) or (((temp1 <= 0) and (temp2 <= 0))):

                    resultado = sum(num1,num2)
                    count += 1
                    string_salida = str(round(ieee754_a_decimal(resultado),3)) + "/" + resultado
                    lista_escribir.append(string_salida)
                                
                else:

                    fallas+=1
                    string_salida= str(round(temp1,3)) + "/" + num1 + ";" + str(round(temp2,3)) + "/" + num2 
                    lista_escribir.append(string_salida)
            else:
                fallas+=1

#se escribe en el archivo resultados.txt
with open('resultados.txt','w') as archivo:
   for i in lista_escribir:
       archivo.write(i+"\n")

#se muestra lo pedido por consola
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


