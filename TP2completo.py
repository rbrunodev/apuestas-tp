import json
import csv
from matplotlib import pyplot as plt
from passlib.context import CryptContext
import http.client
from PIL import Image
import urllib.request
import os

context =   CryptContext(
    schemes = ["pbkdf2_sha256"],
    default = "pbkdf2_sha256",
    pbkdf2_sha256__default_rounds = 30000
)


def verificar_contraseña(password,passlist) -> bool:

    for i in range(0,len(passlist)):
        lock = context.verify(password, passlist[i])
        if lock is False:
            pass
        elif lock is True: 
            break
    return lock

def buscar_credenciales(user_dict) -> str:

    '''Toma datos del diccionario de usuarios y devuelve una variable con el usuario que inició sesión.'''
    search_user = []
    search_password = []
    for users in user_dict:
        search_user.append(user_dict[users][0])
    for passwords in user_dict:
        search_password.append(user_dict[passwords][1])
   
    user = input("Ingrese su nombre de usuario: ")
    while user == "" or user not in search_user:
        user = input("Usuario inexistente. Ingrese su nombre de usuario: ")
    cryppass = input("Ingrese su contraseña: ")
    lock = verificar_contraseña(cryppass,search_password)
    while cryppass == ""  or lock is False:
        cryppass = input("La contraseña no es correcta, por favor, vuelva a ingresar la contraseña: ")
        lock = verificar_contraseña(cryppass,search_password)
    print()
    print(f"Bienvenido {user}!!!")
    print()
    return user

def crear_credenciales(user_dict) -> None:

    '''Solicito el diccionario de usuarios para comparar datos existentes, 
    agrego dicho usuario al diccionario y al arhivo csv.'''
    search_id = sorted(list(user_dict.keys()))
    search_user = []
    for users in user_dict:
        search_user.append(user_dict[users][0])
    id = input("Ingrese su correo electrónico: ")
    while id in search_id:
        id = input("Este correo ya se encuentra asociado a una cuenta existente. Por favor, ingrese un nuevo correo: ")
    user = input("Ingrese un nuevo de usuario: ")
    while user in search_user:
        user = input("Este usuario ya se encuentra asociado a una cuenta existente. Por favor, ingrese un nuevo usuario: ")
    password = input("Ingrese una contraseña: ")
    while password == "" or len(password) < 4:
        password = input("La contraseña debe ser de un mínimo de 4 caracteres, por favor, ingrese una nueva contraseña: ")
    password = context.hash(password)
    moneyspend = 0
    lastgamble = 00000000
    balance = 0
    user_dict[id] = [user,password,moneyspend,lastgamble,balance]
    with open("users_info.csv", "a") as users_info:
        new_user = (f"{id},{user},{password},{moneyspend},{lastgamble},{balance}")
        users_info.write(f"\n{new_user}")
    users_info.close()

def pedir_equipo(diccionario:dict) -> str:

    '''Utilizo el diccionario de equipos para validar la elección del usuario, devuelvo su nombre con un str.'''
    equipos = diccionario.keys()
    eleccion = input("Ingrese el equipo de la manera en la que se muestra en la lista: ")
    eleccion = eleccion.upper()
    print(eleccion)

    while eleccion not in equipos:
        print("El equipo fue mal ingresado o no forma parte de la LPF 2023")
        eleccion = input("Ingrese el equipo de la manera en la que se muestra en la lista: ")

    return eleccion

def listar_equipos(diccionario: dict) -> None:

    '''Solicito el diccionario con los equipos existentes para imprimir una lista de opciones para el usuario.'''
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
    
def mostrar_tabla(anio: int):

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
        next(texto)

        for linea in texto:
            clave = linea[0]
            valores = linea[1:]
            diccionario[clave] = valores


    
    for clave in diccionario:
        diccionario[clave][2] = int(diccionario[clave][2])
        diccionario[clave][3] = int(diccionario[clave][3])
        diccionario[clave][4] = int(diccionario[clave][4])

    return diccionario

def escribir_archivo_dict(diccionario: dict, archivo_nuevo):
    #escribe un nuevo archivo .csv con los datos de un diccionario
    #usar para usuarios.csv

    with open(archivo_nuevo, 'w', newline="") as archivo:
        escritor = csv.writer(archivo)
        for clave, valores in diccionario.items():
            linea = [clave] + valores
            escritor.writerow(linea)

def cargar_dinero(usuarios: dict, usuario: str) -> dict:
    #recibe el diccionario proveniente del archivo usuarios y el usuario, y devuelve el mismo diccionario con el nuevo monto de dinero disponible

    ingreso = int(input("Ingrese el monto a ingresar: "))

    for user in usuarios:
        if usuarios[user][0] == usuario:
            usuarios[user][4] += ingreso

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
        next(texto)

        for linea in texto:
            listas.append(linea)

    for lista in listas:
        lista[1] = int(lista[1])
        lista[3] = int(lista[3])

    return listas

def mas_gano(lista: dict):
#recibe la lista proveniente del archivo transacciones.csv e imprime el que mas gano

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

def escribir_archivo_list(lista: list, archivo_nuevo):
    #escribe un nuevo archivo .csv con los datos de una lista de listas
    #usar para generar transacciones.csv

    with open(archivo_nuevo, 'w', newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(lista)

def goals_x_min(team: str, diccionario: dict) -> None:

    '''Pido el nombre del equipo y el diccionario con los ids de equipos para imprimir el gráfico solicitado.'''
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "2065f862b63d3baeaaeccc0a7b159ddd"
        }

    conn.request("GET", f"/teams/statistics?season=2023&team={diccionario[team]}&league=128", headers=headers)

    res = conn.getresponse()
    data = res.read()

    decode_data = data.decode("utf-8")
    format_data = json.loads(decode_data)

    goals_by_minute = format_data['response']['goals']['for']['minute']
    minutes = []
    goals = []

    for minute, goal_info in goals_by_minute.items():
        if goal_info['total'] is not None:
            minutes.append(int(minute.split('-')[0]))
            goals.append(goal_info['total'])

    plt.rcParams['toolbar'] = 'None'

    plt.step(minutes, goals, where='post')
    plt.xlabel('Minutos')
    plt.ylabel('Goles')
    plt.title(f'Goles por munto de {team}')
    plt.show()

def main():

    users_dict = {}
    with open("users_info.csv",newline='',encoding='UTF-8') as user_info:
        csv_reader = csv.reader(user_info)
        next(csv_reader)
        for line in user_info:
            id, user, password, moneyspend, lastgamble, num = line.split(',')
            balance = num.split("\r\n")
            balance = balance[0]
            users_dict[id] = [user,password,moneyspend,lastgamble,balance]
        user_info.close()
    
    print("\nBienvenido a Jugarsela!!!")
    choice1 = input("\nDigite:\n'i' si desea ingresar a una cuenta existente,\n'r' si desea registrar una cuenta nueva,\n'Enter' si desea salir. ")
    while choice1 == "i" or choice1 == "r":
        choice1.lower()
        if choice1 == "r":
            print("Registro de cuenta nueva.\n")
            crear_credenciales(users_dict)
            choice1 = input("\nDigite:\n'i' si desea ingresar a una cuenta existente,\n'r' si desea registrar una cuenta nueva,\n'Enter' si desea salir. ")
        elif choice1 == "i":
            print("ingreso a cuenta existente.\n")
            user_online = buscar_credenciales(users_dict) #Almaceno el usuario conectado para tomarlo de referencia en operaciones posteriores.
            if user_online != "":
                break


    diccionario_id = {"RIVER PLATE": 435, "TALLERES": 456, "SAN LORENZO": 460, "ESTUDIANTES LP": 450, "ROSARIO CENTRAL": 437,
                      "DEFENSA Y JUSTICIA": 442, "LANUS": 446, "BELGRANO": 440, "ARGENTINOS JUNIORS": 458, "GODOY CRUZ": 439,
                      "BOCA JUNIORS": 451, "NEWELLS OLD BOYS": 457, "PLATENSE": 1064, "SARMIENTO": 474,
                      "GIMNASIA LP": 434, "CENTRAL CORDOBA DE SANTIAGO DEL ESTERO": 1065, "COLON": 448, "RACING CLUB": 436,
                      "BARRACAS CENTRAL": 2432, "TIGRE": 452, "INSTITUTO": 478, "INDEPENDIENTE": 453, "ATLETICO TUCUMAN": 455,
                      "UNION DE SANTA FE": 441, "VELEZ SARFIELD": 438, "HURACAN": 445, "BANFIELD": 449, "ARSENAL DE SARANDI": 459}


    menu = """
    MENU
    
    a. Mostrar el plantel de un equipo
    b. Mostrar posiciones por temporada
    c. Informacion de estadio y escudo de un equipo
    d. Grafico con goles y minutos
    e. Cargar dinero
    f. Mostrar usuario que mas apostó
    g. Mostrar usuario que mas veces ganó
    h. Salir
    
    """

    print(menu)

    opciones = "abcdefgh"
    opciones = list(opciones)
    opcion = input("Ingrese una opcion: ")

    while opcion not in opciones:
        opcion = input("Ingrese una opcion valida: ")
    
    while opcion != "h":

        if opcion == "a":
            
            listar_equipos(diccionario_id)
            mostrar_equipo(diccionario_id)

        elif opcion == "b":
            
            anio = pediranio()
            mostrar_tabla(anio)

        elif opcion == "c":
            
            listar_equipos(diccionario_id)
            mostrar_info(diccionario_id)

        elif opcion == "d":
            
            listar_equipos(diccionario_id)
            equipo = pedir_equipo(diccionario_id)
            goals_x_min(equipo, diccionario_id)

        elif opcion == "e":
            
            usuarios_dict = leer_archivo_usuarios("users_info.csv")
            cargar_dinero(usuarios_dict, user_online)
            escribir_archivo_dict(usuarios_dict, "users_info.csv")

        elif opcion == "f":
            
            usuarios_dict_1 = leer_archivo_usuarios("users_info.csv")
            mayor_apostado(usuarios_dict_1)            

        elif opcion == "g":

            transacciones = leer_archivo_transacciones("transacciones.csv")
            mas_gano(transacciones)

        print("")
        print(menu)
        print("")
        opcion = input("Ingrese una opcion: ")

    print("Gracias!")

main()