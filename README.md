# Logs-Analysis

## 1. What are the most popular three articles of all time? 
/code select title, slug, count(*) as num from log a join articles b on substring(a.path, 10)=b.slug group by b.slug, b.title order by num desc limit 3;

 ###candidate-is-jerk         | 338647
 ###bears-love-berries        | 253801
 ###bad-things-gone           | 170098

## 2. Who are the most popular article authors of all time?

select authors.name from authors as authors, (select author from (select author, count(*) as num from log a join articles b on substring(a.path, 10)=b.slug group by b.author order by num desc) as result) as result_author where authors.id=result_author.author;

## 3. On which days did more than 1% of requests lead to errors?