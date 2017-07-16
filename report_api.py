#! /usr/bin/python

import psycopg2, bleach

DBNAME = "news"

'''
runs the query to fetch top 3 articles' title that have most
views, prints the resulting titles with most viewed title first
'''
def get_top_3_viewed_articles():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(
    "select title as title, num as count from "+
      "(select title, slug, count(*) as num "+
      "from log a join articles b on substring(a.path, 10)=b.slug "+
      "group by b.slug, b.title order by num desc limit 3) "+
    "result;")
  articles = c.fetchall()
  print("")
  print("----------------------------------------------------")
  for i in articles:
    print(i[0]+"  ---  "+str(i[1])+" views")
  print("")
  db.close()
  return articles

'''
runs the query to fetch authors' names and combined number of views
on articles per arthor. Prints the resulting data, authors with most
combined views of articles would be displayed on top.
'''
def get_most_popular_author_list():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(
    "select name, result_author.num "+
    "from authors, "+
      "(select author, count(*) as num "+
      "from log a join articles b on substring(a.path, 10)=b.slug "+
      "group by b.author "+
      "order by num desc)"+
    "as result_author "+
    "where id=result_author.author;")
  authors = c.fetchall()
  print("")
  print("----------------------------------------------------")
  for i in authors:
    print(i[0]+"  ---  "+str(i[1])+" views")
  print("")
  db.close()
  return authors

'''
runs query to find days that has more than 1% of access result in
error. Prints the information on screen.
'''
def get_days_result_in_1percent_error():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(
    "select c.t, c.errors "+
    "from"+ 
    "(select "+
      "a.t1::timestamp::date as t, "+
      "(a.error::decimal/b.total)*100 as errors "+
      "from "+
        "(select "+
          "time::timestamp::date as t1, "+
          "count(time::timestamp::date) as error "+
          "from log "+
          "where status like '%404%' "+
          "group by time::timestamp::date"+
        ") a, "+
        "(select "+
          "time::timestamp::date as t2, "+
          "count(time::timestamp::date) as total "+
          "from log "+
          "group by time::timestamp::date"+
          ") b "+
        "where a.t1=b.t2"+
    ") c where c.errors > 1;")
  days = c.fetchall()
  print("")
  print("----------------------------------------------------")
  for i in days:
    print(str(i[0])+"  ---  "+str(round(i[1], 2))+"% errors")
  print("")
  db.close()
  return days
