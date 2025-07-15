from datetime import datetime
from dotenv import load_dotenv
from client import MyClient
import os

import pandas as pd
load_dotenv()

TOKEN = os.getenv("TOKEN")

client = MyClient(TOKEN)


def main():
    #print(datetime.now())
    data = client.getTradingSchedules(datetime.now())
    df = pd.DataFrame([vars(date) for date in data.exchanges[0].days])
    df.to_csv("РасписаниеТоргов.csv")
    print(df)



if __name__ == "__main__":
    main()
