import random
import string

def gerar_id():
    """Gera ID no formato AAA-99999"""
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=5))
    return f"{letras}-{numeros}"