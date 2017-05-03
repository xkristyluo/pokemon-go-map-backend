import time
import psycopg2

# SELECT expire,pokemon_id, latitude, longitude FROM pokemon_map WHERE longitude > west  AND longitude < east  AND latitude > south AND latitude < north AND expire > current time in ms since the epoch LIMIT 100
def get_pokemons_from_db(north, south, west, east):
    # 1. Open connection: connect to pokemon_map database
    conn = psycopg2.connect(host = "week2demo3.cp24vhenjjas.us-west-2.rds.amazonaws.com",
                            port = 5432,
                            user = "week2demo3",
                            password = "xluo1984",
                            database = "week2demo3")

    # 2. Execute SQL: create a cursor to execute database commands and queries
    with conn.cursor() as cur:
        cur.execute("SELECT expire,pokemon_id, latitude, longitude" + 
                    " FROM pokemon_map " + 
                    " WHERE longitude > %s" +
                    " AND longitude < %s" +
                    " AND latitude > %s" +
                    " AND latitude < %s" +
                    " AND expire > %s" +
                    " LIMIT 100", 
                    (west, east, south, north, time.time() * 1000))
        rows = cur.fetchall()
        result = []
        for row in rows:
            # 1476566289000.0, 231, 41.4195807480884, -73.9995309631575
            result.append({
                            "expiration_timestamp_ms" : row[0],
                            "pokemon_id" : row[1],
                            "latitude" : row[2],
                            "longitude" : row[3]
                          })

    # 3. connection commit 
    conn.commit()
    return result
