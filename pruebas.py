import re

tokens_patron = {
    "KEYWORD": r"\b(if|else|while|for|print|return|int|float|void)\b",
    "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    "NUMBER": r"\b\d+(\.\d+)?\b",
    "OPERATOR": r"[+\-*/]|==|=|\+\+|--",
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

# Analisis lexico
codigo_fuente = """
print(hola);
"""

tokens_globales = identificar_token(codigo_fuente)
print("Tokens encontrados:")
for tipo, valor in tokens_globales:
    if valor == "=":
        print(f"{tipo} : {valor} (asignación)")
    elif valor == "==":
        print(f"{tipo} : {valor} (comparación)")
    elif valor == "++":
        print(f"{tipo} : {valor} (incremento)")
    elif valor == "--":
        print(f"{tipo} : {valor} (decremento)")
    else:
        print(f"{tipo} : {valor}")

# Identificador sintáctico
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def obtener_token_actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def coincidir(self, tipo_esperado):
        token_actual = self.obtener_token_actual()
        if token_actual and token_actual[0] == tipo_esperado:
            self.pos += 1
            return token_actual[1]
        else:
            raise SyntaxError(f"Error sintactico, se esperaba {tipo_esperado}, pero se encontro: {token_actual}")

    def parsear(self):
        while self.obtener_token_actual():
            self.analizar_sentencia()
        print("Analisis sintactico completado sin errores")

    def analizar_sentencia(self):
        token_actual = self.obtener_token_actual()
        if token_actual and token_actual[0] == "KEYWORD":
            palabra = self.coincidir("KEYWORD")
            if palabra == "print":
                self.coincidir("DELIMITER")  # ()
                mensaje = self.coincidir("IDENTIFIER")
                self.coincidir("DELIMITER")  # )
                self.coincidir("DELIMITER")  # ;
                print(f"Imprimiendo: {mensaje}")
            elif palabra == "if":
                self.coincidir("DELIMITER")  # (
                condicion = self.expresion()
                self.coincidir("DELIMITER")  # )
                self.coincidir("DELIMITER")  # {
                if condicion:
                    self.analizar_sentencia()
                self.coincidir("DELIMITER")  # }
            elif palabra == "else":
                self.coincidir("DELIMITER")  # {
                self.analizar_sentencia()
                self.coincidir("DELIMITER")  # }
        else:
            self.expresion()
            self.coincidir("DELIMITER")  # ;

    def expresion(self):
        resultado = self.termino()
        while self.obtener_token_actual() and self.obtener_token_actual()[0] == "OPERATOR" and self.obtener_token_actual()[1] in {"+", "-"}:
            operador = self.coincidir("OPERATOR")
            derecho = self.termino()
            if operador == "+":
                resultado += derecho
            elif operador == "-":
                resultado -= derecho
        return resultado

    def termino(self):
        resultado = self.factor()
        while self.obtener_token_actual() and self.obtener_token_actual()[0] == "OPERATOR" and self.obtener_token_actual()[1] in {"*", "/"}:
            operador = self.coincidir("OPERATOR")
            derecho = self.factor()
            if operador == "*":
                resultado *= derecho
            elif operador == "/":
                resultado /= derecho
        return resultado

    def factor(self):
        token_actual = self.obtener_token_actual()
        if token_actual[0] == "NUMBER":
            return float(self.coincidir("NUMBER"))
        elif token_actual[0] == "DELIMITER" and token_actual[1] == "(":
            self.coincidir("DELIMITER")
            resultado = self.expresion()
            self.coincidir("DELIMITER")
            return resultado
        else:
            raise SyntaxError(f"Error sintactico, se esperaba un numero o '(', pero se encontro: {token_actual}")

try:
    print("Iniciando analisis sintactico...")
    parser = Parser(tokens_globales)
    parser.parsear()
except SyntaxError as e:
    print(e)
