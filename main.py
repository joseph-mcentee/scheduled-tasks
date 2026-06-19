import datetime as dt
import random
import pandas
import smtplib
import os

my_email = os.environ.get("my_email")
password = os.environ.get("password")

today = dt.datetime.now()
today_month = today.month
today_day = today.day

with open("birthdays.csv", "r") as file:
    birthdays = pandas.read_csv(file)
    birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in birthdays.iterrows()}

if (today_month, today_day) in birthdays_dict:
    birthday_person = birthdays_dict[(today_month, today_day)]
    if (today_month, today_day) == (5, 7):
        file_path = "./letter_templates/letter_4.txt"
    else:
        file_path = f"./letter_templates/letter_{random.randint(1, 3)}.txt"
        with open(file_path) as file:
            contents = file.read()
            birthday_wish = contents.replace("[NAME]", birthday_person["name"])

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=birthday_person["email"],
                                msg=f"Subject: HAPPY BIRTHDAY!\n\n{birthday_wish}")
