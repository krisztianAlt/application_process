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


def mentors_by_country():
    return query_result("""SELECT schools.country, COUNT(mentors.id)
                        FROM schools
                        INNER JOIN mentors ON schools.city=mentors.city
                        GROUP BY schools.country
                        ORDER BY schools.country ASC;""")


def contacts():
    return query_result("""SELECT schools.name, mentors.first_name, mentors.last_name
                        FROM schools
                        INNER JOIN mentors ON schools.contact_person=mentors.id
                        ORDER BY schools.name;""")


def applicants():
    return query_result("""SELECT a.first_name, a.application_code, am.creation_date
                        FROM applicants a
                        INNER JOIN applicants_mentors am ON a.id=am.applicant_id
                        WHERE am.creation_date>'2016-01-01'
                        ORDER BY am.creation_date DESC;""")


def applicants_and_mentors():
    return query_result("""SELECT a.first_name, a.application_code, m.first_name, m.last_name
                        FROM applicants a
                        LEFT JOIN applicants_mentors am ON a.id=am.applicant_id
                        LEFT JOIN mentors m ON am.mentor_id=m.id
                        ORDER BY a.id;""")


def applicants_and_schools():
    return query_result("""SELECT a.first_name, a.last_name, s.name, s.city, s.country
                        FROM applicants AS a
                        INNER JOIN applicants_mentors AS am ON a.id=am.applicant_id
                        INNER JOIN mentors AS m ON am.mentor_id=m.id
                        INNER JOIN schools AS s ON m.city=s.city
                        ORDER BY a.last_name ASC;""")


def applicants_per_schools():
    return query_result("""SELECT s.name, COUNT(a.id)
                        FROM applicants AS a
                        RIGHT JOIN applicants_mentors AS am ON a.id=am.applicant_id
                        RIGHT JOIN mentors AS m ON am.mentor_id=m.id
                        RIGHT JOIN schools AS s ON m.city=s.city
                        GROUP BY s.name
                        ORDER BY s.name ASC;""")
