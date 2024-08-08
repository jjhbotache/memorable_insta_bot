import random


def trim_json_str(json_str):
    # Encuentra la primera ocurrencia de '{'
    start = json_str.find('{')
    if start == -1:
        raise "No se encontró '{' en la cadena"
    
    # Encuentra la última ocurrencia de '}'
    end = json_str.rfind('}')
    if end == -1:
        raise "No se encontró '}' en la cadena"
    
    # Verifica que '{' viene antes que '}'
    if start >= end:
        raise "La primera '{' aparece después de la última '}'"
    
    # Corta y devuelve la subcadena desde '{' hasta '}'
    
    json = json_str[start:end+1]
    return str(json)

def get_random_syllable():
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    return random.choice(consonants) + random.choice(vowels)