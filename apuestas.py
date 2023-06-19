import json
import csv
import http.client
from matplotlib import pyplot as plt
from passlib.context import CryptContext
context =   CryptContext(
    schemes = ["pbkdf2_sha256"],
    default = "pbkdf2_sha256",
    pbkdf2_sha256__default_rounds = 30000
)

diccionario_id = {"RIVER PLATE": 435, "TALLERES": 456, "SAN LORENZO": 460, "ESTUDIANTES LP": 450, "ROSARIO CENTRAL": 437,
                      "DEFENSA Y JUSTICIA": 442, "LANUS": 446, "BELGRANO": 440, "ARGENTINOS JUNIORS": 458, "GODOY CRUZ": 439,
                      "BOCA JUNIORS": 451, "NEWELLS OLD BOYS": 457, "PLATENSE": 1064, "SARMIENTO": 474,
                      "GIMNASIA LP": 434, "CENTRAL CORDOBA DE SANTIAGO DEL ESTERO": 1065, "COLON": 448, "RACING CLUB": 436,
                      "BARRACAS CENTRAL": 2432, "TIGRE": 452, "INSTITUTO": 478, "INDEPENDIENTE": 453, "ATLETICO TUCUMAN": 455,
                      "UNION DE SANTA FE": 441, "VELEZ SARFIELD": 438, "HURACAN": 445, "BANFIELD": 449, "ARSENAL DE SARANDI": 459}

def generar_encripcion(password) -> str:

    #copia el código del archivo hashing_test
    print("Función en mantenimiento...")

def buscar_credenciales(user_dict) -> str:

    search_user = []
    search_password = []
    for users in user_dict:
        search_user.append(user_dict[users][0])
    for passwords in user_dict:
        search_password.append(user_dict[passwords][1])
    print(search_user)
    print(search_password)
    user = input("Ingrese su nombre de usuario: ")
    while user == "" or user not in search_user:
        user = input("Usuario inexistente. Ingrese su nombre de usuario: ")
    cryppass = input("Ingrese su contraseña: ")
    while cryppass == ""  or cryppass not in search_password:
        cryppass = generar_encripcion(input("La contraseña no es correcta, por favor, vuelva a ingresar la contraseña: "))
    print()
    print(f"Bienvenido {user}!!!")
    print()
    return user

def crear_credenciales(user_dict) -> None:

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
    moneyspend = 0
    lastgamble = 00000000
    balance = 0
    user_dict[id] = [user,password,moneyspend,lastgamble,balance]
    with open("users_info.csv", "a") as users_info:
        new_user = (f"{id},{user},{password},{moneyspend},{lastgamble},{balance}")
        users_info.write(new_user)
    users_info.close()

def pedir_equipo(diccionario:dict) -> str:

    equipos = diccionario.keys()
    eleccion = input("Ingrese el equipo de la manera en la que se muestra en la lista: ")
    eleccion = eleccion.upper()
    print(eleccion)

    while eleccion not in equipos:
        print("El equipo fue mal ingresado o no forma parte de la LPF 2023")
        eleccion = input("Ingrese el equipo de la manera en la que se muestra en la lista: ")

    return eleccion

def goals_x_min(team,diccionario_id) -> None:

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "2065f862b63d3baeaaeccc0a7b159ddd"
        }

    conn.request("GET", f"/teams/statistics?season=2023&team={diccionario_id[team]}&league=128", headers=headers)

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
        if choice1 == "i":
            print("ingreso a cuenta existente.\n")
            user_online = buscar_credenciales(users_dict) #Almaceno el usuario conectado para tomarlo de referencia en operaciones posteriores.
            pass
        elif choice1 == "r":
            print("Registro de cuenta nueva.\n")
            crear_credenciales(users_dict)
            choice1 = input("\nDigite:\n'i' si desea ingresar a una cuenta existente,\n'r' si desea registrar una cuenta nueva,\n'Enter' si desea salir. ")
        print("1. Mostrar goles por minutos(g).")
        choice2 = input("¿Que desea hacer? ")
        while choice2 == "g":
            if choice2 == "g":
                equipos = sorted(list(diccionario_id.keys()))
                for equipo in equipos:
                    print(equipo)
                print()
                equipo = pedir_equipo(diccionario_id)
                goals_x_min(equipo,diccionario_id)
                choice2 = input("¿Que desea hacer?")
    else:
        print("Hasta pronto!!!")

main()