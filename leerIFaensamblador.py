import re
tokens_patron = {
    "KEYWORD": r"\b(if|else|elif|while|return|int|float|void)\b",
    "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    "NUMBER": r"\b\d+(\.\d+)?\b",
    "OPERATOR": r"[+\-*/]",
    "DELIMITER": r"[(),;{}]",
    "WHITESPACE": r"\s+",
    "EQUAL" : r"=",
    "CONDITION" : r"==|<|>|<=|>=|!="
    
}

class NodoAST():
    def traducir(self):
        raise NotImplementedError("Metodo traducir() No implementado en este nodo.")
    
    def generar_codigo(self):
        raise NotImplementedError("Metodo generar_codigo() No implementado en este nodo.")

class NodoFuncion(NodoAST):
    #Nodo que representa una funcion
    def __init__(self, nombre, parametro, cuerpo):
        super().__init__()
        self.nombre = nombre
        self.parametro = parametro
        self.cuerpo = cuerpo
    
    def traducir(self):
        if self.nombre[0][1] == "INT".lower():
            params = ",".join(NodoParametro(p[0], p[1]).traducir() for p in self.parametro)

            cuerpo = []
            for c in self.cuerpo:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoAsignacion):
                    cuerpo.append(c.traducir())
                elif isinstance(c, NodoRetorno):
                    cuerpo.append(c.traducir())

            return f"def {self.nombre[1][1]} ({params}):\n     {cuerpo[0]}\n     return {cuerpo[1]}"  #Identificador en self.nombre[0] 
        
        elif self.nombre[0][1] == "IF".lower():
            cuerpo = []
            for c in self.parametro:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoAsignacion):
                    cuerpo.append(c.traducir())
                elif isinstance(c, NodoRetorno):
                    cuerpo.append(c.traducir())

            #ejecucion = self.ejecutar("if", cuerpo[0], cuerpo[1])
            #salto = "\n==================================== Ejecucion del Codigo ==========================================="
            return f"{self.nombre[0][1]} {cuerpo[0]}:\n     return {cuerpo[1]}" #\n{salto}\n\n{ejecucion} 
    
        elif self.nombre[0][1] == "ELIF".lower():
            cuerpo = []
            for c in self.parametro:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoAsignacion):
                    cuerpo.append(c.traducir())
                elif isinstance(c, NodoRetorno):
                    cuerpo.append(c.traducir())

            return f"{self.nombre[0][1]} {cuerpo[0]}:\n     return {cuerpo[1]}" 
        
        elif self.nombre[0][1] == "ELSE".lower():
            cuerpo = []
            for c in self.cuerpo:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoRetorno):
                    cuerpo.append(c.traducir())

            return f"{self.nombre[0][1]}:\n     return {cuerpo[0]}" 
            
        

    def ejecutar(self, tipo, cuerpo1, cuerpo2):
        super().__init__()
        self.tipo = tipo
        self.cuerpo1 = cuerpo1
        self.cuerpo2 = cuerpo2
        if self.tipo == "IF".lower():
            if self.cuerpo1[2] == "=" and self.cuerpo1[3] == "=":
                if self.cuerpo1[0] == self.cuerpo1[5]:
                    return f"{self.cuerpo2}"
                else:
                    return f"{self.cuerpo2}"
    
    
    def generar_codigo(self):
        if self.nombre[0][1] == "INT".lower():
            cuerpo = []
            for c in self.cuerpo:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoAsignacion):
                    cuerpo.append(c.generar_codigo())
                elif isinstance(c, NodoRetorno):
                    cuerpo.append(c.generar_codigo())

            return f"{self.nombre[1][1]} PROC \n{cuerpo[0]}\n{cuerpo[1]}    \n{self.nombre[1][1]} ENDP"  
        
        if self.nombre[0][1] == "IF".lower():
            cuerpo = []
            for c in self.parametro:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoAsignacion):
                    cuerpo.append(c.generar_codigo())
                elif isinstance(c, NodoRetorno):
                    cuerpo.append(c.generar_codigo())

            return f"{self.nombre[1][1]} PROC \n{cuerpo[0]}\n{cuerpo[1]}    \n{self.nombre[1][1]} ENDP"

        if self.nombre[0][1] == "ELIF".lower():
            cuerpo = []
            for c in self.parametro:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoAsignacion):
                    cuerpo.append(c.generar_codigo())
                elif isinstance(c, NodoRetorno):
                    cuerpo.append(c.generar_codigo())

            return f"{self.nombre[1][1]} PROC \n{cuerpo[0]}\n{cuerpo[1]}    \n{self.nombre[1][1]} ENDP"
        if self.nombre[0][1] == "ELSE".lower():
            cuerpo = []
            for c in self.cuerpo:
                #Al inicio es un nodo asignacion y un nodo retorno, luego el nodo asignacion se divide en asignacion y operacion
                if isinstance(c, NodoRetorno):
                    cuerpo.append(c.generar_codigo())

            return f"{self.nombre[1][1]} PROC \n{cuerpo[0]}\n{self.nombre[1][1]} ENDP"


        


class NodoParametro(NodoAST):
    #Nodo que representa un parámetro de función
    def __init__(self, tipo, nombre):
        super().__init__()
        self.tipo = tipo
        self.nombre = nombre

    def traducir(self):
       return self.nombre[1]
    
    def generar_codigo(self):
       return self.nombre[1]


class NodoAsignacion(NodoAST):
    #Nodo que representa una asignación de variable
    def __init__(self, nombre, expresion):
        super().__init__()
        self.nombre = nombre
        self.expresion = expresion #Que se está asignando la variable

    def traducir(self):
        if self.nombre[1] == "IF".lower():
            if isinstance(self.expresion, NodoOperacion):
                return f"{self.expresion.traducir()}"
        
        elif self.nombre[0][1] == "INT".lower():
            if isinstance(self.expresion, NodoOperacion):
                return f"{self.nombre[1][1]} = {self.expresion.traducir()}"
    
    def generar_codigo(self):
        if self.nombre[0][1] == "INT".lower():
            if isinstance(self.expresion, NodoOperacion):
                codigo = self.expresion.generar_codigo()
                codigo += f"\n    mov  [{self.nombre[1][1]}], eax; guardar resultado en {self.nombre[1][1]}"
                return codigo
        elif self.nombre[1] == "IF".lower():
            if isinstance(self.expresion, NodoOperacion):
                codigo = self.expresion.generar_codigo()
                codigo += f"\n    mov  resultado, eax;    si son iguales, guardar eax en resultado"
                return codigo


class NodoOperacion(NodoAST):
    #Nodo que representa una operación aritmética
    def __init__(self, izquierda, operador, derecha):
        super().__init__()
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

    def traducir(self):

        if self.operador[0] == "EQUAL" or self.operador[0] == "CONDITION":
            if self.operador[0] == "EQUAL":
                if isinstance(self.izquierda, NodoNumero) and isinstance(self.derecha, NodoNumero):
                    return f"{self.izquierda.traducir()} {str(self.operador[1]) + str(self.operador[1])} {self.derecha.traducir()}"
                elif isinstance(self.izquierda, NodoIdentificador) and isinstance(self.derecha, NodoIdentificador):
                    return f"{self.izquierda.traducir()} {str(self.operador[1]) + str(self.operador[1])} {self.derecha.traducir()}"
            elif self.operador[0] == "CONDITION":
                if isinstance(self.izquierda, NodoNumero) and isinstance(self.derecha, NodoNumero):
                    return f"{self.izquierda.traducir()} {self.operador[1]} {self.derecha.traducir()}"
                elif isinstance(self.izquierda, NodoIdentificador) and isinstance(self.derecha, NodoIdentificador):
                    return f"{self.izquierda.traducir()} {self.operador[1]} {self.derecha.traducir()}"
        
        elif self.operador[0] == "OPERATOR":  
            if isinstance(self.izquierda, NodoNumero) and isinstance(self.derecha, NodoNumero):
                return f"{self.izquierda.traducir()} {self.operador[1]} {self.derecha.traducir()}"
            elif isinstance(self.izquierda, NodoIdentificador) and isinstance(self.derecha, NodoIdentificador):
                return f"{self.izquierda.traducir()} {self.operador[1]} {self.derecha.traducir()}"
    

    def generar_codigo(self):
        codigo = []
        if isinstance(self.izquierda, NodoNumero) and isinstance(self.derecha, NodoNumero):
            codigo.append(self.izquierda.generar_codigo()) #Cargar el operador izquierdo
            codigo.append("    push eax ; guardar en la pila") #Guardar el operando izquierdo en la pila
            
            codigo.append(self.derecha.generar_codigo()) #Cargar el operador derecho
            codigo.append("    pop ebx; recuperar el primer operando") 
            #ebx = operando 1 y eax = operando 2
        elif isinstance(self.izquierda, NodoIdentificador) and isinstance(self.derecha, NodoIdentificador):
            codigo.append(self.izquierda.generar_codigo()) #Cargar el operador izquierdo
            codigo.append("    push eax ; guardar en la pila") #Guardar el operando izquierdo en la pila
            
            codigo.append(self.derecha.generar_codigo()) #Cargar el operador derecho
            codigo.append("    pop ebx; recuperar el primer operando") 

        if self.operador[1] == "+":
            codigo.append("    add eax, ebx ;eax + ebx")
        elif self.operador[1] == "-":
            codigo.append("    sub ebx, eax; ebx - eax")
            codigo.append("    mov eax, ebx")
        elif self.operador[1] == "=":
            codigo.append("    CMP eax, ebx    ;Compara EAX con EBX")
        elif self.operador[0] == "CONDITION":
            codigo.append("    CMP eax, ebx    ;Compara EAX con EBX")

        return "\n".join(codigo)
          
    #Crear un método que optimice la operación
    def optimizar(self):
       if isinstance(self.izquierda, NodoOperacion):
        izquierda = self.izquierda.optimizar()
       else:
          izquierda = self.izquierda
       if isinstance(self.derecha, NodoOperacion):
        derecha = self.derecha.optimizar()
       else:
          derecha = self.derecha

       #Si ambos operandos son numeros, ecaluamos la operación
       if isinstance(izquierda, NodoNumero) and isinstance(derecha, NodoNumero): #Verifica si derecha e izquierda son números
          if self.operador == "+":
             return NodoNumero(izquierda.valor + derecha.valor)
          elif self.operador == "-":
             return NodoNumero(izquierda.valor - derecha.valor)
          elif self.operador == "*":
             return NodoNumero(izquierda.valor * derecha.valor)
          elif self.operador == "/" and derecha.valor != 0:
             return NodoNumero(izquierda.valor / derecha.valor)
          

        #Simplificación algebraica
       if self.operador == "*" and isinstance(derecha, NodoNumero) and derecha.valor == 1:
          return izquierda
       if self.operador == "*" and isinstance(izquierda, NodoNumero) and izquierda.valor == 1:
          return derecha
       if self.operador == "+" and isinstance(derecha, NodoNumero) and derecha.valor == 0:
          return izquierda
       if self.operador == "+" and isinstance(izquierda, NodoNumero) and izquierda.valor == 0:
          return derecha
       
       #Agregar más como 0 / n, 0 * n, n / 0, entre otros

       #Si no se puede optimizar más, devolvemos la misma operación
       return NodoOperacion(izquierda, self.operador, derecha)
                    


class NodoRetorno(NodoAST):
    #Nodo que representa a la sentencia o instrucción RETURN
    def __init__(self, expresion):
        super().__init__()
        self.expresion = expresion

    def traducir(self):
       if isinstance(self.expresion, NodoIdentificador):
            return f"{self.expresion.traducir()}"
    

    def generar_codigo(self):
       if isinstance(self.expresion, NodoIdentificador):
            return self.expresion.generar_codigo() + "\n    ret ; retorno desde la subrutina"
       
    
class NodoIdentificador(NodoAST):
    #Nodo que representa a un identificador
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
    
    def traducir(self):
       return self.nombre[1]
    
    def generar_codigo(self):
       return f"    mov eax, {self.nombre[1]} ;   cargar variable {self.nombre[1]} en eax"
    


class NodoNumero(NodoAST):
    #Nodo que representa un número
    def __init__(self, valor):
        super().__init__()
        self.valor = valor
    
    def traducir(self):
       return str(self.valor[1])
    

    def generar_codigo(self):
       return f"    mov eax, {self.valor[1]} ;   cargar número {self.valor[1]} en eax"

# ================================== Analizador sintáctico ===================================================
class Parcer:
  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0
    self.texto_a_imprimir_traducido_a_lenguaje_python = ""
    self.texto_a_imprimir_traducido_a_lenguaje_ensamblador = ""
  
  def obtener_token_actual(self):
    return self.tokens[self.pos] if self.pos < len(self.tokens) else None #Envía el token actual si está dentro del rango del tamaño
  
  def coincidir(self, tipo_esperado):
    token_actual = self.obtener_token_actual() #Obtiene el token actual
    if token_actual and token_actual[0] == tipo_esperado: #Si el token actual [su valor y token] es igual al tipo esperado
      self.pos += 1 #Aumenta la posición
      return token_actual #Devuelve el token actual
    else:
      raise SyntaxError(f"Error sintactico, se esperaba {tipo_esperado}, pero se encontro: {token_actual}")
  
  def parcear(self):
      funciones = []
      while self.obtener_token_actual():
          funciones.append(self.funcion())
      return funciones

      #Verificar si existe la función main
      #nombres_funciones = [f.nombre[1] if isinstance(f.nombre, tuple) else f.nombre for f in funciones]
      #if "main" not in nombres_funciones:
      #    raise SyntaxError("Error: No se encontró la función 'main'. El programa no puede continuar.")
      #return funciones  # Devuelve todas las funciones


  def funcion(self):
    #La gramática para una función: int IDENTIFIER (int, IDENTIFIER) {CUERPO}7
    tipo = self.coincidir("KEYWORD") #Se espera un KEYWORD cualquiera
    if tipo[1] == "INT".lower():
        nombre_funcion = self.coincidir("IDENTIFIER") #Nombre de la funcion
        self.coincidir("DELIMITER") #Se espera un (
        parametros = self.parametros() 
        self.coincidir("DELIMITER") #Se espera un )
        self.coincidir("DELIMITER") #Se espera un {
        cuerpo = self.cuerpo()
        self.coincidir("DELIMITER") #Se espera un }

        self.texto_a_imprimir_traducido_a_lenguaje_python = NodoFuncion([tipo, nombre_funcion], parametros, cuerpo).traducir()
        self.texto_a_imprimir_traducido_a_lenguaje_ensamblador = NodoFuncion([tipo, nombre_funcion], parametros, cuerpo).generar_codigo()

        return NodoFuncion([tipo, nombre_funcion], parametros, cuerpo)

    elif tipo[1] == "IF".lower():
        self.coincidir("DELIMITER") #Se espera un (
        parametros = self.cuerpo()
        self.coincidir("DELIMITER") #Se espera un }
        cuerpo = parametros[1]
        
        self.texto_a_imprimir_traducido_a_lenguaje_python += NodoFuncion([tipo, tipo], parametros, cuerpo).traducir()
        self.texto_a_imprimir_traducido_a_lenguaje_ensamblador += NodoFuncion([tipo, tipo], parametros, cuerpo).generar_codigo()

        return NodoFuncion([tipo, tipo], parametros, cuerpo)
    
    elif tipo[1] == "ELIF".lower():
        self.coincidir("DELIMITER") #Se espera un (
        parametros = self.cuerpo()
        self.coincidir("DELIMITER") #Se espera un }
        cuerpo = parametros[1]

        self.texto_a_imprimir_traducido_a_lenguaje_python += f"\n{NodoFuncion([tipo, tipo], parametros, cuerpo).traducir()}"
        self.texto_a_imprimir_traducido_a_lenguaje_ensamblador += f"\n{NodoFuncion([tipo, tipo], parametros, cuerpo).generar_codigo()}"

        return NodoFuncion([tipo, tipo], parametros, cuerpo)

    elif tipo[1] == "ELSE".lower():
        self.coincidir("DELIMITER") #Se espera un {
        cuerpo = self.cuerpo()
        self.coincidir("DELIMITER") #Se espera un }                            

        n = ""                        
        self.texto_a_imprimir_traducido_a_lenguaje_python += f"\n{NodoFuncion([tipo, tipo], n, cuerpo).traducir()}"
        self.texto_a_imprimir_traducido_a_lenguaje_ensamblador += f"\n{NodoFuncion([tipo, tipo], n, cuerpo).generar_codigo()}"

        return NodoFuncion([tipo, tipo], n, cuerpo)
    
    else:

        raise SyntaxError(f"Error sintactico {tipo} no es un KEYWORD valido")

  def parametros(self):
    parametros = []
    #Reglas para parámetros: [PALABRA RESERVADA, IDENTIFER, coma, PALABRA RESERVADA, IDENTIFER]

    tipo = self.coincidir("KEYWORD") #Tipo / Palabra reservada del parametro [puede ser int]
    nombre = self.coincidir("IDENTIFIER") #Nombre del parámetro [puede ser a o un número]
    parametros.append((tipo, nombre)) #Se crea nodo
    while self.obtener_token_actual() and self.obtener_token_actual()[1] == ",":
      self.coincidir("DELIMITER") #SE ESPERA UNA ,
      tipo = self.coincidir("KEYWORD") #tipo / Palabra reservada de parámetro
      nombre = self.coincidir("IDENTIFIER") #Nombre del parámetro
      parametros.append((tipo, nombre)) #Se crea nodo

    while self.obtener_token_actual() and self.obtener_token_actual()[1] == "=":
        igual1 = self.coincidir("EQUAL") #Se espera un =
        #Si es una comparación: (==)
        igual2 = self.coincidir("EQUAL") #Se espera un =
        tipo = self.coincidir("KEYWORD") #Se espera un tipo / palabra reservada de parámetro
        nombre = self.coincidir("IDENTIFIER") #se espera el nombre del parámetro
        parametros.append(([str(igual1)+str(igual2),tipo], nombre))

    return parametros
  
  def cuerpo(self):
    #Gramática para el cuerpo: RETURN
    instrucciones = []
    while self.obtener_token_actual() and self.obtener_token_actual()[1] != "}": #VERIFICA SI HAY TOKEN DE CIERRE
        if self.obtener_token_actual()[1] == "return": #Verifica el contenido del token y mira si es igual a return
           instrucciones.append(self.retorno()) #Se agrega a la lista un nodo llamado retorno
        else:
            instrucciones.append(self.asignacion())

    return instrucciones
  
  def asignacion(self):
    if self.obtener_token_actual()[0] == "KEYWORD":
        tipo = self.coincidir("KEYWORD") #Se espera un int 
        nombre = self.coincidir("IDENTIFIER") #Se espera un Identificador como el <Nombre de la variable>
        self.coincidir("EQUAL") #Espera un signo =
        expresion = self.expresion()
        self.coincidir("DELIMITER") #Se espera un ;
        return NodoAsignacion([tipo, nombre], expresion)
    
    elif self.obtener_token_actual()[0] == "IDENTIFIER":
        expresion = self.expresion()
        self.coincidir("DELIMITER") #Se espera un )
        self.coincidir("DELIMITER") #Se espera un {}
        return NodoAsignacion(["keyword", "if"], expresion)
  
  def retorno(self):
     self.coincidir("KEYWORD")
     expresion = self.expresion()
     self.coincidir("DELIMITER")
     retorno = NodoRetorno(expresion)
     return retorno
  
  def expresion(self):
     izquierda = self.termino()

    #+ - * /

     while self.obtener_token_actual()[0] == "OPERATOR" or self.obtener_token_actual()[0] == "EQUAL":

        if self.obtener_token_actual()[0] == "OPERATOR":
            operador = self.coincidir("OPERATOR") #Se espera + - * /
            derecha = self.termino()
            izquierda = NodoOperacion(izquierda, operador, derecha)
            return izquierda
        
        elif self.obtener_token_actual()[0] == "EQUAL":
            operador = self.coincidir("EQUAL") #Se espera un =
            self.coincidir("EQUAL") #Se espera un =
            derecha = self.termino()
            izquierda = NodoOperacion(izquierda, operador, derecha) #----------------------------
            return izquierda
        elif self.obtener_token_actual()[0] == "CONDITION":
            operador = self.coincidir("CONDITION") #Se espera un < > !
            if self.obtener_token_actual()[0] == "COINDITION":
                self.coincidir("CONDITION") #Se espera un < > ! =
                derecha = self.termino()
                izquierda = NodoOperacion(izquierda, operador, derecha)

            else:
                pass

        
     return izquierda
  
  def termino(self):
     token = self.obtener_token_actual()
     if token[0] == "NUMBER":
        return NodoNumero(self.coincidir("NUMBER"))
     elif token[0] == "IDENTIFIER":
        return NodoIdentificador(self.coincidir("IDENTIFIER"))
     else:
        raise SyntaxError(f"Expresion no valida: {token}")
     
  def traducir_a_lenguaje_python(self):
        return self.texto_a_imprimir_traducido_a_lenguaje_python
  
  def traducir_a_lenguaje_ensamblador(self):
        return self.texto_a_imprimir_traducido_a_lenguaje_ensamblador
        #pass
  
  def ejecutar_codigo(self):
        pass


# --------------------------- Analisis Semantico -------------------------------------
class AnalizadorSemantico():
    def __init__(self):
        #Resive la tabla de simbolos
        self.tabla_simbolos = []
        
    def analizar(self, nodo):
        metodo = f"visitar_{type(nodo).__name__}" #__Se utilizan para declarar metodos o atributos que son accesibles solo en la clase
        #python for everbody
        if hasattr(self, metodo)(nodo):

            return getattr(self, metodo)(nodo)
        
        else:

            raise Exception(f"No se ha implementado el analisis cemantico para {type(nodo).__name__}")
        

    def visitar_NodoFuncion(self, nodo):
        if nodo.nombre[1] in self.tabla_simbolos:
            raise Exception(f"ERROR semantico la funcion {nodo.nombre[1]} ya esta definida")
        else:
            self.tabla_simbolos(nodo.nombre[1]) = {f"tipo":nodo.parametros[0].tipo[1], "parametros":nodo.parametros}

        for param in nodo.parametros:
            self.tabla_simbolos[param.nombre[1]] = {"tipo":param.tipo[1]}
        
        for instruccion in nodo.cuerpo:
            self.analizarinstruccion()
        



#=== EJEMPLO DE USO [ en proceso ] ===

import json

# === Código fuente válido ===
codigo_fuente = """
int suma(int a, int b) {
    int c = a + b; 
    return c;
}
"""

codigo_if = """
if ( a == b ) {
    return primerretorno; 
} elif (a == b) {
    return segundoretorno;
} else {
    return tercerterotno;
}
"""

def identificar_token(texto):
    patron_general = "|".join(f"(?P<{token}>{patron})" for token, patron in tokens_patron.items())
    patron_regex = re.compile(patron_general)
    tokens_encontrados = []
    for found in patron_regex.finditer(texto):
        for token, valor in found.groupdict().items():
            if valor is not None and token != "WHITESPACE":
                tokens_encontrados.append((token, valor))
    return tokens_encontrados

#tokens_globales = identificar_token(codigo_fuente) #codigo con int
tokens_globales = identificar_token(codigo_if) #codigo con if
print("\n================================ Tokens encontrados: ====================================================== ")
for tipo, valor in tokens_globales:
    print(f"{tipo} : {valor}")


# === Creación del AST ===
parser = Parcer(tokens_globales)
ast = parser.parcear()
ast_traducido = parser.traducir_a_lenguaje_python()
ast_ensamblador = parser.traducir_a_lenguaje_ensamblador()
ast_ejecutado = parser.ejecutar_codigo()


# === Conversión del AST a JSON ===

def nodo_a_diccionario(nodo):
    if isinstance(nodo, NodoFuncion):
        print(nodo.nombre)
        if nodo.nombre[0][1] == "INT".lower():
            return {
                "tipo": "Funcion",
                "nombre": nodo.nombre[1][1],  # Corregido el acceso a nombre  
                "parametros": [{"tipo": p[0][1], "nombre": p[1][1]} for p in nodo.parametro],  # Convertir tuplas a JSON
                "cuerpo": [nodo_a_diccionario(inst) for inst in nodo.cuerpo]  # Convertir cada instrucción
            }
        elif nodo.nombre[0][1] == "IF".lower():
            return {
                "tipo" : "Funcion",
                "nombre" : nodo.nombre[1][1], #Imprime el nombre
                "parametros" : "int a | EQUAL == | int b", #Imprime la confición del if
                "cuerpo" : " l", #Imprime el resultado del if
            }
    elif isinstance(nodo, NodoParametro):
        return {
            "tipo": "Parametro",
            "tipo_dato": nodo.tipo[1],
            "nombre": nodo.nombre[1]
        }
    elif isinstance(nodo, NodoAsignacion):
        return {
            "tipo": "Asignacion",
            "tipo variable": nodo.nombre[1],  # Extrae el tipo (ej. "int")
            "nombre": nodo.nombre[1][1],  # Extrae el identificador (ej. "c")
            "expresion": nodo_a_diccionario(nodo.expresion)
        }
    elif isinstance(nodo, NodoOperacion):
        return {
            "tipo": "Operacion",
            "izquierda": nodo_a_diccionario(nodo.izquierda),
            "operador": nodo.operador[1] if isinstance(nodo.operador, tuple) else nodo.operador,  # Manejo de tupla o string
            "derecha": nodo_a_diccionario(nodo.derecha)
        }
    elif isinstance(nodo, NodoRetorno):
        return {
            "tipo": "Retorno",
            "expresion": nodo_a_diccionario(nodo.expresion)
        }
    elif isinstance(nodo, NodoIdentificador):
        return {
            "tipo": "Identificador",
            "nombre": nodo.nombre[1] if isinstance(nodo.nombre, tuple) else nodo.nombre  # Manejo seguro del nombre
        }
    elif isinstance(nodo, NodoNumero):
        return {
            "tipo": "Numero",
            "valor": nodo.valor[1] if isinstance(nodo.valor, tuple) else nodo.valor  # Manejo seguro del valor
        }
    elif isinstance(nodo, list):  # Si se pasa una lista de nodos
        return [nodo_a_diccionario(subnodo) for subnodo in nodo]
    return {"tipo": "Desconocido", "valor": str(nodo)}  # Muestra el contenido desconocido

#ast_json = json.dumps(nodo_a_diccionario(ast), indent=4)
print("\n================================ Analisis sintactico completo sin errores =============================================")
print("\n======================================== Arbol JSON =================================================")

#print(ast_json)
print("PROXIMAMENTE...")

print("==================== Traduccion a lenguaje python y ensamblador y su ejecucion ==============================")
print("==================================== Lenguaje C =======================================================")

#print(codigo_fuente) #imprime codigo int
print(codigo_if) #imprime codigo if

print("==================================== Lenguaje Python =======================================================\n")

codigo_python = ast_traducido
print(codigo_python)


print("\n==================================== Lenguaje Ensamblador =======================================================")

codigo_ensamblador = ast_ensamblador
print(codigo_ensamblador)


