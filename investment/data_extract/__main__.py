from investment.data_extract.nordea_holdings_extractor import extract_from_excel

holdings = extract_from_excel("data/nordea_omistukset.xlsx")
for h in holdings:
    print(h)
