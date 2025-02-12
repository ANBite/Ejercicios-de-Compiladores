#ANALIZADOR:  3/02/25
import re
tokens_patron = {
    "KEYWORD": r"\b(if|else|while|return|int|float|void)\b",
    "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    "NUMBER": r"\b\d+(\.\d+)?\b",
    "OPERATOR": r"[+\-*/]",
    "DELIMITER": r"[(),;{}]",
    "WHITESPACE": r"\s+"
}

def identificar_token(texto):
    patron_general = "|".join(f"(?P<{token}>{patron})" for token, patron in tokens_patron.items())
    patron_regex = re.compile(patron_general)
    tokens_encontrados = []
    for found in patron_regex.finditer(texto):
        for token, valor in found.groupdict().items():
            if valor is not None and token != "WHITESPACE":
                tokens_encontrados.append((token, valor))
    return tokens_encontrados

#analisis lexico

codigo_fuente = """
int suma(int a, int b) { return a + b; }
"""
tokens_globales = identificar_token(codigo_fuente)
print("tokens encontrados: ")
for tipo, valor in tokens_globales:
    print(f"{tipo} : {valor}")

#Identificador sintáctico
class Parcer:
  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0
  
  def obtener_token_actual(self):
    return self.tokens[self.pos] if self.pos < len(self.tokens) else None
  
  def coincidir(self, tipo_esperado):
    token_actual = self.obtener_token_actual()
    if token_actual and token_actual[0] == tipo_esperado:
      self.pos += 1
      return token_actual
    else:
      raise SyntaxError(f"Error sintactico, se esperaba {tipo_esperado}, pero se encontro: {token_actual}")
  
  def parcear(self):
    #Punto de entrada: se espera una funcion
    resultado = self.funcion()
    return resultado

  def funcion(self):
    #La gramática para una función: int IDENTIFIER (int, IDENTIFIER) {CUERPO}
    self.coincidir("KEYWORD") #Tipo de retorno (ej. int)
    self.coincidir("IDENTIFIER") #Nombre de la funcion
    self.coincidir("DELIMITER") #Se espera un (
    self.parametros()
    self.coincidir("DELIMITER") #Se espera un )
    self.coincidir("DELIMITER") #Se espera un {
    self.cuerpo()
    self.coincidir("DELIMITER") #Se espera un }

  def parametros(self):
    #Reglas para parámetros: [int, IDENTIFIER, (, INT, IDENTIFIER)]
    self.coincidir("KEYWORD") #Tipo del parámetro
    self.coincidir("IDENTIFIER") #Nombre del parámetro
    while self.obtener_token_actual() and self.obtener_token_actual()[1] == ",":
      self.coincidir("DELIMITER") #sE ESPERA UNA ,
      self.coincidir("KEYWORD") #tipo de parámetro
      self.coincidir("IDENTIFIER") #Nombre del parámetro

  def cuerpo(self):
    #Gramática para el cuerpo: return IDENTIFIER, OPERATOR IDENTIFIER
    self.coincidir("KEYWORD") #Se espera un return
    self.coincidir("IDENTIFIER") #Se espera un Identificador <Nombre de la variable>
    self.coincidir("OPERATOR") #Se espera un Operador <ej. Suma>
    self.coincidir("IDENTIFIER") #Se espera un Identificador <Nombre de la varible>
    self.coincidir("DELIMITER") #Se espera un ;
  

#Análisis sintáctico
try:
  print("Iniciando analisis sintactico...")
  parcer = Parcer(tokens_globales)
  res = parcer.parcear()
  print("Analisis sintactico completado sin errores")
except SyntaxError as e:
  print(e)