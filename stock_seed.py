from app import db, Stock

db.drop_all()
db.create_all()


stock1 = Stock(symbol="MSFT")
stock2 = Stock(symbol="NFLX")
stock3 = Stock(symbol="AMZN")
stock4 = Stock(symbol="GOOG")
stock5 = Stock(symbol="TSLA")
stock6 = Stock(symbol="M")
stock7 = Stock(symbol="INTC")
stock8 = Stock(symbol="BIIB")
stock9 = Stock(symbol="PRTY")
stock10 = Stock(symbol="AAPL")
stock11 = Stock(symbol="AMEX")

db.session.add_all([stock1, stock2, stock3, stock4, stock5, stock6, stock7, stock8, stock9, stock10, stock11])
db.session.commit()