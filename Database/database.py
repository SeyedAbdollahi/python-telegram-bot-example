import json
import datetime
import psycopg2
import jdatetime

database_file_location = './Database/database.json'

# read config.json file
def read_config():
    with open('config.json') as jsonFile:
        return json.load(jsonFile)['database']

# get config data
config = read_config()

# connect to postgresql database
def connect():
    # This con for postgresql online , if you try local postgresql this link can help you:
    # https://stackoverflow.com/questions/13784340/how-to-run-postgres-locally
    con = psycopg2.connect(host=config['host'], database=config['database'], user=config['user'], password=config['password'])
    return con

# add log to logs table postqresql database
def insert_log(log):
    table_name = 'logs'
    try:
        con = connect()
        cur = con.cursor()
        query = ("INSERT INTO %s (date, log) VALUES (\'%s\', \'%s\')" % (table_name, jdatetime.datetime.now(), log))
        cur.execute(query)
        con.commit()
        cur.close()
        con.close()
    except(Exception) as error:
        print('error in insert_log to database:', error)

# get all logs from postgresql database
def get_logs():
    table_name = 'logs'
    con = connect()
    cur = con.cursor()
    query = ("SELECT * FROM %s" % table_name)
    cur.execute(query)
    log = str()
    for row in cur.fetchall():
        log += '[' + str(row[0]) + '] ' + str(row[1]) + ': ' + row[2] + '\n'
    cur.close()
    con.close()
    return log

# delete all logs from postgresql database
def delete_logs():
    table_name = 'logs'
    try:
        con = connect()
        cur = con.cursor()
        query = ("DELETE FROM %s" % table_name)
        cur.execute(query)
        con.commit()
        cur.close()
        con.close()
    except(Exception) as error:
        print('error in delete_logs from database:', error)


# update specific script database
def update_data(script, updated_data):
    data = read_all()
    with open(database_file_location, 'w') as outFile:
        data['scripts'][script]['data'] = updated_data
        data['scripts'][script]['time'] = datetime.datetime.now().strftime('%Y %m %d %H %M').split()
        json.dump(data, outFile)

# read all database
def read_all():
    with open(database_file_location, 'r') as jsonFile:
        return json.load(jsonFile)

# read specific script from database
def read_data(script):
    with open(database_file_location, 'r') as jsonFile:
        return json.load(jsonFile)['scripts'][script]['data']

# get last time script updated data
def get_last_time_updated(script):
    with open(database_file_location, 'r') as jsonFile:
        return json.load(jsonFile)['scripts'][script]['time']

# need to update or no need!
def time_update(script):
    last_time_updated = get_last_time_updated(script)
    time_now = datetime.datetime.now().strftime('%Y %m %d %H %M').split()

    # check Year
    if int(last_time_updated[0]) < int(time_now[0]):
        return True
    # check Month
    elif int(last_time_updated[1]) < int(time_now[1]):
        return True
    # check day
    elif int(last_time_updated[2]) < int(time_now[2]):
        return True
    # check hour
    elif int(last_time_updated[3]) < int(time_now[3]):
        return True
    # check minute
    elif int(last_time_updated[4]) < int(time_now[4]):
        if int(time_now[4]) - int(last_time_updated[4]) > 10:
            return True
    # return True: need to update
    # return False: no need to update
    return False

