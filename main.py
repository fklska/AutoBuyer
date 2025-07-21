from datetime import datetime
from dotenv import load_dotenv
from client import MyClient
from settings import REESTR_TICKER
import os

import pandas as pd
load_dotenv()

TOKEN = os.getenv("TOKEN")
IIS_ID = os.getenv("IIS_ID")

client = MyClient(TOKEN)
client.iis_id = IIS_ID

def main():
    print(client.get_RUB_limits(IIS_ID))


def pipeline():
    pass

def updateFigiReestr():
    reestr = []
    for ticker in REESTR_TICKER:
        reestr.append(client.getFigi(ticker))
    print(reestr)

if __name__ == "__main__":
    main()
