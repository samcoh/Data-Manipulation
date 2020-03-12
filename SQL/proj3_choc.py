import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'
def init_db(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    statement = '''
        DROP TABLE IF EXISTS 'Bars';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Bars' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Company' TEXT NOT NULL,
            'SpecificBeanBarName' TEXT NOT NULL,
            'REF' TEXT NOT NULL,
            'ReviewDate' TEXT,
            'CocoaPercent' REAL NOT NULL,
            'CompanyLocation' TEXT NOT NULL,
            'CompanyLocationId' Integer,
            'Rating' REAL NOT NULL,
            'BeanType' TEXT NOT NULL,
            'BroadBeanOrigin' TEXT NOT NULL,
            'BroadBeanOriginId' Integer
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Countries' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' TEXT NOT NULL,
            'Alpha3' TEXT NOT NULL,
            'EnglishName' TEXT NOT NULL,
            'Region' TEXT NOT NULL,
            'Subregion' REAL NOT NULL,
            'Population' INTEGER NOT NULL,
            'Area' REAL
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()
def insert_flavors_of_cacao_cleaned():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    with open(BARSCSV) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        num = 0
        for row in csvReader:
            num = num + 1
            if num == 1:
                continue
            Company = row[0]
            SpecificBeanBarName = row[1]
            REF = row[2]
            ReviewData = row[3]
            CocoaPercent= (float(row[4][:-1]))/100
            CompanyLocation = row[5]
            CompanyLocationId = ''
            Rating = row[6]
            BeanType = row[7]
            BroadBeanOrigin = row[8]
            BroadBeanOriginId = ''
            insert = (None, Company,SpecificBeanBarName,REF,ReviewData,CocoaPercent,CompanyLocation,CompanyLocationId,Rating,BeanType,BroadBeanOrigin,BroadBeanOriginId)
            statement = 'INSERT INTO Bars '
            statement += 'VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
            cur.execute(statement, insert)
            conn.commit()
        conn.close()

def insert_countries():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    file_name = open(COUNTRIESJSON, 'r')
    json_str = file_name.read()
    data = json.loads(json_str)
    file_name.close()
    for x in data:
        Alpha2 = x["alpha2Code"]
        Alpha3= x["alpha3Code"]
        EnglishName = x["name"]
        Region = x["region"]
        Subregion = x["subregion"]
        Population = x["population"]
        Area = x["area"]
        insert = (None,Alpha2,Alpha3,EnglishName,Region,Subregion,Population,Area)
        statement = 'INSERT INTO Countries '
        statement += 'VALUES (?,?,?,?,?,?,?,?)'
        cur.execute(statement, insert)
        conn.commit()
    conn.close()

def update_company_location_id():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Countries.ID,Bars.Id
        FROM Countries
        JOIN Bars
        ON Countries.EnglishName = Bars.CompanyLocation
    '''
    ids = cur.execute(statement).fetchall()
    for x in ids:
        country_id = x[0]
        bar_id = x[1]
        update = (country_id,bar_id)
        statement = 'UPDATE Bars '
        statement += 'SET CompanyLocationId=? '
        statement += 'WHERE Id=?'
        cur.execute(statement,update)
        conn.commit()
    conn.close()

def update_BroadBeanOriginId():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Countries.ID,Bars.Id
        FROM Countries
        JOIN Bars
        ON Countries.EnglishName = Bars.BroadBeanOrigin
    '''
    ids = cur.execute(statement).fetchall()
    for x in ids:
        country_id = x[0]
        bar_id = x[1]
        update = (country_id,bar_id)
        statement = 'UPDATE Bars '
        statement += 'SET BroadBeanOriginId=? '
        statement += 'WHERE Id=?'
        cur.execute(statement,update)
        conn.commit()
    conn.close()

#sell = company
#source = origin
# Part 2: Implement logic to process user commands
def bars(command):
    split_command = command.split()[1:]
    the_command = {}
    if len(split_command)== 0:
        the_command["name"]="none"
        the_command["sort"]= "Rating"
        the_command["limit"]= ["DESC",10]
        return get_values_for_bars(the_command)

    if "sellcountry" in split_command[0]:
        sell_country = split_command[0]
        list_sell = sell_country.split("=")
        the_command["name"] = list_sell
    elif "sourcecountry" in split_command[0]:
        source_country = split_command[0]
        list_source = source_country.split("=")
        the_command["name"] = list_source
    elif "sellregion" in split_command[0]:
        sell_region = split_command[0]
        list_sell_region = sell_region.split("=")
        the_command["name"] = list_sell_region
    elif "sourceregion" in split_command[0]:
        source_region = split_command[0]
        list_source_region = source_region.split("=")
        the_command["name"] = list_source_region
    else:
        the_command["name"] = "none"
        try:
            if "ratings" == split_command[0]:
                the_command["sort"] = "Rating"
            elif "cocoa" == split_command[0]:
                the_command["sort"] = "CocoaPercent"
            else: #default
                the_command["sort"] = "Rating"
        except:
            the_command["sort"] = "Rating"
        try:

            if "top" in split_command[-1]:
                top = split_command[-1]
                split_top = top.split("=")
                the_command["limit"] = ["DESC",split_top[1]]
            elif "bottom" in split_command[-1]:
                bottom = split_command[-1]
                split_bottom = bottom.split("=")
                the_command["limit"] = ["ASC",split_bottom[1]]
            else:
                default = ["DESC",10]
                the_command["limit"] = default
        except:
            default = ["DESC",10]
            the_command["limit"] = default
        return get_values_for_bars(the_command)
    try:
        if "cocoa" == split_command[1]:
            the_command["sort"] = "CocoaPercent"
        else:
            the_command["sort"] = "Rating"
    except:
        the_command["sort"]= "Rating"
    try:
        if "top" in split_command[-1]:
            top = split_command[-1]
            split_top = top.split("=")
            the_command["limit"] = ["DESC",split_top[1]]
        elif "bottom" in split_command[-1]:
            bottom = split_command[-1]
            split_bottom = bottom.split("=")
            the_command["limit"] = ["ASC",split_bottom[1]]
        else:
            default = ["DESC",10]
            the_command["limit"] = default
    except:
        default = ["DESC",10]
        the_command["limit"] = default
    return get_values_for_bars(the_command)
def get_values_for_bars(dic):
    the_command = dic
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    if the_command["name"] == "none":
        sort = the_command["sort"]
        order = the_command["limit"]
        top_or_bottom= order[0]
        num = str(order[1])
        statement = 'SELECT SpecificBeanBarName, Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
        statement += "FROM Bars "
        statement += "ORDER BY " +sort+" "+top_or_bottom+ " "
        statement += "LIMIT " +num+ ""
        answer = cur.execute(statement)
        # cur.execute(statement)
        # for x in cur:
        #     print(x)
    else:
        first_command = the_command["name"][0]
        area = the_command["name"][1]
        sort = the_command["sort"]
        order = the_command["limit"]
        top_or_bottom = order[0]
        num = str(order[1])
        if "sellcountry" == first_command or "sourcecountry" == first_command:
            if "sellcountry" == first_command:
                place = "CompanyLocation"
            if "sourcecountry" == first_command:
                place = "BroadBeanOrigin"
            insert = (area,num)
            statement = 'SELECT Bars.'+place+ " "
            statement += "FROM Bars "
            statement += "JOIN Countries "
            statement += "ON Countries.Id = Bars." + place + "Id"+" "
            statement += "WHERE Countries.Alpha2 LIKE ? "
            statement += "LIMIT ?"
            cur.execute(statement,insert)
            for x in cur:
                area = x[0]
            insert = (area,num)
            s = 'SELECT SpecificBeanBarName, Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin '
            s += "FROM Bars "
            s += 'WHERE '+place+ " LIKE ? "
            s += "ORDER BY " +sort+" "+top_or_bottom+ " "
            s += "LIMIT ?"
            answer = cur.execute(s,insert)
            # cur.execute(statement,insert)
            # for x in answer:
            #     print(x)
        if "sellregion" == first_command or "sourceregion" == first_command:
            if "sellregion" == first_command:
                place = "Bars.CompanyLocationId"
            if "sourceregion" == first_command:
                place = "Bars.BroadBeanOriginId"
            insert = (area,num)
            statement = 'SELECT Bars.SpecificBeanBarName, Bars.Company, Bars.CompanyLocation, Bars.Rating, Bars.CocoaPercent, Bars.BroadBeanOrigin '
            statement += "FROM Bars "
            statement += 'JOIN Countries '
            statement += 'ON Countries.ID = '+ place + " "
            statement += 'WHERE Countries.Region LIKE ? '
            statement += "ORDER BY " +sort+" "+top_or_bottom+ " "
            statement += "LIMIT ?"
            answer = cur.execute(statement,insert)
            # for x in answer:
            #     print(x)
    data_list = []
    # if sort == "CocoaPercent":
    #     percent = "Yes"
    # else:
    #     percent = "No"
    for x in answer:
        #if percent == "Yes":
        p = int(x[4] * 100)
        data_list.append((x[0],x[1],x[2],x[3],str(p)+"%",x[5]))
        #else:
            #data_list.append(x)
    conn.close()
    if len(data_list) == 0:
        return "None"
    return data_list

def companies(command):
    split_command = command.split()[1:]
    the_command = {}
    if len(split_command)== 0:
        the_command["name"]="none"
        the_command["sort"]= "Rating"
        the_command["limit"]= ["DESC",10]
        return get_values_for_companies(the_command)
    if "country" in split_command[0]:
        sell_country = split_command[0]
        list_sell = sell_country.split("=")
        the_command["name"] = list_sell
    elif "region" in split_command[0]:
        sell_region = split_command[0]
        list_sell_region = sell_region.split("=")
        the_command["name"] = list_sell_region
    else:
        the_command["name"] = "none"
        try:
            if "cocoa" == split_command[0]:
                the_command["sort"] = "CocoaPercent"
            elif "bars_sold" == split_command[0]:
                the_command["sort"] = "bars_sold"
            else: #default
                the_command["sort"] = "Rating"
        except:
            the_command["sort"] = "Rating"
        try:
            if "top" in split_command[-1]:
                top = split_command[-1]
                split_top = top.split("=")
                the_command["limit"] = ["DESC",split_top[1]]
            elif "bottom" in split_command[-1]:
                bottom = split_command[-1]
                split_bottom = bottom.split("=")
                the_command["limit"] = ["ASC",split_bottom[1]]
            else:
                default = ["DESC",10]
                the_command["limit"] = default
        except:
            default = ["DESC",10]
            the_command["limit"] = default
        return get_values_for_companies(the_command)
    try:
        if "cocoa" == split_command[1]:
            the_command["sort"] = "CocoaPercent"
        elif "bars_sold" == split_command[1]:
            the_command["sort"] = "bars_sold"
        else:
            the_command["sort"] = "Rating"
    except:
        the_command["sort"] = "Rating"
    try:

        if "top" in split_command[-1]:
            top = split_command[-1]
            split_top = top.split("=")
            the_command["limit"] = ["DESC",split_top[1]]
        elif "bottom" in split_command[-1]:
            bottom = split_command[-1]
            split_bottom = bottom.split("=")
            the_command["limit"] = ["ASC",split_bottom[1]]
        else:
            default = ["DESC",10]
            the_command["limit"] = default
    except:
        default = ["DESC",10]
        the_command["limit"] = default
    return get_values_for_companies(the_command)
def get_values_for_companies(dic):
    percent = "No"
    the_command = dic
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    if the_command["name"] == "none":
        sort = the_command["sort"]
        if sort == "bars_sold":
            sort = 'COUNT(*)'
        elif sort == "CocoaPercent":
            sort = 'AVG(CocoaPercent)'
            percent = "Yes"
        else:
            sort = 'AVG(Rating)'
        order = the_command["limit"]
        top_or_bottom= order[0]
        num = str(order[1])
        statement = 'SELECT Company,CompanyLocation,'+sort+' '
        statement += "FROM Bars "
        statement += 'GROUP BY Company '
        statement += 'HAVING COUNT(*) > 4 '
        statement += "ORDER BY " +sort+" "+top_or_bottom+ " "
        statement += "LIMIT " +num+ ""
        answer = cur.execute(statement)
        # for x in answer:
        #     print(x)
    elif "country" in the_command["name"]:
        country = the_command["name"][1]
        sort = the_command["sort"]
        if sort == "bars_sold":
            sort = 'COUNT(*)'
        elif sort == "CocoaPercent":
            sort = 'AVG(CocoaPercent)'
            percent = "Yes"
        else:
            sort = 'AVG(Rating)'
        order = the_command["limit"]
        top_or_bottom = order[0]
        num = str(order[1])
        insert = (country,num)
        statement = 'SELECT Bars.CompanyLocation '
        statement += "FROM Bars "
        statement += "JOIN Countries "
        statement += "ON Countries.Id = Bars.CompanyLocationId "
        statement += "WHERE Countries.Alpha2 LIKE ? "
        statement += "LIMIT ?"
        cur.execute(statement,insert)
        for x in cur:
            country = x[0]
        insert=(country,num)
        statement = 'SELECT Company,CompanyLocation,'+sort+' '
        statement += "FROM Bars "
        statement += "WHERE CompanyLocation LIKE ? "
        statement += 'GROUP BY Company '
        statement += 'HAVING COUNT(*) > 4 '
        statement += "ORDER BY " +sort+" "+top_or_bottom+ " "
        statement += "LIMIT ?"
        answer = cur.execute(statement,insert)
        # for x in answer:
        #     print(x)
    elif "region" in the_command["name"]:
        region = the_command["name"][1]
        sort = the_command["sort"]
        if sort == "bars_sold":
            sort = 'COUNT(*)'
        elif sort == "CocoaPercent":
            sort = 'AVG(Bars.CocoaPercent)'
            percent = "Yes"
        else:
            sort = 'AVG(Bars.Rating)'
        order = the_command["limit"]
        top_or_bottom = order[0]
        num = str(order[1])
        insert=(region,num)
        statement = 'SELECT Bars.Company,Bars.CompanyLocation,'+sort+" "
        statement += "FROM Bars "
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = Bars.CompanyLocationId '
        statement += 'WHERE Countries.Region LIKE ? '
        statement += 'GROUP BY Bars.Company '
        statement += 'HAVING COUNT(*) > 4 '
        statement += "ORDER BY " +sort+" "+top_or_bottom+ " "
        statement += "LIMIT ?"
        answer = cur.execute(statement,insert)
        # for x in answer:
        #     print(x)
    data_list = []
    for x in answer:
        if percent == "Yes":
            p = int(x[2] * 100)
            data_list.append((x[0],x[1],str(p)+"%"))
        else:
            data_list.append(x)

    conn.close()
    if len(data_list) == 0:
        return "None"
    return data_list

def countries(command):
    split_command = command.split()[1:]
    the_command = {}
    if len(split_command)== 0:
        the_command["name"]="none"
        the_command["select_countries"]= "sellers"
        the_command["sort"]= "Rating"
        the_command["limit"]= ["DESC",10]
        return get_values_for_countries(the_command)
    if "region" in split_command[0]:
        sell_country = split_command[0]
        list_sell = sell_country.split("=")
        the_command["name"] = list_sell
    else:
        the_command["name"] = "none"
        if "sources" == split_command[0]:
            the_command["select_countries"]= "sources"
        elif "sellers" == split_command[0]:
            the_command["select_countries"]= "sellers"
        else: #no sellers or sources in command
            the_command["select_countries"]= "sellers"
            if "cocoa" == split_command[0]:
                the_command["sort"] = "CocoaPercent"
            elif "bars_sold" == split_command[0]:
                the_command["sort"] = "bars_sold"
            elif "ratings" == split_command[0]:
                the_command["sort"] = "Rating"
            else:
                the_command["sort"] = "Rating"
                if "top" in split_command[0]:
                    top = split_command[0]
                    split_top = top.split("=")
                    the_command["limit"] = ["DESC",split_top[1]]
                elif "bottom" in split_command[0]:
                    bottom = split_command[0]
                    split_bottom = bottom.split("=")
                    the_command["limit"] = ["ASC",split_bottom[1]]
                else:
                    default = ["DESC",10]
                    the_command["limit"] = default
                return get_values_for_countries(the_command)
            if "top" in split_command[-1]:
                top = split_command[-1]
                split_top = top.split("=")
                the_command["limit"] = ["DESC",split_top[1]]
            elif "bottom" in split_command[-1]:
                bottom = split_command[-1]
                split_bottom = bottom.split("=")
                the_command["limit"] = ["ASC",split_bottom[1]]
            else:
                default = ["DESC",10]
                the_command["limit"] = default
            return get_values_for_countries(the_command)
        #if the length of split command is 1 then just set rest of possible commands to default
        #because they will not be in the split command
        if len(split_command) == 1:
            the_command["sort"] = "Rating"
            default = ["DESC",10]
            the_command["limit"] = default
            return get_values_for_countries(the_command)
        #if the length is greater then 1 then keep searching for the key words in command entered
        if "cocoa" == split_command[1]:
            the_command["sort"] = "CocoaPercent"
        elif "bars_sold" == split_command[1]:
            the_command["sort"] = "bars_sold"
        else: #default
            the_command["sort"] = "Rating"
        if "top" in split_command[-1]:
            top = split_command[-1]
            split_top = top.split("=")
            the_command["limit"] = ["DESC",split_top[1]]
        elif "bottom" in split_command[-1]:
            bottom = split_command[-1]
            split_bottom = bottom.split("=")
            the_command["limit"] = ["ASC",split_bottom[1]]
        else:
            default = ["DESC",10]
            the_command["limit"] = default
        return get_values_for_countries(the_command)
    if len(split_command) == 1:
        the_command["select_countries"] = "sellers"
        the_command["sort"] = "Rating"
        default = ["DESC",10]
        the_command["limit"] = default
        return get_values_for_countries(the_command)
    if "sources" == split_command[1]:
        the_command["select_countries"]= "sources"
    elif "sellers" == split_command[1]: #default
        the_command["select_countries"]= "sellers"
    else:
        the_command["select_countries"]= "sellers"
        if "cocoa" == split_command[1]:
            the_command["sort"] = "CocoaPercent"
        elif "bars_sold" == split_command[1]:
            the_command["sort"] = "bars_sold"
        else: #default
            the_command["sort"] = "Rating"
        if "top" in split_command[-1]:
            top = split_command[-1]
            split_top = top.split("=")
            the_command["limit"] = ["DESC",split_top[1]]
        elif "bottom" in split_command[-1]:
            bottom = split_command[-1]
            split_bottom = bottom.split("=")
            the_command["limit"] = ["ASC",split_bottom[1]]
        else:
            default = ["DESC",10]
            the_command["limit"] = default
        return get_values_for_countries(the_command)
    if "cocoa" == split_command[2]:
        the_command["sort"] = "CocoaPercent"
    elif "bars_sold" == split_command[2]:
        the_command["sort"] = "bars_sold"
    else: #default
        the_command["sort"] = "Rating"
    if "top" in split_command[-1]:
        top = split_command[-1]
        split_top = top.split("=")
        the_command["limit"] = ["DESC",split_top[1]]
    elif "bottom" in split_command[-1]:
        bottom = split_command[-1]
        split_bottom = bottom.split("=")
        the_command["limit"] = ["ASC",split_bottom[1]]
    else:
        default = ["DESC",10]
        the_command["limit"] = default
    return get_values_for_countries(the_command)
def get_values_for_countries(dic):
    percent = "No"
    the_command = dic
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    if the_command["name"] == "none":
        sort = the_command["sort"]
        sell_or_source = the_command["select_countries"]
        order = the_command["limit"]
        top_or_bottom= order[0]
        num = str(order[1])
        if sort == "bars_sold":
            sort = 'COUNT(*)'
        elif sort == "CocoaPercent":
            sort = 'AVG(Bars.CocoaPercent)'
            percent = "Yes"
        else:
            sort = 'AVG(Bars.Rating)'
        if sell_or_source == "sellers":
            #select = 'SELECT CompanyLocation,Company,'+sort+' '
            select = 'SELECT Bars.CompanyLocation,Countries.Region,'+sort+" "
            id_ = "Bars.CompanyLocation"
        else:
            #select = 'SELECT BroadBeanOrigin,BroadBeanOriginCountry,'+sort+' '
            select = 'SELECT Bars.BroadBeanOrigin, Countries.Region,'+sort+' '
            id_ = "Bars.BroadBeanOrigin"
        statement = select
        statement += "FROM Bars "
        statement += "JOIN Countries "
        statement += "ON Countries.Id =  "+ id_ + "Id "
        statement += 'GROUP BY '+ id_ + " "
        statement += 'HAVING COUNT(*) > 4 '
        statement += "ORDER BY " + sort +" "+ top_or_bottom + " "
        statement += "LIMIT " + num + ""
        answer = cur.execute(statement)

    elif "region" in the_command["name"]:
        region = the_command["name"][1]
        sort = the_command["sort"]
        sell_or_source = the_command["select_countries"]
        order = the_command["limit"]
        top_or_bottom= order[0]
        num = str(order[1])
        if sort == "bars_sold":
            sort = 'COUNT(*)'
        elif sort == "CocoaPercent":
            sort = 'AVG(Bars.CocoaPercent)'
            percent = "Yes"
        else:
            sort = 'AVG(Bars.Rating)'
        if sell_or_source == "sellers":
            select = 'SELECT Bars.CompanyLocation,Countries.Region,'+sort+" "
            id_ = "Bars.CompanyLocation"
        else:
            select = 'SELECT Bars.BroadBeanOrigin, Countries.Region,'+sort+' '
            id_ = "Bars.BroadBeanOrigin"

        insert = (region,num)
        statement = select
        statement += "FROM Bars "
        statement += 'JOIN Countries '
        statement += 'ON Countries.Id = '+id_ + "Id "
        statement += 'GROUP BY '+ id_ + " "
        statement += 'HAVING COUNT(*) > 4 '
        statement += 'AND Countries.Region LIKE ? '
        statement += "ORDER BY " +sort+" "+top_or_bottom+ " "
        statement += "LIMIT ?"
        answer = cur.execute(statement,insert)
    data_list = []
    for x in answer:
        if percent == "Yes":
            p = int(x[2] * 100)
            data_list.append((x[0],x[1],str(p)+"%"))
        else:
            data_list.append(x)
    conn.close()
    if len(data_list) == 0:
        return "None"
    return data_list

def regions(command):
    split_command = command.split()[1:]
    the_command = {}
    if len(split_command)== 0:
        the_command["select_countries"]= "sellers"
        the_command["sort"]= "Rating"
        the_command["limit"]= ["DESC",10]
        return get_values_for_regions(the_command)
    if split_command[0] == "sellers":
        the_command["select_countries"] = "sellers"
    elif split_command[0] == "sources":
        the_command["select_countries"] = "sources"
    else:
        the_command["select_countries"] = "sellers"
        if "cocoa" == split_command[0]:
            the_command["sort"] = "CocoaPercent"
        elif "bars_sold" == split_command[0]:
            the_command["sort"] = "bars_sold"
        elif "ratings" == split_command[0]:
            the_command["sort"] = "Rating"
        else: #default
            the_command["sort"] = "Rating"
            if "top" in split_command[0]:
                top = split_command[0]
                split_top = top.split("=")
                the_command["limit"] = ["DESC",split_top[1]]
            elif "bottom" in split_command[0]:
                bottom = split_command[0]
                split_bottom = bottom.split("=")
                the_command["limit"] = ["ASC",split_bottom[1]]
            else:
                default = ["DESC",10]
                the_command["limit"] = default
            return get_values_for_regions(the_command)
        if "top" in split_command[-1]:
            top = split_command[-1]
            split_top = top.split("=")
            the_command["limit"] = ["DESC",split_top[1]]
        elif "bottom" in split_command[-1]:
            bottom = split_command[-1]
            split_bottom = bottom.split("=")
            the_command["limit"] = ["ASC",split_bottom[1]]
        else:
            default = ["DESC",10]
            the_command["limit"] = default
        return get_values_for_regions(the_command)
    if len(split_command) == 1:
        the_command["sort"] = "Rating"
        default = ["DESC",10]
        the_command["limit"] = default
        return get_values_for_regions(the_command)
    if "cocoa" == split_command[1]:
        the_command["sort"] = "CocoaPercent"
    elif "bars_sold" == split_command[1]:
        the_command["sort"] = "bars_sold"
    else: #default
        the_command["sort"] = "Rating"
    if "top" in split_command[-1]:
        top = split_command[-1]
        split_top = top.split("=")
        the_command["limit"] = ["DESC",split_top[1]]
    elif "bottom" in split_command[-1]:
        bottom = split_command[-1]
        split_bottom = bottom.split("=")
        the_command["limit"] = ["ASC",split_bottom[1]]
    else:
        default = ["DESC",10]
        the_command["limit"] = default
    return get_values_for_regions(the_command)
def get_values_for_regions(dic):
    percent = "No"
    the_command = dic
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    sort = the_command["sort"]
    sell_or_source = the_command["select_countries"]
    order = the_command["limit"]
    top_or_bottom= order[0]
    num = str(order[1])
    if sell_or_source == "sources":
        sell_or_source = "Bars.BroadBeanOriginId"
    else:
        sell_or_source = "Bars.CompanyLocationId"
    if sort == "bars_sold":
        sort = 'COUNT(*)'
        select = "SELECT Countries.Region, COUNT(*) "
    elif sort == "CocoaPercent":
        percent = "Yes"
        sort = "AVG(Bars.CocoaPercent)"
        select = "SELECT Countries.Region,AVG(Bars.CocoaPercent) "
    else:
        sort = "AVG(Bars.Rating)"
        select = "SELECT Countries.Region,AVG(Bars.Rating) "
    statement = select
    statement += "FROM Bars "
    statement += "JOIN Countries "
    statement += "ON Countries.Id = " +sell_or_source+ " "
    statement += "GROUP BY Countries.Region "
    statement += "HAVING COUNT(*) > 4 "
    statement += "ORDER BY "+sort+ " "+ top_or_bottom + " "
    statement += "LIMIT "+ num + ""
    answer = cur.execute(statement)
    data_list = []
    for x in answer:
        if percent == "Yes":
            p = int(x[1] * 100)
            data_list.append((x[0],str(p)+"%"))
        else:
            data_list.append(x)
    conn.close()
    if len(data_list) == 0:
        return "None"
    return data_list

def process_command(command):
    split_command = command.split()
    if split_command[0] == "bars":
        data = bars(command)
        return data
    if split_command[0] == "companies":
        data = companies(command)
        return data
    if split_command[0] == "countries":
        data = countries(command)
        return data
    if split_command[0]=="regions":
        data = regions(command)
        return data
    #return []
def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = input('Enter a command: ')
    while response != 'exit':
        if response == 'help':
            print(help_text)
            response = input('Enter a command: ')
            continue
        num = 0
        equal = "no"
        if "=" in response:
            for x in response:
                if x == "=":
                    try:
                        if response[num+1] == " " and response[num-1] == " " :
                            equal = "yes"
                            print("Please do not put spaces before or after '='")
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                quit()
                            break
                            # split_response = response.split(" = ")
                            # response = "=".join(split_response)
                        elif response[num+1] == " ":
                            equal  = "yes"
                            print("Please do not put spaces before or after '='")
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                quit()
                            break
                        elif response[num-1] == " ":
                            equal = "yes"
                            print("Please do not put spaces before or after '='")
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                quit()
                            break
                    except:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            quit()
                num = num + 1
            if equal == "yes":
                continue
        split_response = response.split()
        if len(split_response) == 0:
            response = input("Please enter a valid command (or 'help' for directions): ")
            if response == "exit":
                print("Goodbye!")
                break
            continue
        #think of a different way to tell whether the entered a valid command after bars
        if split_response[0].lower() == "bars":
            if len(split_response)==1:
                info = process_command(response)
                for x in info:
                    print(x[0],x[1],x[2],x[3],x[4],x[5])
            elif len(split_response) == 2:
                if "sellcountry" == split_response[1].split("=")[0] or "sourcecountry" == split_response[1].split("=")[0] or "sellregion" == split_response[1].split("=")[0] or "sourceregion" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    info = process_command(response)
                    if info == "None":
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    for x in info:
                        print(x[0],x[1],x[2],x[3],x[4],x[5])
                elif "ratings" == split_response[1] or "cocoa" == split_response[1]:
                    info = process_command(response)
                    for x in info:
                        print(x[0],x[1],x[2],x[3],x[4],x[5])
                elif "top" == split_response[1].split("=")[0] or "bottom" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    try:
                        list_top= split_response[1].split("=")
                        int(list_top[1])
                    except:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    info = process_command(response)
                    if info == "None":
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    for x in info:
                        print(x[0],x[1],x[2],x[3],x[4],x[5])
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response) == 3:
                if "sellcountry" == split_response[1].split("=")[0] or "sourcecountry" == split_response[1].split("=")[0] or "sellregion" == split_response[1].split("=")[0] or "sourceregion" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    if "ratings" == split_response[2] or "cocoa"== split_response[2]:
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2],x[3],x[4],x[5])
                    elif "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2],x[3],x[4],x[5])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                elif "ratings" == split_response[1] or "cocoa"== split_response[1]:
                    if "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2],x[3],x[4],x[5])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response)== 4:
                if "sellcountry" == split_response[1].split("=")[0] or "sourcecountry" == split_response[1].split("=")[0] or "sellregion" == split_response[1].split("=")[0] or "sourceregion" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    if "ratings" == split_response[2] or "cocoa" == split_response[2]:
                        if "top" == split_response[3].split('=')[0] or "bottom" == split_response[3].split('=')[0]:
                            if "=" not in split_response[3]:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            try:
                                list_top= split_response[3].split("=")
                                int(list_top[1])
                            except:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            info = process_command(response)
                            if info == "None":
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            for x in info:
                                print(x[0],x[1],x[2],x[3],x[4],x[5])
                        else:
                            print("Command not recognized: "+response)
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            else:
                print("Command not recognized: "+response)
                response = input("Please enter a valid command (or 'help' for directions): ")
                if response == "exit":
                    print("Goodbye!")
                    break
                continue
            # info = process_command(response)
            # for x in info:
            #     print(x[0],x[1],x[2],x[3],x[4],x[5])
        elif split_response[0].lower() == "companies":
            if len(split_response)==1:
                info = process_command(response)
                for x in info:
                    print(x[0],x[1],x[2])
            elif len(split_response) == 2:
                try:
                    if "country" == split_response[1].split("=")[0] or "region" == split_response[1].split("=")[0]:
                        if "=" not in split_response[1]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    elif "ratings" == split_response[1] or "cocoa" == split_response[1] or "bars_sold"== split_response[1]:
                        info = process_command(response)
                        for x in info:
                            print(x[0],x[1],x[2])
                    elif "top" == split_response[1].split("=")[0] or "bottom" == split_response[1].split("=")[0]:
                        if "=" not in split_response[1]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[1].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                except:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response) == 3:
                if "country" == split_response[1].split("=")[0] or "region" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    if "ratings" == split_response[2] or "cocoa"== split_response[2] or "bars_sold" == split_response[2]:
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    elif "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                elif "ratings" == split_response[1] or "cocoa"== split_response[1] or "bars_sold"==split_response[1]:
                    if "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response)== 4:
                if "country" == split_response[1].split("=")[0] or "region" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    if "ratings" == split_response[2] or "cocoa" == split_response[2] or "bars_sold" == split_response[2]:
                        if "top" == split_response[3].split("=")[0] or "bottom" == split_response[3].split("=")[0]:
                            if "=" not in split_response[3]:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            try:
                                list_top= split_response[3].split("=")
                                int(list_top[1])
                            except:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            info = process_command(response)
                            if info == "None":
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            for x in info:
                                print(x[0],x[1],x[2])
                        else:
                            print("Command not recognized: "+response)
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            else:
                print("Command not recognized: "+response)
                response = input("Please enter a valid command (or 'help' for directions): ")
                if response == "exit":
                    print("Goodbye!")
                    break
                continue
        elif split_response[0].lower() == "countries":
            if len(split_response)==1:
                info = process_command(response)
                for x in info:
                    print(x[0],x[1],x[2])
            elif len(split_response) == 2:
                if "region" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    info = process_command(response)
                    if info == "None":
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    for x in info:
                        print(x[0],x[1],x[2])
                if "sellers" == split_response[1] or "sources" == split_response[1]:
                    info = process_command(response)
                    for x in info:
                        print(x[0],x[1],x[2])
                elif "ratings" == split_response[1] or "cocoa" == split_response[1] or "bars_sold"== split_response[1]:
                    info = process_command(response)
                    for x in info:
                        print(x[0],x[1],x[2])
                elif "top" == split_response[1].split("=")[0] or "bottom" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    try:
                        list_top= split_response[1].split("=")
                        int(list_top[1])
                    except:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    info = process_command(response)
                    if info == "None":
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    for x in info:
                        print(x[0],x[1],x[2])
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response) == 3:
                if "region" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    if "ratings" == split_response[2] or "cocoa"== split_response[2] or "bars_sold" == split_response[2]:
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    elif "sellers" == split_response[2] or "sources" == split_response[2]:
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    elif "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                elif "sellers" == split_response[1] or "sources" == split_response[1]:
                    if "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    elif "ratings" == split_response[2] or "cocoa"== split_response[2] or "bars_sold"==split_response[2]:
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                elif "ratings" == split_response[1] or "cocoa"== split_response[1] or "bars_sold"==split_response[1]:
                    if "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1],x[2])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response)== 4:
                if "country" == split_response[1].split("=")[0] or "region" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    if "sellers" == split_response[2] or "sources" == split_response[2]:
                        if "ratings" == split_response[3] or "cocoa"== split_response[3] or "bars_sold" == split_response[3]:
                            info = process_command(response)
                            if info == "None":
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            for x in info:
                                print(x[0],x[1],x[2])
                        elif "top" == split_response[3].split("=")[0] or "bottom" == split_response[3].split("=")[0]:
                            if "=" not in split_response[3]:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            try:
                                list_top= split_response[3].split("=")
                                int(list_top[1])
                            except:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            info = process_command(response)
                            if info == "None":
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            for x in info:
                                print(x[0],x[1],x[2])
                        else:
                            print("Command not recognized: "+response)
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                    elif "ratings" == split_response[2] or "cocoa"== split_response[2] or "bars_sold" == split_response[2]:
                        if "top" == split_response[3].split("=")[0] or "bottom" == split_response[3].split("=")[0]:
                            if "=" not in split_response[3]:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            try:
                                list_top= split_response[3].split("=")
                                int(list_top[1])
                            except:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            info = process_command(response)
                            if info == "None":
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            for x in info:
                                print(x[0],x[1],x[2])
                        else:
                            print("Command not recognized: "+response)
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                elif "sellers" == split_response[1] or "sources" == split_response[1]:
                    if "ratings" == split_response[2] or "cocoa"== split_response[2] or "bars_sold" == split_response[2]:
                        if "top" == split_response[3].split("=")[0] or "bottom" == split_response[3].split("=")[0]:
                            if "=" not in split_response[3]:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            try:
                                list_top= split_response[3].split("=")
                                int(list_top[1])
                            except:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            info = process_command(response)
                            if info == "None":
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            for x in info:
                                print(x[0],x[1],x[2])
                        else:
                            print("Command not recognized: "+response)
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response)== 5:
                    if "country" == split_response[1].split("=")[0] or "region" == split_response[1].split("=")[0]:
                        if "=" not in split_response[1]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        if "sellers" == split_response[2] or "sources" == split_response[2]:
                            if "ratings" == split_response[3] or "cocoa" == split_response[3] or "bars_sold" == split_response[3]:
                                if "top" == split_response[4].split("=")[0] or "bottom" == split_response[4].split("=")[0]:
                                    if "=" not in split_response[4]:
                                        response = input("Please enter a valid command (or 'help' for directions): ")
                                        if response == "exit":
                                            print("Goodbye!")
                                            break
                                        continue
                                    try:
                                        list_top= split_response[4].split("=")
                                        int(list_top[1])
                                    except:
                                        response = input("Please enter a valid command (or 'help' for directions): ")
                                        if response == "exit":
                                            print("Goodbye!")
                                            break
                                        continue
                                    info = process_command(response)
                                    if info == "None":
                                        response = input("Please enter a valid command (or 'help' for directions): ")
                                        if response == "exit":
                                            print("Goodbye!")
                                            break
                                        continue
                                    for x in info:
                                        print(x[0],x[1],x[2])
                                else:
                                    print("Command not recognized: "+response)
                                    response = input("Please enter a valid command (or 'help' for directions): ")
                                    if response == "exit":
                                        print("Goodbye!")
                                        break
                                    continue
                            else:
                                print("Command not recognized: "+response)
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                        else:
                            print("Command not recognized: "+response)
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
        elif split_response[0].lower() == "regions":
            if len(split_response)==1:
                info = process_command(response)
                for x in info:
                    print(x[0],x[1])
            elif len(split_response) == 2:
                if "sellers" == split_response[1] or "sources" == split_response[1]:
                    info = process_command(response)
                    for x in info:
                        print(x[0],x[1])
                elif "ratings" == split_response[1] or "cocoa" == split_response[1] or "bars_sold"== split_response[1]:
                    info = process_command(response)
                    for x in info:
                        print(x[0],x[1])
                elif "top" == split_response[1].split("=")[0] or "bottom" == split_response[1].split("=")[0]:
                    if "=" not in split_response[1]:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    try:
                        list_top= split_response[1].split("=")
                        int(list_top[1])
                    except:
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    info = process_command(response)
                    if info == "None":
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                    for x in info:
                        print(x[0],x[1])
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response) == 3:
                if "sellers" == split_response[1] or "sources" == split_response[1]:
                    if "ratings" == split_response[2] or "cocoa"== split_response[2] or "bars_sold" == split_response[2]:
                        info = process_command(response)
                        for x in info:
                            print(x[0],x[1])
                    elif "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                elif "ratings" == split_response[1] or "cocoa"== split_response[1] or "bars_sold"==split_response[1]:
                    if "top" == split_response[2].split("=")[0] or "bottom" == split_response[2].split("=")[0]:
                        if "=" not in split_response[2]:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        try:
                            list_top= split_response[2].split("=")
                            int(list_top[1])
                        except:
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        info = process_command(response)
                        if info == "None":
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                        for x in info:
                            print(x[0],x[1])
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue
                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
            elif len(split_response) == 4:
                if "sellers" == split_response[1] or "sources" == split_response[1]:
                    if "ratings" == split_response[2] or "cocoa"== split_response[2] or "bars_sold"==split_response[2]:
                        if "top" == split_response[3].split("=")[0] or "bottom" == split_response[3].split("=")[0]:
                            if "=" not in split_response[3]:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            try:
                                list_top= split_response[3].split("=")
                                int(list_top[1])
                            except:
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            info = process_command(response)
                            if info == "None":
                                response = input("Please enter a valid command (or 'help' for directions): ")
                                if response == "exit":
                                    print("Goodbye!")
                                    break
                                continue
                            for x in info:
                                print(x[0],x[1])
                        else:
                            print("Command not recognized: "+response)
                            response = input("Please enter a valid command (or 'help' for directions): ")
                            if response == "exit":
                                print("Goodbye!")
                                break
                            continue
                    else:
                        print("Command not recognized: "+response)
                        response = input("Please enter a valid command (or 'help' for directions): ")
                        if response == "exit":
                            print("Goodbye!")
                            break
                        continue

                else:
                    print("Command not recognized: "+response)
                    response = input("Please enter a valid command (or 'help' for directions): ")
                    if response == "exit":
                        print("Goodbye!")
                        break
                    continue
        else:
            print("Command not recognized: "+response)
            response = input("Please enter a valid command (or 'help' for directions): ")
            if response == "exit":
                print("Goodbye!")
                break
            continue
        print("")
        response = input('Enter a command: ')
        if response == "exit":
            print("GoodBye!")
            break
# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    init_db(DBNAME)
    insert_flavors_of_cacao_cleaned()
    insert_countries()
    update_company_location_id()
    update_BroadBeanOriginId()
    interactive_prompt()
    #print examples:
    #print(regions('regions sources bars_sold top=5'))
    #print(process_command("companies country=US cocoa"))
    #print(process_command("countries region=Asia sellers cocoa bottom=5"))
    #print(process_command("regions sources bars_sold top=5"))
    #print(process_command("bars sourceregion=Asia cocoa bottom=5"))
    #print(process_command('countries sources ratings bottom=5'))
