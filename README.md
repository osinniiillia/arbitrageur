# arbitr
<br/>bot arbitrageur for asynchronous parsing of finance and ftx  

<br/>Сравнивает значения best ask и best bid бирж BINANCE и FTX

<br/>Пример запуска 
 > python main.py BTC USDT 
 > docker run osinnii/ticker BTC USDT  
 > docker run 903994d76b01 BTC USDT  
 > > имя образа: 903994d76b01  

Предложения по оптимизации: <br/>
>Написать бот на более "быстром" языке C  
>Многопоточность или асинхронность(применяется)  
>Прокси для более быстрого доступа к серверу  
>Сессии, чтобы не загружать сайт раз за разом  
