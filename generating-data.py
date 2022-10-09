## Bruno Vieira Ribeiro - October, 2022
## ICT 128 - Project Phase II
## Script to generate artificial data into MySQL database

## Modules used:
## - mysql.connector -> to interact with the database
## - numpy           -> to generated numerical data
## - pandas          -> to read and write data on countries
## - silly           -> to generated descriptions and locations
## - faker           -> to generate names and emails
#################################################################

# Imports
import mysql.connector
import numpy as np
import pandas as pd
import silly
from faker import Faker

# Instantiating faker object
fake = Faker()

## Connecting to database
mydb = mysql.connector.connect(host="localhost", user="bruno", database="ict128")
mycursor = mydb.cursor()

#################################################################
### Generating data for COUNTRY
#################################################################

# Will read from https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv

# countries_data = pd.read_csv(
#     "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv",
#     usecols=["name", "alpha-3", "region"],
# )
# print(countries_data.head())
# countries_data.to_csv("countries_data.csv", index=False)

# Reading data after local save
countries_data = pd.read_csv("countries_data.csv")
# print(countries_data.head())

# Inserting data into database.
# COUNTRY table has the following columns:
# CT_CODE, ct_name, continent, currency
# We will populate this table with data from our countries_data dataframe.
# The currency will just be code+$, for simplicity

sql = "INSERT INTO COUNTRY (CT_CODE, ct_name, continent, currency) VALUES (%s, %s, %s, %s)"
val = []
for index, row in countries_data.iterrows():
    val.append(
        (row["alpha-3"], row["name"], row["region"].strip(), "$" + row["alpha-3"])
    )
    print(row["region"])

# print(countries_data.region.map(len).max())
# print(countries_data[countries_data[]])

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for ACCOUNT
################################################################

## ACCOUNT HAS THE FOLLOWING COLUMNS:
## ACC_ID (AUTO INCREMENTED), CT_CODE, plan, password
## Possible plans are: free, mid-tier, or no limits

## Let's create 1e4 accounts with random country, plan and password

## Setup for the choices
plans = ["free", "mid-tier", "no-limits"]
plans_weights = [0.6, 0.3, 0.1]
countries_data = pd.read_csv("countries_data.csv")
ct_codes = countries_data["alpha-3"].to_list()

## Inserting data

sql = "INSERT INTO ACCOUNT (CT_CODE, plan, password) VALUES (%s, %s, %s)"
val = []
for _ in range(10000):
    val.append(
        (
            np.random.choice(ct_codes),
            np.random.choice(plans, p=plans_weights),
            silly.plural(),
        )
    )

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for CUSTOMER
################################################################

## CUSTOMER HAS THE FOLLOWING COLUMNS:
## CX_ID (AUTO INCREMENTED), ACC_ID (FK), f_name, l_name, email
## ACC_ID needs to reference ACCOUNT but cannot have more than 4 CX per ACCOUNT
## ACC_ID (as of now) goes from 1 to 1e4

# Setup possible CXs
num_of_cx_weights = [0.6, 0.1, 0.1, 0.2]
num_of_cx = [1, 2, 3, 4]

sql = "INSERT INTO CUSTOMER (ACC_ID, f_name, l_name, email) VALUES (%s, %s, %s, %s)"
val = []

# Loop through all accounts_id:
for acc_id in range(1, 10001):
    cxs_in_acc = np.random.choice(num_of_cx, p=num_of_cx_weights)
    for cx in range(cxs_in_acc):
        val.append((acc_id, fake.first_name(), fake.last_name(), fake.email()))

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for DISTRIBUTOR
#################################################################

# ## DISTRBUTOR HAS THE FOLLOWING COLUMNS:
# ## DIS_ID (AUTO INCREMENTED), CT_CODE
# ## CT_CODE references the COUNTRY table

countries_data = pd.read_csv("countries_data.csv")
ct_codes = countries_data["alpha-3"].to_list()

## Inserting data

sql = "INSERT INTO DISTRIBUTOR (CT_CODE) VALUES (%s)"
val = []
for _ in range(200):
    val.append([np.random.choice(ct_codes)])

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for CONTENT
################################################################

## CONTENT HAS THE FOLLOWING COLUMNS:
## C_ID (AUTO INCREMENTED), DIS_ID, last_viewd, type, tier, description, genre
## DIS_ID references the DISTRIBUTOR table

## DIS_ID randomly selected from DISTRIBUTOR (200)
## last_viewd: we will assume every view will be after January 1st of 2022.
import datetime

start_date = datetime.date(year=2022, month=1, day=1)

## type can be any of:
diff_types = ["movie", "tv-serie", "documentary", "live-stream"]
types_weight = [0.4, 0.4, 0.1, 0.1]

## tier can be any of the plan type in accounts:
plans = ["free", "mid-tier", "no-limits"]
plans_weights = [0.2, 0.4, 0.4]

## description will be random

## genre can be any of
genres = ["action", "romance", "mystery", "horror", "comedy"]

## Inserting data

sql = "INSERT INTO CONTENT (DIS_ID, last_viewed, type, tier, description, genre) VALUES (%s, %s, %s, %s, %s, %s)"
val = []
for _ in range(2000):
    val.append(
        (
            np.random.randint(1, 201),
            fake.date_time_between(start_date=start_date, end_date="now"),
            np.random.choice(diff_types, p=types_weight),
            np.random.choice(plans, p=plans_weights),
            silly.paragraph(),
            np.random.choice(genres),
        )
    )

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")


################################################################
## Generating data for PAYMENT_TYPE
################################################################

## CONTENT HAS THE FOLLOWING COLUMNS:
## PT_ID (AUTO INCREMENTED), type


# type can be any of the following:
payment_types = ["credit", "debit", "OPS"]

## Inserting data

sql = "INSERT INTO PAYMENT_TYPE (type) VALUES (%s)"
val = []
for t in payment_types:
    val.append([t])

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for STREAM
################################################################

## STREAM HAS THE FOLLOWING COLUMNS:
## S_ID (AUTO INCREMENTED), ACC_ID, C_ID, P_ID, D_ID, perc_watched, star_rate, stream_date

# ACC_ID is random from (1,1e4)

# C_ID is random from (1,2000)

# P_ID is random but can be NULL.

# D_ID is a sequential integer number

# perc_watched is an INT chosen at random (will use binomial np.random.binomial(n=100, p=0.5))

# star_rate is an integer chosen at random (will use binomial np.random.binomial(n=5, p=0.5))

## Inserting data

sql = "INSERT INTO STREAM (ACC_ID, C_ID, P_ID, D_ID, perc_watched, star_rate) VALUES (%s, %s, %s, %s, %s, %s)"
val = []

for i in range(20000):
    val.append(
        (
            np.random.randint(1, 10001),
            np.random.randint(1, 2001),
            int(
                np.random.choice(
                    [np.random.randint(1, 15001), 0],
                    p=[0.8, 0.2],
                )
            ),
            int(i),
            np.random.binomial(n=100, p=0.5),
            np.random.binomial(n=5, p=0.5),
        )
    )

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for PAYMENT
################################################################

# Getting unique P_ID from STREAM
mycursor = mydb.cursor()

mycursor.execute("SELECT DISTINCT P_ID FROM STREAM")

myresult = mycursor.fetchall()

unique_P_ID = []

for x in myresult:
    unique_P_ID.append(int(x[0]))

unique_P_ID.sort()

# ## PAYMENT HAS THE FOLLOWING COLUMNS:
# ## P_ID (AUTO INCREMENTED), ACC_ID, PT_ID, S_ID, D_ID, amount, purpose, success, expiration, payment_date

# ACC_ID is random from (1,1e4)

# PT_ID is random from (1,2,3)

###### S_ID is random from (1, 2e4) or 0

# D_ID is sequential starting from 20000

# amount is random uniform

# purpose is "content" if S_ID greater than 0, otherwise is "subscription"

# succes is always TRUE unless PT_ID is 1, then it is random with a weight

# expiration is a random date if PT_ID = 1, otherwise it is set to now + 10years

# payment_date is a random date.

import datetime

start_date = datetime.date(year=2022, month=1, day=1)

## Inserting data

sql = "INSERT INTO PAYMENT (ACC_ID, PT_ID, D_ID, amount, purpose, success, expiration) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = []

for i in range(30000):
    PT_ID = int(np.random.choice([1, 2, 3]))

    # S_ID = int(
    #     np.random.choice(
    #         [np.random.randint(1, 15001), 0],
    #         p=[0.9, 0.1],
    #     )
    # )
    # if S_ID == 0:
    #     purpose = "subs"
    # else:
    #     purpose = "content"

    if (i + 1) in unique_P_ID:
        purpose = "content"
    else:
        purpose = "subs"

    mean_amount = 9.99
    std_amount = 1.99
    amount = np.random.normal(mean_amount, std_amount)
    amount = round(max(0.99, amount), 2)

    end_date = datetime.date(year=2999, month=1, day=1)
    expiration = fake.date_time_between(start_date=start_date, end_date=end_date)

    if PT_ID != 1:
        success = 1
    else:
        success = int(np.random.choice([1, 0], p=[0.98, 0.02]))
        if success == 0:
            old_date = datetime.date(year=2020, month=1, day=1)
            expiration = fake.date_time_between(
                start_date=old_date, end_date=start_date
            )

    val.append(
        (
            int(np.random.randint(1, 10001)),
            PT_ID,
            20000 + i,
            amount,
            purpose,
            success,
            expiration,
        )
    )

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for AVAILABILITY
################################################################

# ## AVAILABILITY HAS THE FOLLOWING COLUMNS:
# ## C_ID, CT_CODE, available, available_date, price


# Every C_ID needs info on availability.
# So this table show have all combinations of C_ID and CT_CODE.
# C_ID ranges 1 to 2000
# CT_CODE can be fecthed from

# Getting unique CT_CODE from COUNTRY
mycursor = mydb.cursor()

mycursor.execute("SELECT DISTINCT CT_CODE FROM COUNTRY")

myresult = mycursor.fetchall()

unique_CT_CODE = []

for x in myresult:
    unique_CT_CODE.append(x[0])

unique_CT_CODE.sort()

# print(unique_CT_CODE)

# available is a boolean chosen at random with weights.
av_choices = [0, 1]
av_weights = [0.2, 0.8]

# available date is a random date starting from Jan 1st of 2022
import datetime

start_date = datetime.date(year=2022, month=1, day=1)

# price is in the countries currency and will be generated randomly from normal distribution

## Inserting data

sql = "INSERT INTO AVAILABILITY (C_ID, CT_CODE, available, available_date, price) VALUES (%s, %s, %s, %s, %s)"
val = []

for cid in range(1, 2001):
    for ctcode in unique_CT_CODE:
        PT_ID = int(np.random.choice([1, 2, 3]))

        mean_price = 9.99
        std_price = 1.99
        price = np.random.normal(mean_price, std_price)
        price = round(max(0.99, price), 2)

        end_date = datetime.date(year=2022, month=12, day=30)
        av_date = fake.date_time_between(start_date=start_date, end_date=end_date)

        val.append(
            (
                cid,
                ctcode,
                int(np.random.choice(av_choices, p=av_weights)),
                av_date,
                price,
            )
        )  # C_ID, CT_CODE, available, available_date, price

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")

################################################################
## Generating data for CONTACTS
################################################################

# ## CONTACTS HAS THE FOLLOWING COLUMNS:
# ## CONTACT_ID (autoincrement), DIS_ID, f_name, l_name, location, dept, email, phone#

# DIS_ID is random from 1 to 200

# Everything else is random

## Inserting data
sql = "INSERT INTO CONTACTS VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
val = []

for _ in range(1000):
    val.append(
        (
            0,
            np.random.randint(1, 201),
            fake.first_name(),
            fake.last_name(),
            fake.city()[:20],
            np.random.choice(["marketing", "finance", "HR", "tech"]),
            fake.email(),
            np.random.randint(111111, 999999),
        )
    )

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")
