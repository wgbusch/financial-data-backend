from model.Ticker import Ticker


def get_tickers(tickers):
    results = []
    results.append(Ticker("asd1", "ADB1", 1.5))
    results.append(Ticker("asd2", "ADB2", 2.5))
    results.append(Ticker("asd3", "ADB3", 3.5))
    results.append(Ticker("asd4", "ADB4", 4.5))
    return results
