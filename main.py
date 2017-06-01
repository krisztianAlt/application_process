import psycopg2
from os import system


def menu():
    system("clear")
    title = "APPLICATION PROCESS 1.0"
    print('-'*len(title))
    print(title)
    print('-'*len(title))
    # Display the menu
    menu_items = ["Mentor\'s name (first, last)",
                  "Nick names of all mentors working at Miskolc",
                  "The lost hat, Chapter One: Carol\'s datas",
                  "The lost hat, Chapter Two: The other girl\'s datas",
                  "Markus Schaffarzyk is on the board: insert his datas",
                  "Jemima Foreman\'s new phone number",
                  "Remove all the applicants, who applied with emails for mauriseu.net domain",
                  "See the whole Mentors table",
                  "See the whole Applicants table",
                  "Exit"]
    for index, item in enumerate(menu_items):
        print("{}. {}".format(index+1, item))
    print("")

    # Handle the user choose
    user_choose_is_invalid = True
    while user_choose_is_invalid:
        user_choosed_menu = input("Choose a menu: ")
        try:
            user_choosed_menu = int(user_choosed_menu)
            if user_choosed_menu > 0 and user_choosed_menu < 11:
                user_choose_is_invalid = False
            else:
                raise KeyError
        except ValueError:
            print("Please, choose a number from the menu.")
        except KeyError:
            print("Please, choose between 1 and 8.")
    print("")
    return user_choosed_menu


def display_table(column_names, table):
    '''Display tables on the screen.

    Args:
    - column names
    - result rows of SQL select command
    '''

    # length of longest element in the table header and rows:
    max_lengths = [0 for _ in range(0, len(column_names))]
    for index in range(0, len(column_names)):
        if len(column_names[index]) > max_lengths[index]:
            max_lengths[index] = len(column_names[index])
    for row in table:
        for index in range(0, len(row)):
            if len(str(row[index])) > max_lengths[index]:
                max_lengths[index] = len(str(row[index]))

    # print table header (column names among lines):
    for index in range(0, len(column_names)):
            if index < len(column_names)-1:
                print('_'*(max_lengths[index]+1), end='')
            else:
                print('_'*(max_lengths[index]+1))
    for index in range(0, len(column_names)):
            if index < len(column_names)-1:
                print(column_names[index].ljust(max_lengths[index]+1, ' '), end='')
            else:
                print(column_names[index].ljust(max_lengths[index]+1, ' '))
    for index in range(0, len(column_names)):
            if index < len(column_names)-1:
                print('-'*(max_lengths[index]+1), end='')
            else:
                print('-'*(max_lengths[index]+1))

    # print table rows:
    for row in table:
        for index in range(0, len(row)):
            if index < len(row)-1:
                print(str(row[index]).ljust(max_lengths[index]+1, ' '), end='')
            else:
                print(str(row[index]).ljust(max_lengths[index]+1, ' '))

    # print close line of table:
    for index in range(0, len(column_names)):
        if index < len(column_names)-1:
            print('_'*(max_lengths[index]+1), end='')
        else:
            print('_'*(max_lengths[index]+1))

    input("\nPress Enter to continue!")


def working_session(cursor):
    end_of_work = False
    while end_of_work is False:
        answer = menu()
        if answer == 10:
            end_of_work = True
        else:
            if answer == 1:
                cursor.execute("""SELECT first_name, last_name FROM mentors;""")
                rows = cursor.fetchall()
                column_names = ["first_name", "last_name"]
                display_table(column_names, rows)
            elif answer == 2:
                cursor.execute("""SELECT nick_name FROM mentors WHERE city='Miskolc';""")
                rows = cursor.fetchall()
                column_names = ["nick_name"]
                display_table(column_names, rows)
            elif answer == 3:
                cursor.execute("""SELECT first_name, last_name, phone_number
                                  FROM applicants WHERE first_name = 'Carol';""")
                rows = cursor.fetchall()
                for index in range(len(rows)):
                    rows[index] = (rows[index][0] + ' ' + rows[index][1], rows[index][2])
                column_names = ["full_name", "phone_number"]
                display_table(column_names, rows)
            elif answer == 4:
                cursor.execute("""SELECT first_name, last_name, phone_number
                                  FROM applicants
                                  WHERE email LIKE '%@adipiscingenimmi.edu';""")
                rows = cursor.fetchall()
                for index in range(len(rows)):
                    rows[index] = (rows[index][0] + ' ' + rows[index][1], rows[index][2])
                column_names = ["full_name", "phone_number"]
                display_table(column_names, rows)
            elif answer == 5:
                try:
                    cursor.execute("""INSERT INTO applicants (first_name, last_name, phone_number, email, application_code)
                    VALUES ('Markus', 'Schaffarzyk', '003620/725-2666', 'djnovus@groovecoverage.com', 54823);""")
                    cursor.execute("""SELECT * FROM applicants WHERE application_code = 54823""")
                    rows = cursor.fetchall()
                    column_names = ["id", "first_name", "last_name", "phone_number", "email", "application_code"]
                    display_table(column_names, rows)
                except:
                    print('This application code already exists.')
                    input("\nPress Enter to continue!")
            elif answer == 6:
                cursor.execute("""UPDATE applicants SET phone_number = '003670/223-7459'
                                  WHERE first_name = 'Jemima' AND last_name = 'Foreman';""")
                cursor.execute("""SELECT * FROM applicants WHERE first_name = 'Jemima' and last_name = 'Foreman';""")
                rows = cursor.fetchall()
                column_names = ["id", "first_name", "last_name", "phone_number", "email", "application_code"]
                display_table(column_names, rows)
            elif answer == 7:
                cursor.execute("""DELETE FROM applicants WHERE email LIKE '%@mauriseu.net';""")
                cursor.execute("""SELECT * FROM applicants;""")
                rows = cursor.fetchall()
                column_names = ["id", "first_name", "last_name", "phone_number", "email", "application_code"]
                display_table(column_names, rows)
            elif answer == 8:
                cursor.execute("""SELECT * FROM mentors;""")
                rows = cursor.fetchall()
                column_names = ["id", "first_name", "last_name",
                                "nick_name", "phone_number", "email",
                                "city", "favourite_number"]
                display_table(column_names, rows)
            elif answer == 9:
                cursor.execute("""SELECT * FROM applicants;""")
                rows = cursor.fetchall()
                column_names = ["id", "first_name", "last_name", "phone_number", "email", "application_code"]
                display_table(column_names, rows)
    print("\nThanks for the great job.\nSee you next time.")


def main():
    # Create database connection and check it:
    try:
        connect_str = "dbname='krisztian' user='krisztian' host='localhost' password='iwillbeaprogrammer'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM mentors;""")
        cursor.execute("""SELECT * FROM applicants;""")
        # After tables are allright:
        working_session(cursor)
    except Exception as e:
        print("Invalid dbname, user or password.")
        print(e)
        print("Please, repair it!")


if __name__ == '__main__':
    main()
