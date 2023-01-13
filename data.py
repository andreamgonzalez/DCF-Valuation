import yfinance as yf
import pandas as pd
import numpy
import json
import datetime
from decimal import Decimal
from currency_converter import CurrencyConverter
from helper import *
cc = CurrencyConverter()

def get_all_stock_data(ticker):
    ##### Returns basic stock info from api #####

    stock = yf.Ticker(ticker)
    stock_info = stock.get_info()

    basic_info = {
        'name' : stock_info.get('shortName', None),
        'symbol' : stock_info.get('symbol', None),
        'enterprise_to_ebitda' : stock_info.get('enterpriseToEbitda', None),
        'enterprise_to_revenue' : stock_info.get('enterpriseToRevenue', None),
        'enterpriseValue' : stock_info.get('enterpriseValue', None),
        'website' : stock_info.get('website', None),
        'summary' : stock_info.get('longBusinessSummary', None),
    }
    
    return basic_info

def get_historical_financials_api(ticker):
    ##### Returns a list of all financials available from api#####

    stock = yf.Ticker(ticker)

    stock_is = stock.get_income_stmt().to_dict()
    stock_cf = stock.get_cashflow().to_dict()
    stock_bs = stock.get_balance_sheet().to_dict()
    
    today = datetime.date.today()
    year = today.year

    historical_financials_list = []

    #loops through each period in dictionary
    for i in range(len(stock_cf)):
        year -=1
        stock_is_key = list(stock_is.keys())[i]
        stock_is_data = stock_is[stock_is_key]

        stock_cf_key = list(stock_cf.keys())[i]
        stock_cf_data = stock_cf[stock_cf_key]

        stock_bs_key = list(stock_bs.keys())[i]
        stock_bs_data = stock_bs[stock_bs_key]

#checks value exists #############################################################################
    ##### Income Statement figures
        
        if not 'TotalRevenue' in stock_is_data:
            TotalRevenue = 0
        TotalRevenue = str(stock_is_data["TotalRevenue"])

        if not 'CostOfRevenue' in stock_is_data:
            CostOfRevenue = 0
        CostOfRevenue = str(stock_is_data["CostOfRevenue"])
        
        if not 'GrossProfit' in stock_is_data:
            GrossProfit = 0
        GrossProfit = str(stock_is_data["GrossProfit"])
        
        if not 'InterestExpense' in stock_is_data:
            InterestExpense = 0
        InterestExpense = str(stock_is_data["InterestExpense"])

        if not 'OperatingExpense' in stock_is_data:
            OperatingExpense = 0
        OperatingExpense = str(stock_is_data["OperatingExpense"])
        
        if not 'OperatingIncome' in stock_is_data:
            OperatingIncome = 0
        OperatingIncome = str(stock_is_data["OperatingIncome"])
        
        if not 'EBIT' in stock_is_data:
            EBIT = 0
        EBIT = str(stock_is_data["EBIT"])

        if not 'PretaxIncome' in stock_is_data:
            PretaxIncome = 0
        PretaxIncome = str(stock_is_data["PretaxIncome"])
        
        if not 'TaxProvision' in stock_is_data:
            TaxProvision = 0
        TaxProvision = str(stock_is_data["TaxProvision"])
        
        if not 'NetIncome' in stock_is_data:
            NetIncome = 0
        NetIncome = str(stock_is_data["NetIncome"])

    ###### Cash Flow Figures
        if not 'OperatingCashFlow' in stock_cf_data:
            OperatingCashFlow = 0
        OperatingCashFlow = str(stock_cf_data["OperatingCashFlow"])
        
        if not 'DeferredTax' in stock_cf_data:
            DeferredTax = 0
        DeferredTax = str(stock_cf_data["DeferredTax"])
        
        if not 'ChangeInInventory' in stock_cf_data:
            ChangeInInventory = 0
        ChangeInInventory = str(stock_cf_data.get("ChangeInInventory"))

        if not 'ChangeInAccountPayable' in stock_cf_data:
            ChangeInAccountPayable = 0
        ChangeInAccountPayable = str(stock_cf_data["ChangeInAccountPayable"])
        
        if not 'ChangeInReceivables' in stock_cf_data:
            ChangeInReceivables = 0
        ChangeInReceivables = str(stock_cf_data.get("ChangeInInventory"))
        
        if not 'DepreciationAndAmortization' in stock_cf_data:
            DepreciationAndAmortization = 0
        DepreciationAndAmortization = str(stock_cf_data["DepreciationAndAmortization"])
        
        if not 'InvestingCashFlow' in stock_cf_data:
            InvestingCashFlow = 0
        InvestingCashFlow = str(stock_cf_data["InvestingCashFlow"])
        
        if not 'CapitalExpenditure' in stock_cf_data:
            CapitalExpenditure = 0
        CapitalExpenditure = str(stock_cf_data["CapitalExpenditure"])

        if not 'ChangeInWorkingCapital' in stock_cf_data:
            ChangeInWorkingCapital = 0
        ChangeInWorkingCapital = str(stock_cf_data["ChangeInWorkingCapital"])

        ##### Balance Sheet Figures

        if not 'LongTermDebt' in stock_bs_data:
            LongTermDebt = 0
        LongTermDebt = str(stock_bs_data["LongTermDebt"])
        
        if not 'CashCashEquivalentsAndShortTermInvestments' in stock_bs_data:
            cc = 0
        cc = str(stock_bs_data["CashCashEquivalentsAndShortTermInvestments"])
        
 # ends value exists check ################################################################################      
        
        #creates a dictionary of financials per period returned from api
        period = (str(list(stock_is.keys())[i]))[:4]

        historical_financials = {
            'period' : period,
            'total_revenue' : TotalRevenue, 
            'cost_of_revenue' : CostOfRevenue, 
            'gross_income' : GrossProfit,
            'interest_exp' : InterestExpense,
            'operating_expenses' : OperatingExpense,
            'operating_income' : OperatingIncome,
            'ebit' : EBIT,
            'taxes' : TaxProvision,
            'net_income' : NetIncome,
            'operating_cashflow' : OperatingCashFlow,
            'deferred_tax' : DeferredTax,
            'change_inventory' : ChangeInInventory,
            'change_ap' : ChangeInAccountPayable,
            'change_ar' : ChangeInReceivables,
            'depreciation_amortization' : DepreciationAndAmortization,
            'investment_cashflows' : InvestingCashFlow,
            'capex' : CapitalExpenditure,
            'change_working_capital' : ChangeInWorkingCapital,
            'cash_equivs_mkt_securities' : cc,
            'long_term_debt' : LongTermDebt,
            }

        historical_financials_list.append(historical_financials)
        
    return historical_financials_list

def get_last_historical_record(ticker):
    ##### Only gets the latest/most recent financial record from api #####

    stock = yf.Ticker(ticker)
    stock_is = stock.get_income_stmt().to_dict()
    stock_is_key = list(stock_is.keys())[0]
    stock_is_data = stock_is[stock_is_key]
    stock_cf = stock.get_cashflow().to_dict()
    stock_cf_key = list(stock_cf.keys())[0]
    stock_cf_data = stock_cf[stock_cf_key]
    stock_bs = stock.get_balance_sheet().to_dict()
    stock_bs_key = list(stock_bs.keys())[0]
    stock_bs_data = stock_bs[stock_bs_key]

    hist_financials = {
        'total_revenue' : str(stock_is_data["TotalRevenue"]),
        'ebit' : str(stock_is_data["EBIT"]),
        'taxes' : str(stock_is_data["TaxProvision"]),
        'depreciation_amortization' : str(stock_cf_data["DepreciationAndAmortization"]),
        'capex' : str(stock_cf_data["CapitalExpenditure"]),
        'change_working_capital' : str(stock_cf_data["ChangeInWorkingCapital"]),
        'cash_equivs_mkt_securities' : str(stock_bs_data["CashCashEquivalentsAndShortTermInvestments"]),
        'long_term_debt' : str(stock_bs_data["LongTermDebt"]),
        }

    return hist_financials

def get_first_historical_record(ticker):
    ##### Only gets the first/oldest financial record from api #####
    stock = yf.Ticker(ticker)
    stock_is = stock.get_income_stmt().to_dict()
    stock_is_key = list(stock_is.keys())[-1]
    stock_is_data = stock_is[stock_is_key]
    stock_cf = stock.get_cashflow().to_dict()
    stock_cf_key = list(stock_cf.keys())[-1]
    stock_cf_data = stock_cf[stock_cf_key]
    stock_bs = stock.get_balance_sheet().to_dict()
    stock_bs_key = list(stock_bs.keys())[-1]
    stock_bs_data = stock_bs[stock_bs_key]


    hist_financials = {
        'total_revenue' : str(stock_is_data["TotalRevenue"]),
        'ebit' : str(stock_is_data["EBIT"]),
        'taxes' : str(stock_is_data["TaxProvision"]),
        'depreciation_amortization' : str(stock_cf_data["DepreciationAndAmortization"]),
        'capex' : str(stock_cf_data["CapitalExpenditure"]),
        'change_working_capital' : str(stock_cf_data["ChangeInWorkingCapital"]),
        'cash_equivs_mkt_securities' : str(stock_bs_data["CashCashEquivalentsAndShortTermInvestments"]),
        'long_term_debt' : str(stock_bs_data["LongTermDebt"]),
        }

    return hist_financials
######################################################################################################

# Below are some helper functions that are for getting direct api json responses to appear in some routes

def get_stock_info(ticker):
    """Return stock info"""
    stock = yf.Ticker(ticker)
    stock_info = convert_keys_to_str(stock.info)
    return stock_info

def get_cash_flow(ticker):
    """Return stock cash flow object"""
    stock = yf.Ticker(ticker)
    stock_cashflow = list(stock.cash_flow)
    return stock_cashflow

def get_income_stmt(ticker):
    """Return stock income statement object"""
    stock = yf.Ticker(ticker)
    stock_income_stmt = convert_keys_to_str(stock.income_stmt)
    return stock_income_stmt

def get_balance_sheet(ticker):
    """Return stock balance sheet object"""
    stock = yf.Ticker(ticker)
    stock_balance_sheet = convert_keys_to_str(stock.balance_sheet)
    return stock_balance_sheet

def get_revenue_forecast(ticker):
    """Return stock revenue forecast object"""
    stock = yf.Ticker(ticker)
    stock_revenue_forecast = convert_keys_to_str(stock.revenue_forecast)
    return stock_revenue_forecast

def get_stock_shares(ticker):
    """Return stock shares object"""
    stock = yf.Ticker(ticker)
    stock_shares = convert_keys_to_str(stock.shares)
    return stock_shares
