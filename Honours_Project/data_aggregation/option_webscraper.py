from requests_html import HTMLSession

# Target https://www.barchart.com/stocks/quotes/stock/options

link = """https://www.barchart.com/stocks/quotes/{ticker}/options?expiration={expiration_date}-m&view={frmat}&moneyness={moneyness}"""

