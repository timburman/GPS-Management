import mysql.connector as ms
import folium
import webbrowser

# Connecting to the mysql database using mysqlconnector
def sql_connect():
    global mycon
    global mycus
    global mycus_1
    mycon = ms.connect(host = 'localhost', user = 'root', passwd = '', database = 'gps_managment')
    mycus = mycon.cursor(buffered=True)
    mycus_1 = mycon.cursor(buffered=True)

# Used sql to create a login portal.. 
def login():
    username = 'select username, password from user_login;'
    mycus.execute(username)
    imp_username = input('Enter your username to login: ')
    for (username, password) in mycus:
        if imp_username in username:
            imp_password = input('Enter your password: ')
            if imp_password in password:
                print('Login Succesfull')
                choice()
            else:
                print('Password incorrect, Try again')
                login()
        else:
            print('Username You entered is worng, try again')
            login()


def choice():
    cho = int(input('Enter your choice,\n 1. Display the map of the location\n 2. Update the existing Locations\n 3. Add a new Location \n 4. Delete a Location\n 5. To quit\n : '))
    if cho in (1,2,3,4,5):
        if cho == 1:
            location()
        elif cho == 2:
            update()
        elif cho == 3:
            insert()
        elif cho == 4:
            deletion()
        else:
            exit

# ====================First option=======================#
# This is to get the location from the database.
def location():
    global loc
    sql_loc = 'select place from gps_coordinates;'
    mycus.execute(sql_loc)
    loc = input('Enter the location of where you want to go: ')
    for place in mycus:
        if loc.capitalize() in place:
            location_coordinate()


# After the location is in our database this funtion will be executed.. this open map of the location which you entered
def location_coordinate():
    sql_coo = (f"select coordinate_1, coordinate_2 from gps_coordinates where place='{loc.capitalize()}'")
    mycus_1.execute(sql_coo)
    for (coordinate_1, coordinate_2) in mycus_1:
        folium.Map(location = [coordinate_1, coordinate_2]).save(f'{loc}.html')
        webbrowser.open(f'{loc}.html')
        choice()
# ============x=========First Option=========x==========#


# ======================Second Option===================#
# Update the existing entries
def update():
    up = int(input('Enter your choice,\n 1. Update Place name\n 2. Update place coordinates\n '))
    if up in (1,2):
        if up == 1:
            plc = input('Enter place name that you wanna change: ')
            plc_new = input('Enter new name of that place: ')
            try:
                query = (f"update gps_coordinates set place='{plc_new.capitalize()}' where place='{plc.capitalize()}'")
                mycus.execute(query)
                mycon.commit()
                print('Entry Updated')
                choice()
            except:
                print('The place you entered does not exist.')
                choice()
        else:
            plc = input('Enter place name that you wanna change: ')
            coo_1 = float(input('Enter the first coordinate: '))
            coo_2 = float(input('Enter the Second coordinate: '))
            try:
                query = (f"update gps_coordinates set coordinate_1={coo_1}, coordinate_2={coo_2} where place='{plc.capitalize()}'")
                mycus.execute(query)
                mycon.commit()
                print('Entry Updated')
                choice()
            except:
                print('The place you entered does not exist.')
                choice()


# ============x========Second Option=========x==========#



# =====================Third Option=====================#
# The function to insert a new location into the database
def insert():
    #Inputs
    inp_loc = input('Enter the place/location: ')
    # Code
    inp_coo1 = float(input('Enter the first coordinate: '))
    inp_coo2 = float(input('Enter the second coordinate: '))
    try:
        query = (f"insert into gps_coordinates values('{inp_loc.capitalize()}',{inp_coo1},{inp_coo2})")
        mycus.execute(query)
        mycon.commit()
        print('Location Recored')
        choice()
    except:
        print('This location already exists in database')
        choice()
# ==========x==========Third Option=============x=======#



# =====================Fourth Option====================#
# Delete a entry
def deletion():
    plc = input('Enter the name of the place: ')
    try:
        query = (f"delete from gps_coordinates where place='{plc}'")
        mycus.execute(query)
        mycon.commit()
        choice()
    except:
        print('The place you entered does not exist')
        choice()

# ==========x==========Fourth Option===========x========#


if __name__ == "__main__":
    sql_connect()
    login()