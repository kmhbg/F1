import ergast_py
import pandas as pd
from datetime import datetime
import sqlite3

e = ergast_py.Ergast()





current_date = datetime.now().strftime('%Y-%m-%d')

db_file = "./database.db"
betters = ["Seb","Oskar","Jonte","Marcus","Filip"]
# Races
def create_races_table():
    """Creates a table holding all races for current year"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute('''
          CREATE TABLE IF NOT EXISTS races
          (season INT, round INT, race_name TEXT,sprint TEXT, race_date DATE)
          ''')
    con.commit()

def create_next_race_table():
    """Creates a table holding all races for current year"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute('''
          CREATE TABLE IF NOT EXISTS next_race
          (last_race INT, next_race INT,updated INT)
          ''')
    con.commit()

def insert_races_to_db(season,round,race_name,sprint,race_date):   
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO races (season, round, race_name, sprint, race_date) VALUES ('{season}','{round}','{race_name}','{sprint}','{race_date}')")
    con.commit()

def update_next_race_in_db(last,next):
    """Updates points to the drivers table, should be run after each race"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f"UPDATE next_race SET last_race = {last}, next_race = {next}")
    con.commit()
# race name races[0].race_name

def get_race_results(round):
    """Getting the results from given race"""
    if not race_status(round):
        race_results = e.season(datetime.now().strftime('%Y')).round(round).get_result()
        first = race_results.results[0].driver.code
        second = race_results.results[1].driver.code
        third = race_results.results[2].driver.code
        insert_result_to_db(round,first,second,third)
        get_next_race()
    else:
        print("Racet är inte slut eller har inte börjat")  
def get_constructor_standings():
    constructor_standings = e.season(datetime.now().strftime('%Y')).get_constructor_standings()
    return constructor_standings

def insert_next_race(last,next,updated=0):
    """Insert bet in for the race in the bet table"""
    create_next_race_table()
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO next_race (last_race,next_race,updated) VALUES ('{last}','{next}','{updated}')")
    con.commit()

def next_race():
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f"SELECT last_race from next_race")
    con.commit()
    last_race = cur.fetchone()[0]
    
    return last_race

def get_next_race():
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f"SELECT last_race from next_race")
    con.commit()
    last_race = cur.fetchone()[0]

    
    race_status = e.season(datetime.now().strftime('%Y')).round(last_race).get_statuses()
    if len(race_status) !=0:
        race_status = e.season(datetime.now().strftime('%Y')).round(last_race+1).get_statuses()
        print(last_race)
        if len(race_status) == 0:
            #print(last_race)
            update_next_race_in_db(last_race+1,last_race+2)
        else:
            pass

    else:
        "Racet har inte börjat än"


def race_status(round):
    """Checks if the date is before or after the racedate"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f"SELECT race_date from races where round={round}")
    con.commit()
    race_date = cur.fetchone()[0]
    if current_date > race_date:
        return False
    elif current_date == race_date:
        return False
    else:
        return True

def get_races():
    """Get all reces for the season"""
    # Get all the races for current year
    races = e.season(datetime.now().strftime('%Y')).get_races()
    create_races_table()
    #datetime.now().strftime('%Y')
    data = {"Säsong": [], "Race": [], "Bana" :[],"Sprint Race": [], "Datum": [] }
    for race in races:        
        sprint = race.sprint
        if sprint is None:
            sprint = "Nej"
        else:
            sprint = "Ja"
        round = race.round_no
        race_name = race.race_name
        season = race.season
        race_date = generate_race_date(race.date.year,race.date.month,race.date.day)
        data["Säsong"].append(season)
        data["Race"].append(round)
        data["Bana"].append(race_name)
        data["Sprint Race"].append(sprint)
        data["Datum"].append(race_date)
        insert_races_to_db(season,round,race_name,sprint,race_date) 
    #df = pd.DataFrame(data)
    #return df

# Results
def create_result_table():
    """Creates a table holding all results for current year"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute('''
          CREATE TABLE IF NOT EXISTS result
          (round INT, first TEXT,second TEXT, third TEXT)
          ''')
    con.commit()

def insert_result_to_db(round,first,second,third):
    create_result_table()
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO result (round,first,second,third) VALUES ('{round}','{first}','{second}','{third}')")
    con.commit()
    
# Drivers
def create_driver_table():
    """Creates a table holding all drivers and standings for current year"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute('''
          CREATE TABLE IF NOT EXISTS drivers
          (code TEXT, name TEXT, points INT, wins INT, standing INT)
          ''')
    con.commit()

def insert_drivers_to_db(code,name,points=0,wins=0,standing=0):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO drivers (code,name,points,wins,standing) VALUES ('{code}','{name}','{points}','{wins}','{standing}')")
    con.commit()

def update_drivers_in_db(code,points,wins,standing):
    """Updates points to the drivers table, should be run after each race"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f"UPDATE drivers SET points = '{points}', wins = '{wins}', standing = '{standing}' WHERE code = '{code}'")
    con.commit()

# Bets
def create_bet_table():
    """Creates a table holding all bets for current year"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute('''
          CREATE TABLE IF NOT EXISTS bets
          (name INT, round INT, first TEXT,second TEXT, third text, points INT)
          ''')
    con.commit()




def insert_bet_to_db(name,round,first="",second="",third="",points=0):
    """Insert bet in for the race in the bet table"""
    create_bet_table()
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO bets (name,round,first,second,third,points) VALUES ('{name}','{round}','{first}','{second}','{third}','{points}')")
    con.commit()

def check_bet(round):

    for better in betters:
        points = 0 
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        cur.execute(f"SELECT first, second, third from result where round={round}")
        con.commit()
        result = cur.fetchall()
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        cur.execute(f"SELECT first, second, third from bets where round={round} and name='{better}'")
        con.commit()
        bets = cur.fetchall()

        if result[0][0] == bets[0][0]:
            points += 1
        if result[0][1] == bets[0][1]:
            points += 1
        if result[0][2] == bets[0][2]:
            points += 1
        print(points)
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        cur.execute(f"UPDATE bets SET points = '{points}' WHERE round = '{round}' and name = '{better}'")
        con.commit()

    




def create_bet(round, better, one, two, three):
    """Createing the bet and checks if the bet is possible based on the result of race_status()"""
    if race_status(round):
        insert_bet_to_db(better, round,one, two,three)
        return "Tack för ditt bett"
    else:
        return "Du är sen eller så har racet redan varit"

# Others
def check_file_in_db(current_year):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    exists = cur.execute(
        f"select exists(select season from races where round = '{current_year}')")
    con.commit()
    if cur.fetchone():
        return True

    else:
        return False

            
def format_date_part(part):
    """Add 0 to numbers between 1-9"""

    if 1 <= part <= 9:
        part = f"0{part}"
        return part
    else:
        return part

def generate_race_date(y,m,d):
    """Format dates from yyyy m d to yyyy-mm-dd format """
    date = f"{y}-{format_date_part(m)}-{format_date_part(d)}"
    return date


        


def get_drivers():
    # Get all drivers for current year
    drivers = e.season(datetime.now().strftime('%Y')).get_drivers()
    create_driver_table()
    for driver in drivers:        
        code = driver.code
        name = f"{driver.given_name} {driver.family_name}"
        insert_drivers_to_db(code,name)


def update_points():
    # Get total standings
    driver_standings = e.season(datetime.now().strftime('%Y')).get_driver_standings()
    for driver in driver_standings[0].driver_standings:
        update_drivers_in_db(driver.driver.code,driver.points,driver.wins,driver.position)

def read_database(table_name):
    con = sqlite3.connect("./database.db")
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", con)
    return df
def bets_with_race_name():
    con = sqlite3.connect("./database.db")
    df = pd.read_sql_query(f"SELECT bets.name AS 'Namn',races.race_name AS 'Bana',bets.first AS '1:a',bets.second AS '2:a',bets.third AS '3:a',bets.points FROM bets LEFT JOIN races on bets.round=races.round", con)
    return df

def get_driver_list():
    con = sqlite3.connect("./database.db")
    df = pd.read_sql_query(f"SELECT code FROM drivers", con)
    return df

def get_race_list():
    con = sqlite3.connect("./database.db")
    df = pd.read_sql_query(f"SELECT round FROM races", con)
    return df
def remove_bet_from_db(round,name):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f"delete from bets where round={round} and name='{name}'")
    con.commit()
    return f"Better för {name} och race {round} är borttaget"

def get_race_name():
    round = next_race()
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f"SELECT race_name FROM races WHERE round='{round}'")
    con.commit()
    race_name = cur.fetchone()[0]
    return race_name


def sum_bet_points():
    con = sqlite3.connect("./database.db")
    df = pd.read_sql_query(f"select name,sum(points) as points from bets group by name", con)
    return df

def check_bets(name,first,second,third):
    race_name = get_race_name()
    unique_bet = 0
    round = next_race()
    con = sqlite3.connect("./database.db")
    df2 = pd.read_sql_query(f"select name from bets where round={round} and name = '{name}'", con)
    if first == second == third:
        return "Du har valt samma på alla positioner"
    elif not df2['name'].empty:
        
        return f"Du har redan lagt ditt bet för {race_name}"
    else:
        for better in betters:
            
            df = pd.read_sql_query(f"select first, second, third from bets where round={round} and name = '{better}'", con)
            if df.empty:
                create_bet(round, name, first, second, third)
                return "Tack för ditt bett!"
            elif first == df['first'].iloc[0] and second == df['second'].iloc[0] and third == df['third'].iloc[0]:
                pass
            else:
                unique_bet += 1
    if unique_bet != 3:
        return "Sorry ditt bet finns resan"
    else:
        create_bet(round, name, first, second, third)
        return "Tack för ditt bett!"

def run():
    #get_drivers()
    #print(get_driver_list().values.tolist())
    #get_races()
    #update_points()
    #create_bet(1,"Seb","VER","LEC","HUL")
    #create_bet(1,"Filip","VER","PER","SAI")
    #create_bet(1,"Jonte","VER","PER","ALO")
    #create_bet(1,"Oskar","VER","PER","LEC")
    #create_bet(1,"Marcus","VER","LEC","ALO")
    #get_race_results(2)
    #check_bet(1)
    #is_race_over()
    #get_next_race()
    #insert_next_race(1,2)
    #print(check_bets("Seb","VER","PER","ALO"))
    print(get_constructor_standings())
    print(get_next_race())
    print(get_race_name())
    print("hej")

if __name__ == "__main__":
    run()