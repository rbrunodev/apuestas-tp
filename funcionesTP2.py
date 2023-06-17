import http.client
import json
from PIL import Image
import urllib.request
import csv
import os


def generar_diccionario() -> dict:
    #genera un diccionario en donde las claves son los equipos y el valor los id
    #LA FUNCION ESTA EN REALIDAD NO SIRVE, EN LA API NO ESTAN CARGADOS TODOS LOS EQUIPOS PARA 2023 Y SI HAGO REQUEST DE 2022 HAY EQUIPOS QUE YA NO ESTAN EN 2023
    #EL DICCIONARIO SE CREA MANUALMENTE

    #request de la tabla de posiciones 2023
    import http.client

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "af9675e5c749d2035287a6b4aa76a41c"
        }

    conn.request("GET", "/standings?league=128&season=2023", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #transformo en objeto python
    decode_data = data.decode("utf-8")
    format_data = json.loads(decode_data)

    #acomodo la response
    info: list = format_data["response"]
    informacion: dict = info[0]
    posiciones: list = informacion["league"]["standings"]
    posiciones0: list = posiciones[0]

    #itero sobre la info y extraigo los equipos con su id
    diccionario = {}
    for equipo in posiciones0:
        nombre = equipo["team"]["name"]
        id = equipo["team"]["id"]
        diccionario[nombre] = id

    print(diccionario)

def pedir_equipo(diccionario:dict) -> str:

    equipos = diccionario.keys()
    eleccion = input("Ingrese el equipo de la manera en la que se muestra en la lista: ")

    while eleccion not in equipos:
        print("El equipo fue mal ingresado o no forma parte de la LPF 2023")
        eleccion = input("Ingrese el equipo de la manera en la que se muestra en la lista: ")

    return eleccion

def listar_equipos(diccionario: dict):

    equipos = sorted(list(diccionario.keys()))
    print("EQUIPOS LPF 2023:")
    print(" ")
    for i in equipos:
        print(i)

def mostrar_equipo(diccionario: dict):
    #recibe el diccionario de cada equipo y su id
    
    #solicita uno al usuario
    equipo = pedir_equipo(diccionario)
    id = diccionario[equipo]
    

    #request a la api
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "af9675e5c749d2035287a6b4aa76a41c"
        }

    conn.request("GET", f"/players/squads?team={id}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #transformo en objeto python
    decode_data = data.decode("utf-8")
    format_data = json.loads(decode_data)

    #itero sobre toda la informacion almacenando los jugadores con su posicion en una lista de listas
    lista_jugadores = []
    informacion: list = format_data["response"]
    informacion0: dict = informacion[0]
    jugadores: list = informacion0["players"]
    for jugador in jugadores:
        jugador_info = [jugador["name"], jugador["position"]]
        lista_jugadores.append(jugador_info)

    #separo por posicion
    arqueros = []
    defensores = []
    mediocampistas = []
    delanteros = []
    for jugador in lista_jugadores:
        if jugador[1] == "Goalkeeper":
            arqueros.append(jugador[0])
        elif jugador[1] == "Defender":
            defensores.append(jugador[0])
        elif jugador[1] == "Midfielder":
            mediocampistas.append(jugador[0])
        elif jugador[1] == "Attacker":
            delanteros.append(jugador[0])


    #imprimo
    print(" ")
    print(f"PLANTEL {equipo} LPF 2023")
    print(" ")
    print("ARQUEROS")
    for i in arqueros:
        print(i)
    print(" ")
    print("DEFENSORES")
    for i in defensores:
        print(i)
    print(" ")
    print("MEDIOCAMPISTAS")
    for i in mediocampistas:
        print(i)
    print(" ")
    print("DELANTEROS")
    for i in delanteros:
        print(i)

def pediranio() -> int:

    anio = int(input("Ingrese el año a buscar la tabla de posiciones: "))

    while anio < 2015 or anio > 2023:
        print("Ingrese un año entre 2015 y 2023")
        anio = int(input("Ingrese el año a buscar la tabla de posiciones: "))

    return anio
    
def mostrar_tabla():

    anio = pediranio()

    #request a la api
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "af9675e5c749d2035287a6b4aa76a41c"
        }

    conn.request("GET", f"/standings?league=128&season={anio}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #transformo en objeto python
    decode_data = data.decode("utf-8")
    format_data = json.loads(decode_data)

    #acomodo la response
    informacion: list = format_data["response"]
    informacion0: dict = informacion[0]
    informacion1: dict = informacion0["league"]
    lista: list = informacion1["standings"]
    lista0: list = lista[0]

    #itero sobre la lista y extraigo el nombre del equipo con los puntos
    tabla = []
    for equipo in lista0:
        equipo_info = [equipo["team"]["name"], equipo["points"], equipo["rank"]]
        tabla.append(equipo_info)

    #imprimo
    for equipo in tabla:
        print(f"{equipo[2]}. {equipo[0]} | {equipo[1]} pts")

def mostrar_info(diccionario: dict):

    #solicito equipo
    equipo = pedir_equipo(diccionario)
    id = diccionario[equipo]

    #request a la api
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "af9675e5c749d2035287a6b4aa76a41c"
        }

    conn.request("GET", f"/teams?id={id}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #transformo en objeto python
    decode_data = data.decode("utf-8")
    format_data = json.loads(decode_data)

    #acomodo la response
    informacion: list = format_data["response"]
    informacion0: dict = informacion[0]

    #extraigo informacion
    nombre = informacion0["venue"]["name"]
    direccion = informacion0["venue"]["address"]
    ciudad = informacion0["venue"]["city"]
    capacidad = informacion0["venue"]["capacity"]
    superficie = informacion0["venue"]["surface"]
    link_logo = informacion0["team"]["logo"]

    if superficie == "grass":
        superficie = "pasto"

    #muestro logo
    nombre_archivo = "logo1.png"
    urllib.request.urlretrieve(link_logo, nombre_archivo)
    im = Image.open(nombre_archivo)
    im.show()

    #imprimo
    print(f"""
    INFORMACION DEL ESTADIO DE: {equipo}

    NOMBRE: {nombre}
    DIRECCION: {direccion}
    CIUDAD: {ciudad}
    CAPACIDAD: {capacidad}
    SUPERFICIE: {superficie}
    """)
    
def leer_archivo_usuarios(archivo):
    #recibe el archivo usuarios.csv y me devuelve sus datos en un diccionario
    diccionario = {}
    with open(archivo, 'r') as archivo_aux:
        texto = csv.reader(archivo_aux)
        for linea in texto:
            clave = linea[0]
            valores = linea[1:]
            diccionario[clave] = valores
    
    for clave in diccionario:
        diccionario[clave][2] = int(diccionario[clave][2])
        diccionario[clave][3] = int(diccionario[clave][3])
        diccionario[clave][4] = int(diccionario[clave][4])

    return diccionario

def escribir_archivo(diccionario: dict, archivo_nuevo):
    #escribe un nuevo archivo .csv con los datos de un diccionario

    with open(archivo_nuevo, 'w', newline="") as archivo:
        escritor = csv.writer(archivo)
        for clave, valores in diccionario.items():
            linea = [clave] + valores
            escritor.writerow(linea)

def cargar_dinero(diccionario: dict, usuario: str) -> dict:
    #recibe el diccionario proveniente del archivo y el usuario, y devuelve el mismo diccionario con el nuevo monto de dinero disponible

    ingreso = int(input("Ingrese el monto a ingresar: "))

    for user in diccionario:
        if diccionario[user][0] == usuario:
            diccionario[user][4] += ingreso

    print("Dinero cargado correctamente")

def mayor_apostado(diccionario: dict): 
    #recibe un diccionario con la info de los usuarios, ordena y muestra el usuario que mas aposto

    valores = list(diccionario.values())

    valores_ordenada = sorted(valores, key=lambda x: x[2], reverse=True)

    print(f"El usuario {valores_ordenada[0][0]} es el que mas aposto ({valores_ordenada[0][2]})")

def leer_archivo_transacciones(archivo):
    #recibe el archivo transaccioness.csv y me devuelve sus datos en una lista de listas
    listas = []
    with open(archivo, 'r') as archivo_aux:
        texto = csv.reader(archivo_aux)
        for linea in texto:
            listas.append(linea)

    for lista in listas:
        lista[1] = int(lista[1])
        lista[3] = int(lista[3])

    return listas

def mas_gano(lista: dict):
#recibe la lista proveniente del archivo transacciones.csv e imprime que mas gano

    contador = {}
    for sublista in lista:
        usuario = sublista[0]
        resultado = sublista[2]
        if resultado == "Gana":
            if usuario in contador:
                contador[usuario] += 1
            else:
                contador[usuario] = 1

    lista_aux = []
    for usuario in contador:
        usuario_y_ganadas = [usuario, contador[usuario]]
        lista_aux.append(usuario_y_ganadas)

    lista_ord = sorted(lista_aux, key=lambda x: x[1], reverse=True)

    print(f"El usuario que mas gano es {lista_ord[0][0]} ({lista_ord[0][1]} veces)")

def main():

    diccionario_id = {"River Plate": 435, "Talleres": 456, "San Lorenzo": 460, "Estudiantes LP": 450, "Rosario Central": 437,
                      "Defensa y Justicia": 442, "Lanus": 446, "Belgrano": 440, "Argentinos Juniors": 458, "Godoy Cruz": 439,
                      "Boca Juniors": 451, "Newells Old Boys": 457, "Club Atletico Platense": 1064, "Sarmiento": 474,
                      "Gimnasia LP": 434, "Central Cordoba de Santiago": 1065, "Colon": 448, "Racing Club": 436,
                      "Barracas Central": 2432, "Tigre": 452, "Instituto": 478, "Independiente": 453, "Atletico Tucuman": 455,
                      "Union de Santa Fe": 441, "Velez Sarfield": 438, "Huracan": 445, "Banfield": 449, "Arsenal de Sarandi": 459}

    

main() 
