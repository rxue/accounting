import certifi
from html.parser import HTMLParser
import pycurl
from io import BytesIO

from investment.company.models import CompanyCode
from investment.holdings.market_quote.model import Price


def _fetch_html(ticker: str) -> str:
    url = f"https://www.google.com/finance/quote/{ticker}"
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.HTTPHEADER, ["User-Agent: curl/8.5.0"])
    c.perform()
    c.close()
    return buffer.getvalue().decode("utf-8")


class _AttributeFinder(HTMLParser):
    def __init__(self, keyword: str):
        super().__init__()
        self.keyword = keyword
        self.value: str | None = None

    def handle_starttag(self, tag, attrs):
        if self.value is None:
            attrs_dict = dict(attrs)
            if self.keyword in attrs_dict:
                self.value = attrs_dict[self.keyword]


def _find_element_by_keyword(html: str, keyword: str) -> str | None:
    finder = _AttributeFinder(keyword)
    finder.feed(html)
    return finder.value


def get_stock_price(company_code: CompanyCode, keyword: str = "data-last-price") -> Price | None:
    html = _fetch_html(company_code)
    price = _find_element_by_keyword(html, keyword)
    if price is None:
        return None
    timestamp_val = _find_element_by_keyword(html, "data-last-normal-market-timestamp")
    timezone_offset_val = _find_element_by_keyword(html, "data-tz-offset")
    return Price(value=price,
                 currency=_find_element_by_keyword(html, "data-currency-code"),
                 last_timestamp=int(timestamp_val),
                 timezone_offset=int(timezone_offset_val))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m investment.holdings.market_quote.google_finance_fetcher <company_code>")
        print()
        print("  <company_code>  ticker_symbol:stock_exchange_symbol")
        print("  Example:        FORTUM:HEL")
        sys.exit(1)
    ticker, stock_exchange_symbol = sys.argv[1].split(":")
    result = get_stock_price(CompanyCode(ticker_symbol=ticker, stock_exchange_symbol=stock_exchange_symbol))
    print(result)
