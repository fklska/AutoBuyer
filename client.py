from tinkoff.invest.services import InstrumentsService
from tinkoff.invest import Client
from datetime import datetime, timedelta
import pandas as pd

class MyClient:
    client = None

    def __init__(self, TOKEN: str):
        self.client = Client(TOKEN).__enter__()
    
    def getTradingSchedules(self, fr: datetime):
        new_date = fr + timedelta(days=13)
        return self.client.instruments.trading_schedules(exchange="MOEX", from_=datetime.now(), to=new_date)


    def saveTradeSchedules(self):
        data = self.getTradingSchedules(datetime.now())
        df = pd.DataFrame([vars(date) for date in data.exchanges[0].days])
        df.to_csv("РасписаниеТоргов.csv")
        