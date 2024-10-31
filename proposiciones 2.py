import re  # Importa el módulo re para trabajar con expresiones regulares
import pickle  # Importa pickle para la serialización de objetos

# Diccionario para almacenar proposiciones identificadas
proposiciones_guardadas = {}

# Cargar proposiciones guardadas desde un archivo
def cargar_proposiciones():
    global proposiciones_guardadas
    try:
        with open('proposiciones.pkl', 'rb') as file:
            proposiciones_guardadas = pickle.load(file)
            print("Proposiciones cargadas correctamente.")
    except (FileNotFoundError, EOFError):
        print("No se encontraron proposiciones guardadas, se empezará desde cero.")

# Guardar proposiciones en un archivo binario
def guardar_proposiciones():
    with open('proposiciones.pkl', 'wb') as file:
        pickle.dump(proposiciones_guardadas, file)
        print("Proposiciones guardadas correctamente.")

# Guardar proposiciones en un archivo de texto
def guardar_proposiciones_txt():
    with open('proposiciones.txt', 'w', encoding='utf-8') as file:
        for letra, proposicion in proposiciones_guardadas.items():
            file.write(f"{letra}: {proposicion}\n")
    print("Proposiciones guardadas en proposiciones.txt correctamente.")

def identificar_proposiciones(oracion):
    # Define los conectores lógicos y sus símbolos equivalentes
    operadores = {
        " y ": "∧",
        " o ": "∨",
        "no ": "¬",
        " pero ": "∧",
        " además, ": "∧",
        " Además, ": "∧",
        ", ": "∧"
    }
    
    # Reemplaza los conectores en la oración con sus símbolos
    for conector, simbolo in operadores.items():
        oracion = oracion.replace(conector, simbolo)

    # Divide la oración en proposiciones simples y operadores
    proposiciones_simples = re.split(r'[∧∨]', oracion)
    operadores_encontrados = re.findall(r'[∧∨]', oracion)
    
    # Crea una lista para almacenar las letras que representan proposiciones
    letras = []
    for i, prop in enumerate(proposiciones_simples):
        prop = prop.strip()  # Limpia espacios en blanco al inicio y final
        if '¬' in prop:  # Verifica si la proposición contiene negación
            letras.append('¬' + chr(65 + i))  # Agrega ¬ seguido de una letra (A, B, C, ...)
            proposiciones_guardadas[f'¬{chr(65 + i)}'] = prop.replace('¬', 'no ')
        else:
            letras.append(chr(65 + i))  # Solo agrega la letra (A, B, C, ...)
            proposiciones_guardadas[chr(65 + i)] = prop  # Guarda la proposición sin negación

    # Reconstruye la oración utilizando las letras y los operadores
    nueva_oracion = ""
    for i in range(len(letras)):
        nueva_oracion += letras[i]
        if i < len(operadores_encontrados):
            nueva_oracion += operadores_encontrados[i]
    
    return nueva_oracion, letras

def revisar_proposiciones():
    print("Proposiciones guardadas:")
    for letra, proposicion in proposiciones_guardadas.items():
        print(f"{letra}: {proposicion}")

# Cargar proposiciones al inicio
cargar_proposiciones()

# Ejemplo de uso de la función
oracion = input("Por favor, ingresa una proposición: ")
frase_con_cambios, letras = identificar_proposiciones(oracion)  # Llama a la función con un ejemplo de oración

print("Frase con cambios:", frase_con_cambios)  # Imprime la nueva oración con cambios
print("Frases sustituidas por letras:", letras)  # Imprime las frases originales sustituidas por letras

# Revisar y mostrar proposiciones guardadas
revisar_proposiciones()

# Guardar proposiciones después de cada ejecución
guardar_proposiciones()
guardar_proposiciones_txt()  # También guarda en el archivo de texto
