from passlib.hash import ldap_pbkdf2_sha256
from matplotlib import pyplot as plt

def generar_encripcion(password) -> str:
    cryppass = ldap_pbkdf2_sha256.hash(password)
    print(cryppass)
    return cryppass
def buscar_credenciales(user,password) -> None:
    #Acá va la linea para abrir el archivo, leerlo y verificar la existencia de ciertos datos.
    user = input("Ingrese un nuevo de usuario: ")
    #while user not in users.info.csv:
        #id = input("Este usuario ya se encuentra asociado a una cuenta existente. Por favor, ingrese un nuevo usuario: ")
    password = input("Ingrese una contraseña: ")
    cryppass = generar_encripcion(password)
    while password == "" or len(password) < 4: #or cryppass not in usersinfo:
        password = input("La contraseña no es correcta, por favor, vuelva a ingresar la contraseña: ")
    print(f"Bienvenido {user}!!!")
def crear_credenciales() -> None:
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
    print("\nBienvenido a Jugarsela!!!")
    choice = input("\nDigite:\n'i' si desea ingresar a una cuenta existente,\n'r' si desea registrar una cuenta nueva,\n'Enter' si desea salir. ")
    while choice != "" and choice is str:
        choice.lower()
        if choice == "i":
            print("ingreso a cuenta existente.\n")
            user = input("Ingrese su usuario: ")
            password = input("Ingrese su contraseña: ")
            buscar_credenciales(user,password)
        if choice == "r":
            print("Registro de cuenta nueva.\n")
            crear_credenciales()
        else:
            break

main()