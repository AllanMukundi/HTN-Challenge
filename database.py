import sqlite3, json, requests 

r = requests.get('https://htn-interviews.firebaseio.com/users.json?download')
user_data = json.loads(r.text)
print(user_data)
database = sqlite3.connect(':memory:')
cursor = database.cursor()

try:

    cursor.execute("""CREATE TABLE Users (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name TEXT NOT NULL,
                        picture TEXT NOT NULL,
                        company TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        latitude REAL NOT NULL,
                        longitude REAL NOT NULL
                    )""")

    cursor.execute("""CREATE TABLE Skills (
                        email INTEGER NOT NULL,
                        name TEXT NOT NULL, 
                        rating REAL NOT NULL
                    )""")

    database.commit()

    try:

        for i in range(len(user_data)):
            cursor.execute("""INSERT INTO Users(name, picture, company, email, phone, latitude, longitude)
                            VALUES(:name, :picture, :company, :email, :phone, :latitude, :longitude)""",
                            {'name':user_data[i]['name'], 'picture':user_data[i]['picture'], 'company':user_data[i]['company'],
                                'email':user_data[i]['email'], 'phone':user_data[i]['phone'], 'latitude':user_data[i]['latitude'],
                                'longitude':user_data[i]['longitude']})

            for skill in range(len(user_data[i]['skills'])):
                cursor.execute("""INSERT INTO Skills(email, name, rating)
                                VALUES(:email, :name, :rating)""",
                                {'email':user_data[i]['email'], 'name':user_data[i]['skills'][skill]['name'], 'rating':user_data[i]['skills'][skill]['rating']})

        database.commit()
        print("Insertion complete.")

    except sqlite3.OperationalError:
        print("Error inserting values.")

except sqlite3.OperationalError:
    print("Table could not be created.")


finally:
    database.close()
