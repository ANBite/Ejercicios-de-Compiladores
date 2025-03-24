#traducir if, for, while, repeat a ensamblador
#luego que ejecute

#TRADUCIR IF y ELSE a ensamblador
import re
tokens_patron = {
    "KEYWORD": r"\b(if|else|while|return|int|float|void)\b",
    "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    "NUMBER": r"\b\d+(\.\d+)?\b",
    "OPERATOR": r"[+\-*/]",
    "DELIMITER": r"[(),;{}]",
    "WHITESPACE": r"\s+"
}

class NodoAST():
    #Clase base para todos los nodos del AST


    #Traducir de lenguaje C a python 17/03/2025
        #ubut suma(int a, intb) {
        #   int c = a + b;
        #   return c
        #}

        #def suma(a,b):
        #c = a + b
        #return c

    def traducir(self):
        raise NotImplementedError("Método traducir() No implementado en este nodo.")
    
    def generar_codigo(self):
        raise NotImplementedError("Método generar_codigo() No implementado en este nodo.")


class NodoFuncion(NodoAST):
    #Nodo que representa una funcion
    def __init__(self, nombre, parametro, cuerpo):
        super().__init__()
        self.nombre = nombre
        self.parametro = parametro
        self.cuerpo = cuerpo
    
    def traducir(self):
        params = ",".join(p.traducir() for p in self.parametro)
        cuerpo = "\n    ".join(c.traducir() for c in self.cuerpo)
        return f"def {self.nombre[1]} ({params}):\n     {cuerpo}"  #Identificador en self.nombre[0]   



class NodoParametro(NodoAST):
    #Nodo que representa un parámetro de función
    def __init__(self, tipo, nombre):
        super().__init__()
        self.tipo = tipo
        self.nombre = nombre

    def traducir(self):
       return self.nombre[1]


class NodoAsignacion(NodoAST):
    #Nodo que representa una asignación de variable
    def __init__(self, nombre, expresion):
        super().__init__()
        self.nombre = nombre
        self.expresion = expresion #Que se está asignando la variable

    def traducir(self):
       return f"{self.nombre[1]} = {self.expresion.traducir()}"
    
    def generar_codigo(self):
       codigo = self.expresion.generar_codigo()
       codigo += f"\n    mov  [{self.nombre[1]}], eax; guardar resultado en {self.nombre[1]}"
       return codigo


class NodoOperacion(NodoAST):
    #Nodo que representa una operación aritmética
    def __init__(self, izquierda, operador, derecha):
        super().__init__()
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

    def traducir(self):
       return f"{self.izquierda.traducir()} {self.operador[1]} {self.derecha.traducir()}"
    
    def generar_codigo(self):
       codigo = []
       codigo.append(self.izquierda.generar_codigo()) #Cargar el operador izquierdo
       codigo.append("    push eax ; guardar en la pila") #Guardar el operando izquierdo en la pila
       
       codigo.append(self.derecha.generar_codigo()) #Cargar el operador derecho
       codigo.append("    pop ebx; recuperar el primer operando") 
       #ebx = operando 1 y eax = operando 2

       if self.operador()[1] == "+":
          codigo.append("    add eax, ebx ;eax + ebx")
       elif self.operador[1] == "-":
          codigo.append("    sub ebx, eax; ebx - eax")
          codigo.append("    mov eax, ebx")
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
       return f"return {self.expresion.traducir()}"
    

    def generar_codigo(self):
       return self.expresion.generar_codigo() + "\n    ret ; retorno desde la subrutina"
       
    


class NodoIdentificador(NodoAST):
    #Nodo que representa a un identificador
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
    
    def traducir(self):
       return self.nombre[1]
    
    def generar_codigo(self):
       return f"    mov eax, {self.nombre[1]} ;cargar variable {self.nombre[1]} en eax" #IDENTIFICADOR [0] ; VALOR [1]
    


class NodoNumero(NodoAST):
    #Nodo que representa un número
    def __init__(self, valor):
        super().__init__()
        self.valor = valor
    
    def traducir(self):
       return str(self.valor[1])
    

    def generar_codigo(self):
       return f"    mov eax, {self.valor[1]} ;cargar número {self.valor[1]} en eax" #NUMBER [0] ; VALOR [1]
    
    """
    ARQUITECTURA DE REGISTRO
    rax = 64
    -------------------------------
    ! 32 bits   | eax = 32        |
    |           | 16b     |       |
    """

    class NodoIf(NodoAST):
    def __init__(self, condicion, cuerpo, else_cuerpo=None):
        super().__init__()
        self.condicion = condicion  # Expresión condicional
        self.cuerpo = cuerpo  # Instrucciones dentro del if
        self.else_cuerpo = else_cuerpo  # Instrucciones dentro del else (opcional)

    def traducir(self):
        else_part = f"\nelse:\n    {self.else_cuerpo.traducir()}" if self.else_cuerpo else ""
        return f"if {self.condicion.traducir()}:\n    {self.cuerpo.traducir()}{else_part}"

    def generar_codigo(self):
        codigo = self.condicion.generar_codigo()  # Código de la condición
        codigo += "\n    CMP AX, 0 ; Comparar resultado con 0"  # Verificar si es falso
        codigo += "\n    JE ELSE ; Saltar a ELSE si es falso"
        
        # Código dentro del bloque if
        for instruccion in self.cuerpo:
            codigo += f"\n{instruccion.generar_codigo()}"

        if self.else_cuerpo:
            codigo += "\n    JMP END_IF ; Saltar fuera del if"
            codigo += "\nELSE:"
            for instruccion in self.else_cuerpo:
                codigo += f"\n{instruccion.generar_codigo()}"

        codigo += "\nEND_IF:"
        return codigo


#----------------------------------------------------------------------------------- ANALIZADOR ----------------------
class Parcer:
  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0
  
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

      #Verificar si existe la función main
      nombres_funciones = [f.nombre[1] if isinstance(f.nombre, tuple) else f.nombre for f in funciones]
      if "main" not in nombres_funciones:
          raise SyntaxError("Error: No se encontró la función 'main'. El programa no puede continuar.")
      return funciones  # Devuelve todas las funciones


  def funcion(self):
    #La gramática para una función: int IDENTIFIER (int, IDENTIFIER) {CUERPO}
    tipo_return = self.coincidir("KEYWORD") #Tipo de retorno (ej. int)
    nombre_funcion = self.coincidir("IDENTIFIER") #Nombre de la funcion
    self.coincidir("DELIMITER") #Se espera un (
    parametros = self.parametros() 
    self.coincidir("DELIMITER") #Se espera un )
    self.coincidir("DELIMITER") #Se espera un {
    cuerpo = self.cuerpo()
    self.coincidir("DELIMITER") #Se espera un }
    return NodoFuncion(nombre_funcion, parametros, cuerpo)

  def parametros(self):
    parametros = []
    #Reglas para parámetros: [PALABRA RESERVADA, IDENTIFIER, coma, PALABRA RESERVADA, IDENTIFICADOR]
    tipo = self.coincidir("KEYWORD") #Tipo / Palabra reservada del parámetro
    nombre = self.coincidir("IDENTIFIER") #Nombre del parámetro
    parametros.append((tipo, nombre)) #Se crea nodo
    while self.obtener_token_actual() and self.obtener_token_actual()[1] == ",":
      self.coincidir("DELIMITER") #sE ESPERA UNA ,
      tipo = self.coincidir("KEYWORD") #tipo / Palabra reservada de parámetro
      nombre = self.coincidir("IDENTIFIER") #Nombre del parámetro
      parametros.append((tipo, nombre)) #Se crea nodo
    return parametros
  
  def cuerpo(self):
    #Gramática para el cuerpo: return IDENTIFIER, OPERATOR IDENTIFIER
    instrucciones = []
    while self.obtener_token_actual() and self.obtener_token_actual()[1] != "}": #VERIFICA SI HAY TOKEN DE CIERRE 
        if self.obtener_token_actual()[1] == "return": #Verifica el contenido del token y mira si es igual a return
           instrucciones.append(self.retorno()) #Se agrega a la lista un nodo llamado retorno
        else:
           instrucciones.append(self.asignacion())
    return instrucciones
  
  def asignacion(self):
    tipo = self.coincidir("KEYWORD") #Se espera un return
    nombre = self.coincidir("IDENTIFIER") #Se espera un Identificador <Nombre de la variable>
    self.coincidir("OPERATOR") #Se espera un Operador <ej. Suma>
    expresion = self.expresion()
    self.coincidir("DELIMITER") #Se espera un ;
    return NodoAsignacion([tipo, nombre], expresion)
  
  def retorno(self):
     self.coincidir("KEYWORD")
     expresion = self.expresion()
     self.coincidir("DELIMITER")
     retorno = NodoRetorno(expresion)
     return retorno
  
  def expresion(self):
     izquierda = self.termino()
     while self.obtener_token_actual() and self.obtener_token_actual()[1] == "OPERATOR":
        operador = self.coincidir("OPERATOR")
        derecha = self.termino()
        izquierda = NodoOperacion(izquierda, operador, derecha)
     return izquierda
  
  def termino(self):
     token = self.obtener_token_actual()
     if token[0] == "NUMBER":
        return NodoNumero(self.coincidir("NUMBER"))
     elif token[0] == "IDENTIFIER":
        return NodoIdentificador(self.coincidir("IDENTIFIER"))
     else:
        raise SyntaxError(f"Expresion no valida: {token}")

#=== EJEMPLO DE USO [ en proceso ] ===

import json

# === Código fuente válido ===
codigo_fuente = """
if suma(int a, int b) { 
  int a + b;
  return c;
}

int main(int a, int b) { 
  int a + b;
  return a; 
  }

int resta(int a, int b) { 
  int a - b;
  return c;
}
"""

codigo_2 = """"
int resta(int a, int b) { 
  int a - b;
  return c;
}"""

def identificar_token(texto):
    patron_general = "|".join(f"(?P<{token}>{patron})" for token, patron in tokens_patron.items())
    patron_regex = re.compile(patron_general)
    tokens_encontrados = []
    for found in patron_regex.finditer(texto):
        for token, valor in found.groupdict().items():
            if valor is not None and token != "WHITESPACE":
                tokens_encontrados.append((token, valor))
    return tokens_encontrados

tokens_globales = identificar_token(codigo_2)
print("Tokens encontrados:")
for tipo, valor in tokens_globales:
    print(f"{tipo} : {valor}")


# === Tokenización ===


def tokenizar(codigo):
    tokens = []
    patron = "|".join(f"(?P<{tipo}>{expresion})" for tipo, expresion in tokens_patron.items())
    for coincidencia in re.finditer(patron, codigo):
        tipo = coincidencia.lastgroup
        valor = coincidencia.group(tipo)
        if tipo != "WHITESPACE":
            tokens.append((tipo, valor))
    return tokens

# === Creación del AST ===
parser = Parcer(tokenizar(codigo_fuente))
ast = parser.parcear()

# === Conversión del AST a JSON ===

def nodo_a_diccionario(nodo):
    if isinstance(nodo, NodoFuncion):
        return {
            "tipo": "Funcion",
            "nombre": nodo.nombre[1],  # Corregido el acceso a nombre
            "parametros": [{"tipo": p[0][1], "nombre": p[1][1]} for p in nodo.parametro],  # Convertir tuplas a JSON
            "cuerpo": [nodo_a_diccionario(inst) for inst in nodo.cuerpo]  # Convertir cada instrucción
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

ast_json = json.dumps(nodo_a_diccionario(ast), indent=4)
print("=== Analisis sintactico completo sin errores ===")
print(ast_json)


print("----- Expresion optimizada ----")
nodo_expresion = NodoOperacion(NodoNumero(5), "+", NodoNumero(8))
print(json.dumps(nodo_a_diccionario(nodo_expresion), indent=1))
expresion_optimizada = nodo_expresion.optimizar()
print("-------------------------------------------------------------------------------------------------------------------------")
print(codigo_fuente)
print("Código traducido")
codigo_ensamblador = ast_json.generarcodigo()
print(codigo_ensamblador)
