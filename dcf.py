"""Discounted cash flow math. No database or api calls happen in here."""

import math

PROJECTION_YEARS = 5


def project_dcf(revenue, cash, debt, shares, growth_rate, ebit_rate, tax_rate,
                depr_amort_rate, capex_rate, nwc_rate, wacc, tgr, years=PROJECTION_YEARS):
    """Projects unlevered free cash flows and values the company off of them.

    revenue, cash and debt come from the latest reported year.
    All rates are decimals (0.08 for 8%) and mean the following:

        growth_rate      - revenue growth year over year
        ebit_rate        - EBIT as a share of revenue
        tax_rate         - taxes as a share of EBIT
        depr_amort_rate  - D&A as a share of revenue
        capex_rate       - capital expenditures as a share of revenue
        nwc_rate         - increase in net working capital as a share of revenue
        wacc             - discount rate
        tgr              - terminal growth rate

    Capex and the increase in working capital are entered as positive rates
    and are subtracted from the cash flow.

    Returns a dictionary with one entry per projected year under 'periods',
    plus the terminal value, enterprise value, equity value and share price.
    Raises ValueError if the inputs can not produce a valuation.
    """
    inputs = [revenue, cash, debt, shares, growth_rate, ebit_rate, tax_rate,
              depr_amort_rate, capex_rate, nwc_rate, wacc, tgr]
    if not all(math.isfinite(value) for value in inputs):
        raise ValueError("All financials and assumptions must be numbers.")
    if shares <= 0:
        raise ValueError("Shares must be greater than zero.")
    if wacc <= tgr:
        raise ValueError("WACC must be greater than the terminal growth rate.")

    periods = []
    total_pv_unlevered_cf = 0

    for p in range(1, years + 1):
        revenue = revenue * (1 + growth_rate)
        ebit = revenue * ebit_rate
        taxes = ebit * tax_rate
        ebiat = ebit - taxes
        depreciation_amortization = revenue * depr_amort_rate
        capex = revenue * capex_rate
        change_working_capital = revenue * nwc_rate

        unlevered_cf = ebiat + depreciation_amortization - capex - change_working_capital
        pv_unlevered_cf = unlevered_cf / pow(1 + wacc, p)
        total_pv_unlevered_cf += pv_unlevered_cf

        periods.append({
            'period' : p,
            'total_revenue' : revenue,
            'ebit' : ebit,
            'taxes' : taxes,
            'ebiat' : ebiat,
            'depreciation_amortization' : depreciation_amortization,
            'capex' : capex,
            'change_working_capital' : change_working_capital,
            'unlevered_cf' : unlevered_cf,
            'pv_unlevered_cf' : pv_unlevered_cf,
        })

    # terminal value is based on the last projected year only
    terminal_value = (unlevered_cf * (1 + tgr)) / (wacc - tgr)
    pv_terminal_value = terminal_value / pow(1 + wacc, years)

    enterprise_value = total_pv_unlevered_cf + pv_terminal_value
    equity_value = enterprise_value + cash - debt
    share_price = equity_value / shares

    return {
        'periods' : periods,
        'terminal_value' : terminal_value,
        'pv_terminal_value' : pv_terminal_value,
        'enterprise_value' : enterprise_value,
        'equity_value' : equity_value,
        'share_price' : share_price,
    }
