import mysql.connector


## Connecting to database
mydb = mysql.connector.connect(host="localhost", user="bruno", database="ict128")
mycursor = mydb.cursor()

## Queries:

## 1. As a customer I want to list all the action movies.

# query = """
# SELECT
#     *
# FROM
#     CONTENT
# WHERE
#     type = 'movie' AND genre = 'action';
# """

# mycursor.execute(query)

# myresult = mycursor.fetchall()

# for x in myresult:
#     print(x)


## 2. As a manager I want to know the number of movies currently available at the “no limit” tier.

# query = """
# SELECT
#     COUNT(*)
# FROM
#     CONTENT
# WHERE
#     type = 'movie' AND tier = 'no-limits';
# """

# mycursor.execute(query)

# myresult = mycursor.fetchall()

## 3. As a customer I want to change my tier from free to mid-level.

# ### Assumptions: as a customer you can only change the tier for the account you are under.
# ### To change tiers, the customer will need to know: 'account ID' and 'password'.

# query = """
# UPDATE ACCOUNT
# SET
#     plan = 'mid-tier'
# WHERE
#     ACC_ID = 1;
# """

# mycursor.execute(query)

# myresult = mycursor.fetchall()

# for x in myresult:
#     print(x)

## 4. As a customer I want to create a new account on the system at the free tier level.

# # Creating the free account:
# query_1 = """
# INSERT INTO ACCOUNT (CT_CODE, plan, password) VALUES ("BRA", "free", "123password")
# """

# # Link customer to new account by getting the MAX(ACC_ID) of the newly created account.
# query_2 = """
# INSERT INTO CUSTOMER (ACC_ID, f_name, l_name, email)
# SELECT MAX(ACC_ID), "Bruno", "Ribeiro", "me@place.ca"
# FROM ACCOUNT;
# """

# 5. As a customer, I want to add an additional email to the account (give another person access to
# the account).

# ## Assumption: the customer knows the account id

# query = """
# INSERT INTO CUSTOMER (ACC_ID, f_name, l_name, email)
# VALUES (10001, "Natalia", "Sena", "her@place.ca");
# """

# 6. As a manager I want to know all the horror movies where at least one customer has given it a 5
# rating.

# # The query will return the C_ID of these movies.

# """
# SELECT
#     s.C_ID, c.type, c.genre, s.star_rate, COUNT(*) AS number_of_ratings
# FROM
#     STREAM AS s
# INNER JOIN
#     CONTENT AS c
#         ON s.C_ID = c.C_ID
# WHERE
#     c.type = "movie" AND c.genre = "horror" AND s.star_rate = 5
# GROUP BY
#     s.C_ID, s.star_rate
# HAVING
#     number_of_ratings >= 1;
# """

# 7. As a manager I want to change all the content from a particular distributor as unavailable
# because the contract with the distributor has expired.

# First select all availability with DIS_ID = 100

# # """
# # SELECT
# #     a.C_ID, c.DIS_ID, a.available
# # FROM
# #     CONTENT AS c
# # INNER JOIN
# #     AVAILABILITY AS a
# # ON
# #     c.C_ID = a.C_ID
# # WHERE
# #     c.DIS_ID = 100;
# """

# Given an DIS_ID (100, in this example), set all 'available fields to 0
# """
# UPDATE AVAILABILITY AS a
# INNER JOIN CONTENT AS c
#     ON a.C_ID = c.C_ID
# SET
#     a.available = 0
# WHERE c.DIS_ID = 100;
# """

# 8. As a manager I want to delete a customer that is on a mid-tier plan whose subscription is paid for
# 4 more months.

# ## ASSUMPTION: all subscriptions are for one year.

# # List subscription payments with account and plan info with payment from 8 months ago

# """
# SELECT
#     a.ACC_ID, cx.CX_ID, purpose, success, date_time, plan
# FROM
#     CUSTOMER AS cx
# INNER JOIN
#     ACCOUNT AS a
#     ON cx.ACC_ID = a.ACC_ID
# INNER JOIN
#     PAYMENT AS p
#     ON a.ACC_ID = p.ACC_ID
# INNER JOIN
#     DATE_KEEP as d
#     ON p.D_ID = d.D_ID
# WHERE
#     purpose = "subs" AND plan = "mid-tier" AND date_time > (NOW() - INTERVAL 8 MONTH);
# """

# # Deleting these customers
# """
# DELETE cx.*
# FROM
#     CUSTOMER AS cx
# INNER JOIN
#     ACCOUNT AS a
#     ON cx.ACC_ID = a.ACC_ID
# INNER JOIN
#     PAYMENT AS p
#     ON a.ACC_ID = p.ACC_ID
# INNER JOIN
#     DATE_KEEP as d
#     ON p.D_ID = d.D_ID
# WHERE
#     purpose = "subs" AND plan = "mid-tier" AND date_time > (NOW() - INTERVAL 8 MONTH);
# """

# 9. As a manager I want to find the average star rating for every genre of all the tv-series that were
# viewed in the last month.

# # All tv-series viewd last month
# """
# SELECT
#     c.type, c.genre, AVG(s.star_rate) AS avg_star_rating
# FROM
#     STREAM AS s
# INNER JOIN
#     CONTENT AS c
# USING (C_ID)
# WHERE
#     c.type = "tv-serie"
#     AND
#     c.last_viewed > (NOW() - INTERVAL 1 MONTH)
# GROUP BY
#     c.genre;
# """
