#VARIABLES GLOBALES
count=0 #contador de operaciones suma

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

def float_to_binary(linea):
    pos = linea.index(";")
    Num1= linea[:pos]
    Num2= linea[pos+1:]
    Num2= Num2.replace("\n","")
    Num1= binary(float(Num1))
    Num2= binary(float(Num2))
    print(Num1 +"           " + Num2)
    return 


with open('operaciones.txt','r') as archivo:
    for linea in archivo:
        float_to_binary(linea)
        
