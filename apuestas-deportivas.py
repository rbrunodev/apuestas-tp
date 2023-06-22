import json
import csv
from matplotlib import pyplot as plt
from passlib.context import CryptContext
from PIL import Image
import http.client
import urllib.request
import os
import random

context = CryptContext(
    schemes = ["pbkdf2_sha256"],
    default = "pbkdf2_sha256",
    pbkdf2_sha256__default_rounds = 30000
)

def verificar_contraseña(password:str, cryppass:str) -> bool:
    '''Toma la contraseña ingresada y la contraseña del usuario al que se desea acceder, devolviendo un booleano.'''
    lock = context.verify(password, cryppass)

    return lock

def buscar_credenciales(user_dict:dict) -> str:
    '''Toma datos del diccionario de usuarios y devuelve una variable con el usuario que inició sesión.'''
    search_id = list(user_dict.keys())
    search_user = []

    for users in user_dict:
        search_user.append(user_dict[users][0])
    
    user = input("Ingrese su nombre de usuario: ")
    while user == "" or user not in search_user:
        user = input("Usuario inexistente. Ingrese su nombre de usuario: ")
    
    x = search_user.index(user)
    user_id = search_id[x]
    cryppass = user_dict[user_id][1]
    password = input("Ingrese su contraseña: ")
    lock = verificar_contraseña(password,cryppass)
    while cryppass == ""  or lock is False:
        print()
        password = input("La contraseña no es correcta, por favor, vuelva a ingresar la contraseña: ")
        lock = verificar_contraseña(password,cryppass)
    print()
    print(f"Bienvenido {user}!!!")
    print()
    return user

def crear_credenciales(user_dict:dict) -> None:
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

    return user

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

def mostrar_equipo(equipos: dict)->None:
    '''Recibe el diccionario de cada equipo e imprime por pantalla.'''
    
    #solicita uno al usuario
    equipo = pedir_equipo(equipos)
    id = equipos[equipo]
    
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
    '''Recibe un anio e imprime por pantalla.'''
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
    '''Recibe los equipos e imprime por pantalla.'''
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
    
def leer_archivo_usuarios(archivo:str):
    '''Recibe el archivo usuarios.csv y me devuelve sus datos en un diccionario'''
    usuarios = {}
    with open(archivo, 'r') as archivo_aux:
        texto = csv.reader(archivo_aux)
        next(texto)
        for linea in texto:
            email = linea[0]
            valores = linea[1:]
            usuarios[email] = valores

    for clave in usuarios:
        usuarios[clave][2] = int(usuarios[clave][2])
        usuarios[clave][3] = int(usuarios[clave][3])
        usuarios[clave][4] = int(usuarios[clave][4])

    return usuarios

def escribir_archivo_dict(usuarios: dict, archivo_nuevo:str)->None:
    '''Recibe los usuarios y el nombre del archivo donde escribe crea ese archivo.csv con los datos de un diccionario'''

    with open(archivo_nuevo, 'w', newline="") as archivo:
        escritor = csv.writer(archivo)
        for clave, valores in usuarios.items():
            linea = [clave] + valores
            escritor.writerow(linea)

def cargar_dinero(usuarios: dict, usuario: str)->None:
    '''Recibe usuarios y el id del usuario (mail), y actualiza el monto de dinero disponible en ese diccionario'''

    ingreso = int(input("Ingrese el monto a ingresar: "))

    for user in usuarios:
        if usuarios[user][0] == usuario:
            usuarios[user][4] += ingreso

    print("Dinero cargado correctamente")

def mayor_apostado(usuarios: dict)->None: 
    '''Recibe los usuarios, ordena y imprime por pantalla el usuario que mas aposto'''
    valores = list(usuarios.values())
    valores_ordenada = sorted(valores, key=lambda x: x[2], reverse=True)

    print(f"El usuario {valores_ordenada[0][0]} es el que mas aposto ({valores_ordenada[0][2]})")

def leer_archivo_transacciones(archivo:str)->list:
    '''Recibe el archivo transaccioness.csv y me devuelve sus datos en una lista de listas'''
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

def mas_gano(lista: dict)->None:
    '''Recibe la lista proveniente del archivo transacciones.csv e imprime el que mas gano'''
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

def limpiar_consola()->None:
    '''Limpia la consola del sistema.'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pago_apuestas(fixture_id:int, team_local:str)->list:
    '''Recibe el fixture id y el equipo que es local, consulta en la api las predicciones de ese partido y devuelve, 
    segun esos datos, cuanto se le pagara a cada equipo L/V'''

    prediction = []

    if(api_predictions_por_fixture(fixture_id)):
        prediction = api_predictions_por_fixture(fixture_id)

    number = random.randint(1, 4)

    pay_local = number
    pay_visitor = number

    if(len(prediction) > 0):
        winner_name : str = prediction['winner_name']
        if(winner_name.upper() == team_local.upper()):
            if(prediction['win_or_draw']):
                pay_local = pay_local * 0.1
            else:
                pay_visitor = pay_visitor * 0.1
        else: 
            if(prediction['win_or_draw']):
                pay_visitor = pay_visitor * 0.1
            else:
                pay_local = pay_local * 0.1
    
    return [round(pay_local,1), round(pay_visitor, 1)]

def api_fixture(id_equipo: int, equipo: str, fixtures:dict)->None:
    ''' Recibe el id del equipo y carga los datos en el dict fixtures'''
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "e47f133bb10ac93f5737c9bedbe082e3"
        }
    conn.request("GET", f"/fixtures?league=128&season=2023&team={id_equipo}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    data_decode = data.decode("utf-8")
    data_format = json.loads(data_decode)

    response : list = data_format['response']

    for res in response:
        team_home : str = res['teams']['home']['name']
        fixtures[res['fixture']['id']] = {
            'codigo' : res['fixture']['id'],
            'date' : res['fixture']['date'], 
            'team_local' : res['teams']['home']['name'],
            'team_visitor' : res['teams']['away']['name'],
            'rival' : res['teams']['away']['name'] if team_home.upper() == equipo else team_home
        }

def api_predictions_por_fixture(fixture_id : int)->dict:
    '''Recibe el id del fixture y devuelve la prediction de ese partido'''
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "e47f133bb10ac93f5737c9bedbe082e3"
        }

    conn.request("GET", f"/predictions?fixture={fixture_id}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data_decode = data.decode("utf-8")
    data_format = json.loads(data_decode)

    response : list = data_format['response']

    prediction = {}

    for res in response:
        prediction = {
            'winner_id' : res['predictions']['winner']['id'],
            'winner_name' : res['predictions']['winner']['name'],
            'win_or_draw' : res['predictions']['win_or_draw'],
            'prediction': res['predictions']['advice']
        }
    
    return prediction

def validacion_cod_fixture(codigo:int, fixtures:dict)->bool:
    '''Verfica que el codigo (id del fixture) este dentro del dict de fixtures'''
    return codigo not in list(fixtures.keys())

def elegir_partido(fixtures:dict)->int:
    '''Recibe el diccionario de fixtures y devuelve el codigo ingresado por el usuario habiendo
    verificado que exista en los fixtures.'''
    codigo = int(input("Ingrese el codigo de la fecha por la que quiere apostar: "))
    while(validacion_cod_fixture(codigo, fixtures)):
        print("El codigo ingresado no corresponde a una fecha de partido. Intente nuevamente.")
    
    return codigo

def dinero_disponible(usuario:str, usuarios:dict)->int:
    '''Recibe el id del usuario (mail) y el dict de usuarios y devuelve el dinero disponible que tiene ese usuario'''
    datos_usuario = usuarios[usuario]
    
    return int(datos_usuario[4])

def simular_resultado()->str:
    '''Devuelve una inicial que simula un resultado de partido.'''
    dado = random(1, 3)
    if(dado == 1):
        return "L"

    if(dado == 2):
        return "E"
    
    if(dado == 3):
        return "V"
    
def cargar_dinero_disponible(usuario: str, dinero:int)->None:
    '''Recibe el id del usuario(mail) y el dinero a cargar.
    Modifica el archivo usuarios para actualizar el monto disponible de ese usuario'''
    archivo_csv = 'usuarios.csv'
    datas = []
    with open(archivo_csv, 'r') as archivo:
        leer = csv.reader(archivo)
        for fila in leer:
            datas.append(fila)
    
    for data in datas:
        if(data[0] == usuario):
            data[5] = int(data[5]) + dinero
    
    with open(archivo_csv, 'w', newline='') as archivo:
        escribir = csv.writer(archivo)
        escribir.writerows(datas)

def descontar_dinero(usuario:str, monto_descontar:int)->None:
    '''Recibe el id del usuario(mail) y el monto a descontar.
    Modifica el archivo usuarios para actualizar el monto disponible de ese usuario'''
    archivo_csv = 'usuarios.csv'
    datas = []
    with open(archivo_csv, 'r') as archivo:
        leer = csv.reader(archivo)
        for fila in leer:
            datas.append(fila)
    
    for data in datas:
        if(data[0] == usuario):
            data[5] = int(data[5]) - monto_descontar
    
    with open(archivo_csv, 'w', newline='') as archivo:
        escribir = csv.writer(archivo)
        escribir.writerows(datas)

def existe_archivo(nombre_archivo:str)->bool:
    '''Recibe el nombre del archivo y devuelve un bool (True/False) si el archivo existe o no.'''
    return os.path.exists(nombre_archivo)

def archivo_vacio(nombre_archivo:str)->bool:
    '''Recibe el nombre del archivo y verifa que no este vacio. Devuelve un True o False.'''
    with open(nombre_archivo, 'r') as archivo:
        caracter = archivo.read(1)
        print(caracter)
        if(caracter):
            False
        else: 
            True
            
def guardar_transacciones(usuario:str, dinero:int, tipo:str)->None:
    '''Recibe el id usuario (mail), el dinero y el tipo de transaccion.
    Guarda en el archivo transacciones los datos.'''
    encabezados = ['idEmail', 'fecha', 'tipo', 'importe']
    datos = []
    archivo_vacio = True 

    if(existe_archivo('transacciones.csv')):
        archivo_vacio = False
        with open('transacciones.csv', 'r') as archivo:
            leer = csv.reader(archivo)
            for fila in leer:
                datos.append(fila)
            
    fila = [usuario, 'hoy', tipo, dinero]
    datos.append(fila)

    with open('transacciones.csv', 'w', newline='') as archivo:
        escribir = csv.writer(archivo)
        if(archivo_vacio == False):
            escribir.writerows(datos)
        else: 
            escribir.writerow(encabezados)
            escribir.writerows(datos)
    return

def apostar_partido(codigo:int, fixtures:dict, usuario: str, usuarios:dict)->None:
    '''Recibe el id del fixture, el dict de fixtures y el id del usuario (mail)
    El usuario apuesta por un partido con su dinero disponible y se le devuelve un mensaje con su situacion, 
    si gano o perdio lo apostado. En ambos casos se guarda la transaccion y se descuenta o se suma a su dinero en cuenta.'''
    limpiar_consola()
    print("-- Datos del partido -- ")
    print(f"Equipo local: {fixtures[codigo]['team_local']} - PAGA: {fixtures[codigo]['pay_local']} lo apostado")
    print(f"Equipo visitante: {fixtures[codigo]['team_visitor']} - PAGA: {fixtures[codigo]['pay_visitor']} lo apostado")

    equipo = input("Ingrese por quien quiere apostar Local o visitante. (L/V) :")
    while(equipo[0] not in ['L', 'V', 'l', 'v']):
        equipo = input("Debe ingresar por quien quiere apostar LOCAL o VISITANTE. (L/V) :")

    apuesta = input("Ingrese si GANA, EMPATE o PIERDE el equipo que elijio (G/P/E): ")
    while(apuesta[0] not in ['G', 'P', 'E', 'e', 'g', 'p']):
        apuesta = input("Debe ingresar su apuesta. GANA, PIERDE o EMPATA su equipo elegido (G/P/E): ")

    dinero = dinero_disponible(usuario, usuarios)

    if(dinero == 0):
        print("Usted no dispone de dinero para apostar.")
        print("Finalizo el programa")
        fixtures.clear()
        return

    print(f"Usted tiene disponible {dinero}.")
    monto = int(input("Ingrese el monto a apostar: "))

    while(monto > dinero):
        print("No dispone de dinero disponible para apostar el monto ingreado.")
        monto = int(input("Ingrese otro monto a apostar: "))

    resultado = simular_resultado()

    dinero_ganado = 0

    if(resultado == "L" & equipo[0].upper()): #gana el equipo elegido
        if(apuesta[0] == "G" or apuesta[0] == "E" ):
            dinero_ganado = monto * fixtures[codigo]['pay_local']
            print("Has ganado!")
    
    if(resultado == "V" & equipo[0].upper()):  #gana el equipo elegido
        if(apuesta[0] == "G" or apuesta[0] == "E" ):
            dinero_ganado = monto * fixtures[codigo]['pay_visitor']
            print("Has ganado!")
    
    if(dinero_ganado > 0):  
        cargar_dinero_disponible(usuario, dinero_ganado)
        guardar_transacciones(usuario, dinero_ganado, 'Gana')
        print("Hemos cargado su dinero ganado correctamente!")
        fixtures.clear()
        return
    else: 
        descontar_dinero(usuario, monto)
        guardar_transacciones(usuario, - monto, 'Pierde')
        print("Hemos descontado de su dinero disponible lo apostado.")
        fixtures.clear()
        return
    
def listado_fixture(equipo: str, fixtures:dict, equipos:dict)->None:
    '''Recibe el nombre de un equipo e imprime el listado de partidos que debe jugar en el torneo'''
    id_equipo = equipos[equipo]

    api_fixture(id_equipo, equipo, fixtures)

    count = 1
    if(len(fixtures) > 0):
        for fixture in fixtures.values():
            pagos = pago_apuestas(fixture['codigo'], fixture['team_local'])
            fixture['pay_local'] = pagos[0] 
            fixture['pay_visitor'] = pagos[1] 
            print(f"************** Fecha {count} ************************")
            print(f"Codigo: {fixture['codigo']}")
            print(f"Fecha: {fixture['date']}")
            print(f"Rival: {fixture['rival']}")
            print(f"Local: {fixture['team_local']}, PAGA: {pagos[0]} veces lo apostado")
            print(f"Visitante: {fixture['team_visitor']}, PAGA: {pagos[1]} veces lo apostado")
            count += 1
        print("************************************************")

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
    
    print("\nBienvenido a Jugarsela!!!")
    choice1 = input("\nDigite:\n'i' si desea ingresar a una cuenta existente,\n'r' si desea registrar una cuenta nueva: ")
    choice1.lower()
    while choice1 != "i" and choice1 != "r":
        choice1 = input("\nDigite:\n'i' si desea ingresar a una cuenta existente,\n'r' si desea registrar una cuenta nueva: ")
    if choice1 == "r":
        print("Registro de cuenta nueva.\n")
        user_online = crear_credenciales(users_dict)
    elif choice1 == "i":
        print("ingreso a cuenta existente.\n")
        user_online = buscar_credenciales(users_dict) #Almaceno el usuario conectado para tomarlo de referencia en operaciones posteriores.

    equipos = {
        "RIVER PLATE": 435, "TALLERES": 456, "SAN LORENZO": 460, "ESTUDIANTES LP": 450, "ROSARIO CENTRAL": 437,
        "DEFENSA Y JUSTICIA": 442, "LANUS": 446, "BELGRANO": 440, "ARGENTINOS JUNIORS": 458, "GODOY CRUZ": 439,
        "BOCA JUNIORS": 451, "NEWELLS OLD BOYS": 457, "PLATENSE": 1064, "SARMIENTO": 474,
        "GIMNASIA LP": 434, "CENTRAL CORDOBA DE SANTIAGO DEL ESTERO": 1065, "COLON": 448, "RACING CLUB": 436,
        "BARRACAS CENTRAL": 2432, "TIGRE": 452, "INSTITUTO": 478, "INDEPENDIENTE": 453, "ATLETICO TUCUMAN": 455,
        "UNION DE SANTA FE": 441, "VELEZ SARFIELD": 438, "HURACAN": 445, "BANFIELD": 449, "ARSENAL DE SARANDI": 459
    }


    menu = """
    MENU
    
    a. Mostrar el plantel de un equipo
    b. Mostrar posiciones por temporada
    c. Informacion de estadio y escudo de un equipo
    d. Grafico con goles y minutos
    e. Cargar dinero
    f. Mostrar usuario que mas apostó
    g. Mostrar usuario que mas veces ganó
    h. Ingrese a realizar una apuesta.
    i. Salir
    
    """

    print(menu)

    opciones = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    opcion = input("Ingrese una opcion: ")

    while opcion not in opciones:
        opcion = input("Ingrese una opcion valida: ")
    
    while opcion != "i":
        if opcion == "a":
            listar_equipos(equipos)
            mostrar_equipo(equipos)
        elif opcion == "b":
            anio = pediranio()
            mostrar_tabla(anio)
        elif opcion == "c":
            listar_equipos(equipos)
            mostrar_info(equipos)
        elif opcion == "d":
            listar_equipos(equipos)
            equipo = pedir_equipo(equipos)
            goals_x_min(equipo, equipos)
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
        elif opcion == "h":
            fixtures = {}
            equipo = input("Ingrese el nombre del equipo para conocer el listado del fixture: ")
            while equipo.upper() not in equipos:
                print("Debe ingresar el nombre de un equipo de la Liga Profesional 2023")
                equipo = input("Ingrese el nombre del equipo: ")

            listado_fixture(equipo.upper(), fixtures, equipos)

            if(len(fixtures) == 0):
                print("No hay partidos para mostrarle.")

            while len(fixtures) > 0: 
                codigo = elegir_partido(fixtures)
                apostar_partido(codigo, fixtures, user_online, users_dict)
        print("")
        print(menu)
        print("")
        opcion = input("Ingrese una opcion: ")
    print("Gracias!")
main()