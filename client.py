from tinkoff.invest.services import InstrumentsService
from tinkoff.invest import InstrumentIdType, InstrumentType, TradingDay, GetDividendsResponse, Dividend, Account
from tinkoff.invest import Client, Instrument, typedefs, ShareResponse
from datetime import datetime, timedelta
import pandas as pd

from settings import CLASS_CODE, REESTR_FIGI
class MyClient:
    client = None
    iis_id = ""
    def __init__(self, TOKEN: str):
        self.client = Client(TOKEN).__enter__()
    
    def getTradingSchedules(self, fr: datetime):
        new_date = fr + timedelta(days=13)
        return self.client.instruments.trading_schedules(exchange="MOEX", from_=datetime.now(), to=new_date)

    def UpdateTradeSchedules(self):
        data = self.getTradingSchedules(datetime.now())
        properties = ["date", "is_trading_day", "start_time", "end_time"]
        df = pd.DataFrame({prop: getattr(date, prop) for prop in properties} for date in data.exchanges[0].days)
        df.to_csv("РасписаниеТоргов.csv")

    def getFigi(self, tiker: str):
        return self.client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code=CLASS_CODE, id=tiker).instrument.figi

    def getDiv(self, figi: str) -> list[Dividend]:
        date = datetime.now()
        return self.client.instruments.get_dividends(figi=figi, from_=date, to=date + timedelta(days=30)).dividends

    def UpdateOrderList(self):
        divs_data = []
        for share_figi in REESTR_FIGI:
            for divs in self.getDiv(share_figi):
                divs_data.append(divs.last_buy_date)

    def get_RUB_limits(self, id: str):
        for curr in self.client.operations.get_withdraw_limits(account_id=id).money:
            if (curr.currency == 'rub'):
                return curr

    def get_accounts_id(self):
        id = []
        for acc in self.client.users.get_accounts().accounts:
            id.append((acc.id, acc.name))
        return id

    def getShares(self) -> list[Instrument]:
        shares = []
        for acc in self.client.users.get_accounts().accounts:
            print(acc.id)
            for portfel in self.client.operations.get_portfolio(account_id=acc.id):
                #print(portfel.instrument_type)
                if (portfel.instrument_type == "share"):
                    #print(portfel.ticker)
                    shares.append(self.client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID, id=portfel.instrument_uid).instrument)
        return shares