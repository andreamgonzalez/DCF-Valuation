from unittest import TestCase
from dcf import project_dcf


class ProjectDcfTestCase(TestCase):
    def setUp(self):
        # free cash flow works out to 13% of revenue, and with growth equal
        # to WACC every year discounts back to the same 130
        self.inputs = {
            'revenue' : 1000,
            'cash' : 100,
            'debt' : 50,
            'shares' : 10,
            'growth_rate' : 0.10,
            'ebit_rate' : 0.20,
            'tax_rate' : 0.25,
            'depr_amort_rate' : 0.05,
            'capex_rate' : 0.06,
            'nwc_rate' : 0.01,
            'wacc' : 0.10,
            'tgr' : 0.02,
        }

    def test_first_period_financials(self):
        first = project_dcf(**self.inputs)['periods'][0]

        self.assertEqual(first['period'], 1)
        self.assertAlmostEqual(first['total_revenue'], 1100)
        self.assertAlmostEqual(first['ebit'], 220)
        self.assertAlmostEqual(first['taxes'], 55)
        self.assertAlmostEqual(first['ebiat'], 165)
        self.assertAlmostEqual(first['depreciation_amortization'], 55)
        self.assertAlmostEqual(first['capex'], 66)
        self.assertAlmostEqual(first['change_working_capital'], 11)
        self.assertAlmostEqual(first['unlevered_cf'], 143)
        self.assertAlmostEqual(first['pv_unlevered_cf'], 130)

    def test_projects_five_periods(self):
        periods = project_dcf(**self.inputs)['periods']

        self.assertEqual([p['period'] for p in periods], [1, 2, 3, 4, 5])
        self.assertAlmostEqual(periods[4]['total_revenue'], 1000 * 1.1 ** 5)
        for p in periods:
            self.assertAlmostEqual(p['pv_unlevered_cf'], 130)

    def test_valuation_totals(self):
        result = project_dcf(**self.inputs)

        self.assertAlmostEqual(result['terminal_value'], 130 * 1.1 ** 5 * 1.02 / 0.08)
        self.assertAlmostEqual(result['pv_terminal_value'], 1657.5)
        self.assertAlmostEqual(result['enterprise_value'], 5 * 130 + 1657.5)
        self.assertAlmostEqual(result['equity_value'], 2357.5)
        self.assertAlmostEqual(result['share_price'], 235.75)

    def test_wacc_must_be_greater_than_terminal_growth(self):
        self.inputs['tgr'] = 0.10
        with self.assertRaises(ValueError):
            project_dcf(**self.inputs)

    def test_shares_must_be_positive(self):
        self.inputs['shares'] = 0
        with self.assertRaises(ValueError):
            project_dcf(**self.inputs)

    def test_missing_financials_are_rejected(self):
        self.inputs['revenue'] = float('nan')
        with self.assertRaises(ValueError):
            project_dcf(**self.inputs)
