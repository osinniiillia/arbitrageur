import sys
import asyncio
from binance import AsyncClient
import time
import hmac
from requests import Request, Session
import yaml
from yaml.loader import SafeLoader

stream = open('api.yaml', 'r')
api_keys = yaml.load(stream, Loader=SafeLoader)
#получаем ключи из yaml файла
binance_api_key = api_keys['BINANCE']['api_key']
binance_api_secret = api_keys['BINANCE']['api_secret']

ftx_api_key = api_keys['FTX']['api_key']
ftx_api_secret = api_keys['FTX']['api_secret']

async def binance(ticker1, ticker2):

    global binancebid
    global binanceask
    client = await AsyncClient.create(binance_api_key, binance_api_secret)
    #Получаем данные по конкретному тикеру
    res = await client.get_ticker(symbol=f"{ticker1}{ticker2}")
    binancebid = float(res['bidPrice'])
    binanceask = float(res['askPrice'])

    await client.close_connection()

async def ftx(ticker1,ticker2):

    global ftxbid
    global ftxask
    ts = int(time.time() * 1000)
    # получаем данные по конкретному тикеру
    requestFTX = Request('GET', f'https://ftx.us/api/markets/{ticker1}/{ticker2}')
    preparedFTX = requestFTX.prepare()
    #загружаем секретный ключ
    signature_payload = f'{ts}{preparedFTX.method}{preparedFTX.path_url}'.encode()
    signature = hmac.new(ftx_api_secret.encode(), signature_payload, 'sha256').hexdigest()
    #используем US биржу
    requestFTX.headers['FTXUS-KEY'] = ftx_api_key
    requestFTX.headers['FTXUS-SIGN'] = signature
    requestFTX.headers['FTXUS-TS'] = str(ts)
    # извлекаем спрос и предложение
    FTX = Session().send(preparedFTX).json()['result']
    ftxbid = float(FTX['bid'])
    ftxask = float(FTX['ask'])


async def main():

    while True:
        # создаем 2 асинхронные задачи
        task1 = loop.create_task (binance(sys.argv[1],sys.argv[2]))
        task2 = loop.create_task(ftx(sys.argv[1],sys.argv[2]))
        # ожидаем выполнения этих задач
        await asyncio.wait([task1,task2])
        # только после этого производим вычисления
        if (binanceask < ftxbid) or (ftxask < binancebid):
            print(binanceask, '<', ftxbid, '    ', ftxask, '<', binancebid)
            print('ask < bid')



if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except :
        pass