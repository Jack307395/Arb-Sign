import ccxt
import requests
import time

print("BOT STARTING...")

BOT_TOKEN = "8540273853:AAH8GnAFdI-LRR3H-wg0e1ulxJG77mGSVLE"
CHAT_ID = "5694710315"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
        print("Telegram message sent")
        
    except Exception as e:
        print("Telegram error:", e)

exchanges = {
    "kucoin": ccxt.kucoin({'enableRateLimit': True}),
     "mexc": ccxt.mexc({'enableRateLimit': True}),
    "gateio": ccxt.gateio({'enableRateLimit': True}),
    "htx": ccxt.htx({'enableRateLimit': True}),
    "poloniex":ccxt.poloniex({'enableRateLimit': True}),
    "bitget":ccxt.bitget({'enableRateLimit': True})
}
  
print("Loading markets...")

def get_pairs(ex):
    markets = ex.load_markets()
    return [p for p in markets if p.endswith("/USDT")]

def common_pairs():
    sets = []
    for ex in exchanges.values():
        sets.append(set(get_pairs(ex)))
    return list(set.intersection(*sets))

print("Building pair list...")
pairs = common_pairs()
print("TOTAL PAIRS:", len(pairs))

send("Bot is ONLINE")

while True:

    for pair in pairs:

        prices = {}

        for name, ex in exchanges.items():
            try:
                ticker = ex.fetch_ticker(pair)
                price = ticker.get("last")

                if price and price > 0:
                    prices[name] = price
            except:
                continue

        if len(prices) < 2:
            continue

        buy_ex = min(prices, key=prices.get)
        sell_ex = max(prices, key=prices.get)

        buy = prices[buy_ex]
        sell = prices[sell_ex]

        spread = ((sell - buy) / buy) * 100
        fee = 0.2
        net_profit = spread - fee

        if net_profit >= 1 and spread <= 10:

            msg = (
                "🔥 ARBITRAGE SIGNAL 🔥\n\n"
                f"🪙 {pair}\n\n"
                f"💵 BUY: {buy_ex} @ {buy}\n\n"
                f"💰 SELL: {sell_ex} @ {sell}\n\n"
                f"📈 SPREAD: {round(spread,2)}%\n\n"
                f"💎 NET PROFIT: {round(net_profit,2)}%"
            )

            send(msg)
            time.sleep(2)

    time.sleep(20)