# 20260213
## pyproject.toml is as per project => it is impossible to define multiple projects in pyproject.toml
tried error: `pip._vendor.tomli.TOMLDecodeError: Cannot declare ('project',) twice (at line 12, column 9)`

# 20260303
## Question: Does my company need Double-entry or Single-enty bookkeeping?
Based on https://www.vero.fi/en/businesses-and-corporations/business-operations/setting-up-a-business/accounting-financial-year-tax-period/ my company is not toiminimi => needs ~~single-entry bookkeeping~~ double-entry bookkeeping

## Question: what attachments are needed when reporting tax
Answer: https://www.vero.fi/yritykset-ja-yhteisot/verot-ja-maksut/osakeyhtio-ja-osuuskunta/veroilmoitus/ilmoittamisen-ohje/#Tilinpaatostiedot

=> need tilinpäätös:
* income statement
* balance sheet

## [Cash Accounting](https://www.youtube.com/watch?v=8t9PFHlLLVI) (probably irrelevant to my company)
* Transactions are only recorded when cash changes hands
* revenue is recognized once cash is received
* expenses are recorded once cash is paid out

# 20260304
## revisit [tutorial about pyproject](https://www.youtube.com/watch?v=v6tALyc4C10&t=1375s&pp=0gcJCTAAlc8ueATH)
### [*src-layout*](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout)
### [*flat-layout*](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#flat-layout)

> This layout is very practical for using the [*REPL*](https://peps.python.org/pep-0762/)

Moreover, Gemini suggested when to use flat-layout:

* Simple Projects: For small scripts, personal tools, or tutorials where you want the lowest barrier to entry.

* Beginners: It’s intuitive because what you see is what you get.

* Non-distributed code: If you aren’t planning to upload the code to PyPI and just want to run it locally.

**So as to my current SIMPLE project, *flat-layout* suffices**

# 20260307
Plan of checksum:
cash infusion + (dividend gross value - withholding tax) + trading income - expense = cash in account + sum of book value in remaining lots

# 20260315
## AI Prompt
add to tax_report/pdf_generation/pdf_generator.py a function called generate_ListOfSecuritesAndBookEntrySharesTable(), it takes list[SecurityAndBookEntrySharesDTO] as the 1st argument and output_path as the second argument. The implementation generation List of Securities And Book Entry Shares table into a pdf file in the given output path, the table has the following columns
* name of company or cooperative
* Business Id
* Share quantity
* Undepreciated acquisition cost for purposes of income tax
* Comparison value per unit
* Comparison value in total

# 20260317
## Python learning tips
In Python, the name of a *module*, i.e. a Python file, is rarely named with verb. This is logic when taking the functions inside the module into consideration. Functions inside a Python module is named with verb by nature, so if the module is also named with verb, it is against intuition

# 20260430
Google Finance is not a good source to get the stock quotes. The daily change rate on the Google Finance page is parsed from Javascript, but the *pycurl* by nature is not parsing Javascript
