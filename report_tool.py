#!/usr/bin/python

import report_api as api


def show_menu():
    '''
    This method presents the initial screen when running the application. It
    will show the user a list of project questions and allows the user to
    select the item which will triggers the corresponding query to run to
    return useful information.
    '''
    leave = False
    # loops forever until leave === True
    while(not leave):
        Q1 = "1 - What are the most popular three articles of all time?"
        Q2 = "2 - Who are the most popular article authors of all time?"
        Q3 = "3 - On which days did more than 1% of requests lead to errors?"
        continue_msg = "press any key to continue ... "

        print("----------------------------------------------------")
        print("                 Log Reporting Tool     ")
        print("----------------------------------------------------")
        print("")
        print("Select the corresponding number to view report")
        print("")
        print(Q1)
        print(Q2)
        print(Q3)
        print("4 - exit")
        print("")
        a = raw_input("Please select: ")
        print("")

        if str(a) == "1":
            print("REPORT " + Q1)
            api.get_top_3_viewed_articles()
            raw_input(continue_msg)
        elif str(a) == "2":
            print("REPORT " + Q2)
            api.get_most_popular_author_list()
            raw_input(continue_msg)
        elif str(a) == "3":
            print("REPORT " + Q3)
            api.get_days_result_in_1percent_error()
            raw_input(continue_msg)
        elif str(a) == "4":
            print("exiting ... BYE")
            leave = True
        else:
            raw_input("invalid input, press any key to continue ...")


if __name__ == '__main__':
    show_menu()

