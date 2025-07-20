from datetime import datetime
from dotenv import load_dotenv
from client import MyClient
import os

import pandas as pd
load_dotenv()

TOKEN = os.getenv("TOKEN")

client = MyClient(TOKEN)


def main():
    for share in client.getShares():
        print(share.class_code)


if __name__ == "__main__":
    main()
