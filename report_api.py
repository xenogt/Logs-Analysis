#!/usr/bin/python

import psycopg2
import bleach

DBNAME = "news"


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        # THEN perhaps exit the program
        sys.exit(1) # The easier method
        # OR perhaps throw an error
        raise e
        # If you choose to raise an exception,
        # It will need to be caught by the whoever called this function


def get_query_results(query):
    """common method that takes care of connecting to db, grab cursor,
    execute query, close db connection and returns the query result."""
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def get_top_3_viewed_articles():
    '''
    runs the query to fetch top 3 articles' title that have most
    views, prints the resulting titles with most viewed title first
    '''
    query = "select title as title, num as count from " \
            "(select title, slug, count(*) as num " \
            "from log a join articles b on substring(a.path, 10)=b.slug " \
            "group by b.slug, b.title order by num desc limit 3) " \
            "result;"
    articles = get_query_results(query)

    print("")
    print("----------------------------------------------------")
    for i in articles:
        print(i[0]+"  ---  "+str(i[1])+" views")
    print("")
    return articles


def get_most_popular_author_list():
    '''
    runs the query to fetch authors' names and combined number of views
    on articles per arthor. Prints the resulting data, authors with most
    combined views of articles would be displayed on top.
    '''
    query = "select name, result_author.num " \
        "from authors, " \
        "(select author, count(*) as num " \
        "from log a join articles b on substring(a.path, 10)=b.slug " \
        "group by b.author " \
        "order by num desc)" \
        "as result_author " \
        "where id=result_author.author;"
    authors = get_query_results(query)

    print("")
    print("----------------------------------------------------")
    for i in authors:
        print(i[0]+"  ---  "+str(i[1])+" views")
    print("")
    return authors


def get_days_result_in_1percent_error():
    '''
    runs query to find days that has more than 1% of access result in
    error. Prints the information on screen.
    '''
    query = "select c.t, c.errors from" \
        "(select a.t1::timestamp::date as t, " \
        "(a.error::decimal/b.total)*100 as errors " \
        "from (select " \
        "time::timestamp::date as t1, " \
        "count(time::timestamp::date) as error " \
        "from log where status like '%404%' " \
        "group by time::timestamp::date) a, " \
        "(select time::timestamp::date as t2, " \
        "count(time::timestamp::date) as total " \
        "from log group by time::timestamp::date) b " \
        "where a.t1=b.t2) c where c.errors > 1;"
    days = get_query_results(query)
    
    print("")
    print("----------------------------------------------------")
    for i in days:
        print(str(i[0])+"  ---  "+str(round(i[1], 2))+"% errors")
    print("")
    return days
