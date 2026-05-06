from unittest.mock import patch

import investment.holdings.company.repository as repo
from investment.holdings.company.repository import find_company_name_by_symbol


def test_find_company_name_by_symbol_existing():
    with patch.object(repo, "companies_cache", {"PFE": "Pfizer Inc"}):
        assert find_company_name_by_symbol("PFE") == "Pfizer Inc"

def test_find_company_name_by_symbol_not_exist():
    with patch.object(repo, "companies_cache", {}):
        assert find_company_name_by_symbol("PFE") == None
