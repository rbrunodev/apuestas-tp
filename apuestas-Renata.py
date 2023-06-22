
import random
import http.client
import json
import os 
import csv

def limpiar_consola()->None:
    '''Limpia la consola del sistema.'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pago_apuestas(fixture_id:int, team_local:str)->list:
    '''Recibe el fixture id y el equipo que es local, consulta en la api las predicciones de ese partido y devuelve, 
    segun esos datos, cuanto se le pagara a cada equipo L/V'''
    prediction = api_predictions_por_fixture(fixture_id)

    winner_name : str = prediction['winner_name']

    number = random.randint(1, 4)

    pay_local = number
    pay_visitor = number

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

    fixtures = {}

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

def leer_archivo_usuarios()->dict:
    '''Lee el archivo usuarios y devuelve un diccionario con los datos.'''
    archivo = 'users_info.csv'
    usuarios = {}
    with open(archivo, 'r') as archivo_aux:
        texto = csv.reader(archivo_aux)
        next(texto)
        for linea in texto:
            email = linea[0]
            valores = linea[1:]
            usuarios[email] = valores

    return usuarios

def dinero_disponible(usuario:str)->int:
    '''Recibe el id del usuario (mail) y devuelve el dinero disponible que tiene ese usuario'''
    usuarios = leer_archivo_usuarios()
    datos_usuario = usuarios[usuario]

    return datos_usuario[4]

def simular_resultado()->str:
    '''Devuelve una inicial que simula un resultado de partido.'''
    dado = random(1, 3)

    if(dado == 1):
        return "L"

    if(dado == 2):
        return "E"
    
    if(dado == 3):
        return "V"
    
def cargar_dinero_disponible(usuario: str, dinero:int) ->None:
    '''Recibe el id del usuario(mail) y el dinero a cargar.
    Modifica el archivo usuarios para actualizar el monto disponible de ese usuario'''
    archivo_csv = 'users_info.csv'
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
    archivo_csv = 'users_info.csv'
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

def apostar_partido(codigo:int, fixtures:dict, usuario: str)->None:
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

    dinero = dinero_disponible(usuario)

    if(dinero == 0):
        print("Usted no dispone de dinero para apostar.")
        print("Finalizo el programa")
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
    else: 
        descontar_dinero(usuario, monto)
        guardar_transacciones(usuario, - monto, 'Pierde')
        print("Hemos descontado de su dinero disponible lo apostado.")
        return
    
def listado_fixture(equipo: str, fixtures:dict, equipos:dict)->None:
    '''Recibe el nombre de un equipo y devuelve el listado de partidos que debe jugar en el torneo'''
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
    equipos = {
        "RIVER PLATE": 435, "TALLERES": 456, "SAN LORENZO": 460, "ESTUDIANTES LP": 450, "ROSARIO CENTRAL": 437,
        "DEFENSA Y JUSTICIA": 442, "LANUS": 446, "BELGRANO": 440, "ARGENTINOS JUNIORS": 458, "GODOY CRUZ": 439,
        "BOCA JUNIORS": 451, "NEWELLS OLD BOYS": 457, "PLATENSE": 1064, "SARMIENTO": 474,
        "GIMNASIA LP": 434, "CENTRAL CORDOBA DE SANTIAGO DEL ESTERO": 1065, "COLON": 448, "RACING CLUB": 436,
        "BARRACAS CENTRAL": 2432, "TIGRE": 452, "INSTITUTO": 478, "INDEPENDIENTE": 453, "ATLETICO TUCUMAN": 455,
        "UNION DE SANTA FE": 441, "VELEZ SARFIELD": 438, "HURACAN": 445, "BANFIELD": 449, "ARSENAL DE SARANDI": 459
    }
    usuario_login = "pruba@mail.com"
    fixtures = {}
    equipo = input("Ingrese el nombre del equipo para conocer el listado del fixture: ")
    while equipo.upper() not in equipos:
        print("Debe ingresar el nombre de un equipo de la Liga Profesional 2023")
        equipo = input("Ingrese el nombre del equipo: ")

    listado_fixture(equipo.upper(), fixtures, equipos)

    while len(fixtures) > 0: 
        codigo = elegir_partido(fixtures)
        apostar_partido(codigo, fixtures, usuario_login)
    
    print("No hay partidos para mostrarle.")
main()

