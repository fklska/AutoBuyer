from tinkoff.invest.services import InstrumentsService
from tinkoff.invest import InstrumentIdType, InstrumentType
from tinkoff.invest import Client, Instrument, typedefs, ShareResponse
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
    
    def getFigi(self, tiker: str):
        self.client.instruments.share_by(InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, "????", tiker)
    
    def getShares(self) -> list[Instrument]:
        shares = []
        for acc in self.client.users.get_accounts().accounts:
            print(acc.id)
            for portfel in self.client.operations.get_portfolio(account_id=acc.id).positions:
                #print(portfel.instrument_type)
                if (portfel.instrument_type == "share"):
                    #print(portfel.ticker)
                    shares.append(self.client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID, id=portfel.instrument_uid).instrument)
        return shares