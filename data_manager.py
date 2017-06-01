import psycopg2


def connect_database():
    try:
        # setup connection string
        connect_str = "dbname='krisztian' user='krisztian' host='localhost'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # set autocommit option, to do every query when we call it
        conn.autocommit = True
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    return cursor, conn


def query_result(*query):
    """Execute SQL query and return the result if it exists.

    Close the connection after execution.
    """
    try:
        cursor, conn = connect_database()
        cursor.execute(*query)
        rows = cursor.fetchall()
        rows = [list(row) for row in rows]
    except psycopg2.OperationalError as e:
        print(e)
    except psycopg2.ProgrammingError as e:
        print(e)
        print("Nothing to print")
        rows = ""
    except psycopg2.IntegrityError as e:
        print(e)
        rows = ""
    finally:
        if conn:
            conn.close()

    return rows


def mentors_and_schools():
    return query_result("""SELECT mentors.first_name, mentors.last_name, schools.name, schools.country
                        FROM mentors
                        INNER JOIN schools ON mentors.city=schools.city
                        ORDER BY mentors.id;""")


def all_school():
    return query_result("""SELECT mentors.first_name, mentors.last_name, schools.name, schools.country
                        FROM mentors
                        RIGHT JOIN schools ON mentors.city=schools.city
                        ORDER BY mentors.id;""")