import csv
from passlib.hash import ldap_pbkdf2_sha256
from matplotlib import pyplot as plt

def generar_encripcion(password) -> str:
    cryppass = ldap_pbkdf2_sha256.hash(password)
    print(cryppass)
    return cryppass
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
    cryppass = generar_encripcion(input("Ingrese una contraseña: "))
    while cryppass == ""  or cryppass not in search_password:
        cryppass = generar_encripcion(input("La contraseña no es correcta, por favor, vuelva a ingresar la contraseña: "))
    print(f"Bienvenido {user}!!!")
    return user
def crear_credenciales(user_dict) -> None:
    #Acá va la linea para abrir el archivo, leerlo y verificar la existencia de ciertos datos.
    id = input("Ingrese su correo electrónico: ")
    #while id in users.info.csv:
        #id = input("Este correo ya se encuentra asociado a una cuenta existente. Por favor, ingrese un nuevo correo: ")
    user = input("Ingrese un nuevo de usuario: ")
    #while user in users.info.csv:
        #id = input("Este usuario ya se encuentra asociado a una cuenta existente. Por favor, ingrese un nuevo usuario: ")
    password = input("Ingrese una contraseña: ")
    while password == "" or len(password) < 4:
        password = input("La contraseña debe ser de un mínimo de 4 caracteres, por favor, ingrese una nueva contraseña: ")
    cryppass = generar_encripcion(password)
    moneyspend = 0
    lastgamble = 0
    balance = 0
    new_user = (f"{id},{user},{cryppass},{moneyspend},{lastgamble},{balance}")#En esta linea irian incluidas todas las variables que se van a escribir en el archivo.csv, ordenadas en un string compatible con el csv.
    #En esta linea se abre el comando writeline para dejar registro de los datos de la cuenta creada.
    #Finalmente en esta linea se cierra el archivo.
def mostrar_graficos() -> None:
    equipo = "equipo1"
    x1 = [0,10,20,30,40,50,60,70,80,90] #Minutos jugados de un partido x
    y1 = [0,0,0,1,1,1,2,2,2,2] #Número de goles por cada minuto graficado.
    plt.step(x1, y1, label=equipo, linewidth=1, color="red")
    plt.title(f"Goles por minuto de {equipo}.")
    plt.xlabel("Minutos jugados.")
    plt.ylabel("Goles realizados.")
    plt.rcParams['toolbar'] = 'None'
    plt.legend()
    plt.show()
    print()
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
    choice = input("\nDigite:\n'i' si desea ingresar a una cuenta existente,\n'r' si desea registrar una cuenta nueva,\n'Enter' si desea salir. ")
    while choice != "" and choice is not str:
        choice.lower()
        if choice == "i":
            print("ingreso a cuenta existente.\n")
            user_online = buscar_credenciales(users_dict)
        if choice == "r":
            print("Registro de cuenta nueva.\n")
            crear_credenciales(users_dict)
        else:
            break
main()