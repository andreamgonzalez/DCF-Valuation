"""SQLAlchemy models for DCF."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from data import *
from helper import *
import random
from datetime import date


bcrypt = Bcrypt()
db = SQLAlchemy()
today = datetime.date.today()
############################# User Model ###########################################
class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text)
    favorites = db.relationship("Stock", secondary="favorite_stocks")
    

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

############################## Financial Model ######################

class Financial(db.Model):
    """saves stock financials collected from api and stores values for historic financials analysis"""

    __tablename__ = 'financials'

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer)
    date_updated = db.Column(db.Date)
    symbol = db.Column(db.Text)
    total_revenue = db.Column(db.Float)
    ebit = db.Column(db.Float)
    taxes = db.Column(db.Float)
    ebiat = db.Column(db.Float)
    depreciation_amortization = db.Column(db.Float)
    capex = db.Column(db.Float)
    change_working_capital = db.Column(db.Float)
    unlevered_cf = db.Column(db.Float)
    cash = db.Column(db.Float)
    debt = db.Column(db.Float)
    growth_rate = db.Column(db.Numeric(precision=10, scale=2))
    ebit_rate = db.Column(db.Numeric(precision=10, scale=2))
    taxes = db.Column(db.Numeric(precision=10, scale=2))
    depreciation_amorization_rate= db.Column(db.Numeric(precision=10, scale=2))
    depreciation_amorization_rate_capex = db.Column(db.Numeric(precision=10, scale=2))
    capex_rate = db.Column(db.Numeric(precision=10, scale=2))
    change_nwc_rate = db.Column(db.Numeric(precision=10, scale=2))
    change_nwc_change_rev = db.Column(db.Numeric(precision=10, scale=2))


    @classmethod
    def get_all_historical_financials(cls, symbol):
        """Fetch historical financials from api for each historic period"""
        prior_financials = list(get_historical_financials_api(symbol))
        converted_floats = convert_values_to_floats(prior_financials)
        financials = list(reversed(converted_floats))
        return financials


############################### Stock Model #########################

class Stock(db.Model):
    """All Stocks fetched and stored from API"""

    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    date_updated = db.Column(db.Date)
    name = db.Column(db.Text)
    symbol = db.Column(db.Text)
    enterprise_to_ebitda = db.Column(db.Float)
    enterprise_to_revenue  = db.Column(db.Float)
    enterpriseValue = db.Column(db.Float)

    @classmethod
    def get_stock_info(cls, ticker):
        """ Get stock info from api"""
        stock_info = get_stock_info(ticker)
        return stock_info

    @classmethod
    def get_stock_cashflow(cls, ticker):
        """ Get stock cashflow from api"""
        stock_cashflow = get_cash_flow(ticker)
        return stock_cashflow
    
    @classmethod
    def get_stock_balance_sheet(cls, ticker):
        """ Get stock balance sheet from api"""
        stock_balance_sheet = get_balance_sheet(ticker)
        return stock_balance_sheet

    @classmethod
    def get_stock_income_stmt(cls, ticker):
        """ Get stock income statement from api"""
        stock_income_stmt = get_income_stmt(ticker)
        return stock_income_stmt

    @classmethod
    def get_stock_shares(cls, ticker):
        """ Get stock shares from api"""
        stock_shares = get_stock_shares(ticker)
        return stock_shares

    @classmethod
    def get_stock_data(cls, ticker):
        """Get stock data from api"""

        stock_data = get_all_stock_data(ticker)
        return stock_data
    
    ##### The below Functions not implemented yet ######
    @classmethod
    def search(cls, ticker):
        """ Find stock with `ticker` in the database.

        This is a class method (call it on the class, not an individual stock.)
        It searches for a stock whose ticker matches this ticker
        and, if it finds such a stock, returns that stock object.

        If not found, returns False.


        This is not currently an implemented feature as stock info as of now
        is not stored in db and instead called from the api with below function.
        """
        stock = cls.query.filter_by(symbol=ticker).first()

        if stock:
            return stock
        return False

    @classmethod
    def save_stock_data(cls, ticker):
        """Save stock data from api to database
        
        This function is not currently implemented.
        All data called directly from api and not saved until valuations have been calculated.
        """

        stock_data = list(get_all_stock_data(ticker))

        if stock_data:
            stock = Stock(
                name = stock_data['name'],
                symbol = stock_data['symbol'],
                enterprise_to_ebitda = stock_data['enterprise_to_ebitda'],
                enterprise_to_revenue = stock_data['enterprise_to_revenue'],
                enterpriseValue = stock_data['enterpriseValue'],
                date_updated = date.today()
            )

        
            for i in range(len(get_cash_flow(ticker))):
                total_revenue = stock_data['total_revenue'][i]
                ebiat = stock_data['ebit'][i] - stock_data['taxes'][i]
                unlevered_cf = stock_data['ebit'][i] + stock_data['depreciation_amortization'][i] - stock_data['capex'][i] - stock_data['change_working_capital'][i]
                rate_growth = stock_data['total_revenue'][i+1] / stock_data['total_revenue'][i]
                rate_ebit = stock_data['ebit'][i] / stock_data['total_revenue'][i]
                rate_tax = stock_data['taxes'][i] / stock_data['ebit'][i]
                rate_depr_amort = stock_data['depreciation_amortization'][i] / stock_data['total_revenue'][i]
                rate_depr_amort_capex = stock_data['depreciation_amortization'][i] / stock_data['capex'][i]
                rate_capex = stock_data['capex'][i] / stock_data['total_revenue'][i]
                rate_change_nwc = stock_data['change_working_capital'][i] / stock_data['total_revenue'][i]
                # calculates working capital as it relates to the change in revenue (rather than actual revenue by year as above)
                rate_change_nwc_from_rev = stock_data['change_working_capital'][i] / ( stock_data['total_revenue'][i+1] - stock_data['total_revenue'][i])
                
                
                financial = Financial(
                    period = i,
                    date_updated = date.today(),
                    symbol = stock_data['symbol'][i],
                    total_revenue = stock_data['total_revenue'][i],
                    ebit = stock_data['ebit'][i],
                    taxes = stock_data['taxes'][i],
                    ebiat = ebiat, #calculated above
                    depreciation_amortization = stock_data['depreciation_amortization'][i],
                    capex = stock_data['capex'][i],
                    change_working_capital = stock_data['change_working_capital'][i],
                    unlevered_cf = unlevered_cf, #calculated above
                    cash = stock_data['cash_equivs_mkt_securities'][i],
                    debt = stock_data['long_term_debt'][i],
                    
                    #rates calculated above
                    growth_rate = rate_growth,
                    ebit_rate = rate_ebit,
                    tax_rate = rate_tax,
                    depreciation_amorization_rate = rate_depr_amort,
                    depreciation_amorization_rate_capex = rate_depr_amort_capex,
                    capex_rate = rate_capex,
                    change_nwc_rate = rate_change_nwc,
                    change_nwc_change_rev = rate_change_nwc_from_rev
                )
                db.session.add(financial)
            db.session.add(stock)
            db.session.commit()
            return stock
        return None
    

####################  Valuation Model  ##############################


class Valuation(db.Model):
    """Stores calculated user valuations as per their assumptions"""

    __tablename__ = 'user_valuations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    valuation_name = db.Column(db.Text)
    valuation_id = db.Column(db.Integer)
    period = db.Column(db.Integer)
    date_updated = db.Column(db.Integer)
    symbol = db.Column(db.Text)

    ##### Calculated Predictions ####
    total_revenue = db.Column(db.Float)
    ebit = db.Column(db.Float)
    taxes = db.Column(db.Float)
    ebiat = db.Column(db.Float) 
    depreciation_amortization = db.Column(db.Float)
    capex = db.Column(db.Float)
    change_working_capital = db.Column(db.Float)
    unlevered_cf = db.Column(db.Float)
    pv_unlevered_cf_total = db.Column(db.Float)
    terminal_value = db.Column(db.Float)
    pv_terminal_value = db.Column(db.Float)
    enterprise_val = db.Column(db.Float)
    equity_value = db.Column(db.Float)
    share_price = db.Column(db.Float)

    #### user assumptions ####
    growth_rate = db.Column(db.Numeric(precision=10, scale=2))
    ebit_rate = db.Column(db.Numeric(precision=10, scale=2))
    tax_rate = db.Column(db.Numeric(precision=10, scale=2))
    depreciation_amorization_rate= db.Column(db.Numeric(precision=10, scale=2))
    capex_rate = db.Column(db.Numeric(precision=10, scale=2))
    change_nwc_rate = db.Column(db.Numeric(precision=10, scale=2))
    wacc = db.Column(db.Numeric(precision=10, scale=2))
    tgr = db.Column(db.Numeric(precision=10, scale=2))
    
    shares = db.Column(db.Integer)
        
    ####  Valuation Calculations ####
    ebiat = db.Column(db.Float)
    unlevered_cf = db.Column(db.Float)
    pv_unlevered_cf = db.Column(db.Float)

    terminal_value = db.Column(db.Float)
    pv_terminal_value = db.Column(db.Float)

    enterprise_value = db.Column(db.Float)
    equity_value = db.Column(db.Float)
    shares = db.Column(db.Float)
    share_price = db.Column(db.Float)

    def __repr__(self):
        return f"<User #{self.id}>"

    @classmethod
    def calculate_user_valuation(cls, symbol, revenue_growth, ebit_rate, tax_rate, depr_amort_rate, capex_rate, nwc, wacc, tgr, shares):
        """calculates valuation but does not save to db, daving to db is a user privileged feature"""

        # converts assumptions to percentages for calculations
        growth_rate = float(revenue_growth/100)
        ebit_rate = float(ebit_rate/100)
        tax_rate = float(tax_rate/100)
        depreciation_amorization_rate = float(depr_amort_rate/100)
        capex_rate = float(capex_rate/100)
        nwc = float(nwc/100)
        wacc = float(wacc/100)
        tgr = float(tgr/100)
        shares = float(shares)
        
        valuation_id = random.randint(0, 4000)

        ############ Calculates predictions into future periods (for total of 5 periods)
        
        # all records from newest to oldest
        records= get_historical_financials_api(symbol)      

        #holds all period predictions
        per_period_predictions=[]
        per_period_financials = []
       
        ## first calculation based on latest financials from api
        lp = 0
        
        tr= float(records[lp].get('total_revenue'))
        ebt= float(records[lp].get('ebit'))
        txs= float(records[lp].get('taxes'))
        da = float(records[lp].get('depreciation_amortization'))
        cpx = float(records[lp].get('capex'))
        cwc = float((records[lp].get('change_working_capital')))
        csh = float(records[lp].get('cash_equivs_mkt_securities'))
        dbt = float(records[lp].get('long_term_debt'))
        
        # gets latest year financials for beginning calculations
        ly = {
            'total_revenue' : tr,
            'ebit' : ebt,
            'taxes' : txs,
            'depreciation_amortization' : da,
            'capex': cpx,
            'change_working_capital': cwc,
            'cash' : csh,
            'debt' : dbt
        }
        per_period_financials.append(ly)


        #sums predicted unlevered free cash flows
        total_predicted_cfs = 0
        predicted_unlevered_cfs = []

        for i in predicted_unlevered_cfs:
            total_predicted_cfs += predicted_unlevered_cfs['pv_unlevered_cf'][i]

        
        for i in range(6):
            #calculations for each period
            
            p = i+1
    
            total_revenue = per_period_financials[i].get('total_revenue') * (1 + growth_rate)
            ebit = per_period_financials[i].get('ebit') * (1 + ebit_rate)
            taxes = per_period_financials[i].get('taxes') * (1 + tax_rate)
            ebiat = per_period_financials[i].get('ebit') - per_period_financials[i].get('taxes')
            depreciation_amortization = per_period_financials[i].get('depreciation_amortization') * (1 + depreciation_amorization_rate)
            capex = per_period_financials[i].get('capex') * (1 + capex_rate)
            change_working_capital = per_period_financials[i].get('change_working_capital') * (1 + nwc)
            
            unlevered_cf = per_period_financials[i].get('ebit') + per_period_financials[i].get('depreciation_amortization') - per_period_financials[i].get('capex') - per_period_financials[i].get('change_working_capital')
            present_value_unlevered_cf = unlevered_cf  / pow((1+wacc),(p))
            
            terminal_value = ( unlevered_cf * (1+tgr)) / ((wacc-tgr) + .00001)
            present_value_terminal_value = ( terminal_value / pow((1+wacc),(p)) )
            
            #uses both previous and current ucf's
            enterprise_value = (total_predicted_cfs + unlevered_cf) + present_value_terminal_value
            
            equity_value = enterprise_value + per_period_financials[0].get('cash') - per_period_financials[0].get('debt') 
            share_price = equity_value / shares
            
            cfs = {
                'pv_unlevered_cf' : present_value_unlevered_cf
            }

            predicted_unlevered_cfs.append(cfs)

            #stores values in dictionary
            period_prediction = {
            'total_revenue' : convert_numbers_to_thousands(total_revenue),
            'ebit' : convert_numbers_to_thousands(ebit),
            'taxes' : convert_numbers_to_thousands(taxes),
            'ebiat' : convert_numbers_to_thousands(ebiat),
            'depreciation_amortization' : convert_numbers_to_thousands(depreciation_amortization),
            'capex' : convert_numbers_to_thousands(capex),
            'change_working_capital' : convert_numbers_to_thousands(change_working_capital),
            'unlevered_cf' : convert_numbers_to_thousands(unlevered_cf), 
            'pv_unlevered_cf_total' : convert_numbers_to_thousands(present_value_unlevered_cf),

            'terminal_value' : convert_numbers_to_thousands(terminal_value),
            'pv_terminal_value' : convert_numbers_to_thousands(present_value_terminal_value),
            
            'enterprise_val' : convert_numbers_to_thousands(enterprise_value),
            
            'equity_value' : convert_numbers_to_thousands(equity_value),
            'share_price' : convert_numbers_to_thousands(share_price),

            'valuation_id' : valuation_id,
            'period' : i+1,
            'date_updated' : today.year,
            'symbol' : symbol,
            
            'growth_rate' : growth_rate,
            'ebit_rate' : ebit_rate,
            'tax_rate' : tax_rate,
            'depreciation_amorization_rate' : depreciation_amorization_rate,
            'capex_rate' : capex_rate,
            'change_nwc_rate' : nwc,
            'wacc' : wacc,
            'tgr' : tgr,

            'shares' : shares 

            }

            ny = {
            'total_revenue' : total_revenue,
            'ebit' : ebit,
            'taxes' : taxes,
            'depreciation_amortization' : depreciation_amortization,
            'capex': capex,
            'change_working_capital': change_working_capital,
            }
            
            per_period_financials.append(ny)
            per_period_predictions.append(period_prediction)


        return per_period_predictions



    @classmethod
    def calculate_and_save_valuation(cls, user_id, valuation_name, symbol, revenue_growth, ebit_rate, tax_rate, depr_amort_rate, capex_rate, nwc, wacc, tgr, shares):
        """Saves user valuation data for 5 future periods (called only for signed up users)"""

        # converts assumtpions to percentages
        user_id = user_id
        valuation_name = valuation_name
        growth_rate = float(revenue_growth/100)
        ebit_rate = float(ebit_rate/100)
        tax_rate = float(tax_rate/100)
        depreciation_amorization_rate = float(depr_amort_rate/100)
        capex_rate = float(capex_rate/100)
        nwc = float(nwc/100)
        wacc = float(wacc/100)
        tgr = float(tgr/100)
        shares = float(shares)
        
        valuation_id = random.randint(0, 4000)
    
        ############ Calculates predictions into future periods (total 5 periods)

        # all records from newest to oldest
        records= get_historical_financials_api(symbol)
        
        #holds all period financials
        per_period_predictions=[]
        per_period_financials = []

        ## first calculation based on latest financials from api
        lp = 0

        tr= float(records[lp].get('total_revenue'))
        ebt= float(records[lp].get('ebit'))
        txs= float(records[lp].get('taxes'))
        da = float(records[lp].get('depreciation_amortization'))
        cpx = float(records[lp].get('capex'))
        cwc = float((records[lp].get('change_working_capital')))
        csh = float(records[lp].get('cash_equivs_mkt_securities'))
        dbt = float(records[lp].get('long_term_debt'))
        period = records[lp].get('period')
        # gets latest year financials
        ly = {
            'total_revenue' : tr,
            'ebit' : ebt,
            'taxes' : txs,
            'depreciation_amortization' : da,
            'capex': cpx,
            'change_working_capital': cwc,
            'cash' : csh,
            'debt' : dbt
        }
        per_period_financials.append(ly)


        #predicted unlevered free cash flows
        total_predicted_cfs = 0
        predicted_unlevered_cfs = []
        
        for i in predicted_unlevered_cfs:
            total_predicted_cfs += predicted_unlevered_cfs['pv_unlevered_cf'][i]

        for i in range(6):
            #calculates next period financials
            p = i+1

            total_revenue = per_period_financials[i].get('total_revenue') * (1 + growth_rate)
            ebit = per_period_financials[i].get('ebit') * (1 + ebit_rate)
            taxes = per_period_financials[i].get('taxes') * (1 + tax_rate)
            ebiat = per_period_financials[i].get('ebit') - per_period_financials[i].get('taxes')
            depreciation_amortization = per_period_financials[i].get('depreciation_amortization') * (1 + depreciation_amorization_rate)
            capex = per_period_financials[i].get('capex') * (1 + capex_rate)
            change_working_capital = per_period_financials[i].get('change_working_capital') * (1 + nwc)
            
            unlevered_cf = per_period_financials[i].get('ebit') + per_period_financials[i].get('depreciation_amortization') - per_period_financials[i].get('capex') - per_period_financials[i].get('change_working_capital')
            present_value_unlevered_cf = unlevered_cf  / pow((1+wacc),(p))
            
            terminal_value = ( unlevered_cf * (1+tgr)) / ((wacc-tgr) + .00001)
            present_value_terminal_value = ( terminal_value / pow((1+wacc),(p)) )
            
            #uses both previous and current ucf's
            enterprise_value = (total_predicted_cfs + unlevered_cf) + present_value_terminal_value
            
            equity_value = enterprise_value + per_period_financials[0].get('cash') - per_period_financials[0].get('debt') 
            share_price = equity_value / shares
            
            cfs = {
                'pv_unlevered_cf' : present_value_unlevered_cf
            }

            predicted_unlevered_cfs.append(cfs)
            
            valuation = Valuation (
                total_revenue = convert_nums(total_revenue),
                ebit = convert_nums(ebit),
                taxes = convert_nums(taxes),
                ebiat = convert_nums(ebiat),
                depreciation_amortization = convert_nums(depreciation_amortization),
                capex = convert_nums(capex),
                change_working_capital = convert_nums(change_working_capital),
                
                unlevered_cf = convert_nums(unlevered_cf), 
                pv_unlevered_cf_total = convert_nums(present_value_unlevered_cf),
                
                terminal_value = convert_nums(terminal_value),
                pv_terminal_value = convert_nums(present_value_terminal_value),

                enterprise_val = convert_nums(enterprise_value),
                
                equity_value = convert_nums(equity_value), 
                share_price = share_price,
                
                user_id = user_id,
                valuation_name = valuation_name,
                valuation_id =valuation_id,
                period = period,
                date_updated = today.year,
                symbol = symbol,
                
                growth_rate = growth_rate,
                ebit_rate = ebit_rate,
                tax_rate = tax_rate,
                depreciation_amorization_rate= depreciation_amorization_rate,
                capex_rate = capex_rate,
                change_nwc_rate = nwc,
                wacc = wacc,
                tgr = tgr,

                shares = shares           
            
            )
            db.session.add(valuation)
            db.session.commit()

            ny = {
            'total_revenue' : total_revenue,
            'ebit' : ebit,
            'taxes' : taxes,
            'depreciation_amortization' : depreciation_amortization,
            'capex': capex,
            'change_working_capital': change_working_capital,
            }
            
            per_period_financials.append(ny)
            

        return valuation

    @classmethod
    def get_prev_growth_rates(cls, symbol):
        """Calculates historical rate growth (3 periods total)"""

        per_period_prev_growth = []
        
        # returns all records from newest to oldest
        records= list(get_historical_financials_api(symbol))

        #start with oldest financial record
        p = 0
        
        for i in range(len(records)-1):
            #Current year
            c_total_revenue = float(records[p].get('total_revenue'))
            c_ebit = float(records[p].get('ebit'))
            c_taxes = float(records[p].get('taxes'))
            c_depreciation_amortization = float(records[p].get('depreciation_amortization'))
            c_capex = float(records[p].get('capex'))
            c_change_working_capital = float((records[p].get('change_working_capital')))

            #Prev year
            p_total_revenue = float(records[p+1].get('total_revenue'))
            p_ebit = float(records[p+1].get('ebit'))
            p_taxes = float(records[p+1].get('taxes'))
            p_depreciation_amortization = float(records[p+1].get('depreciation_amortization'))
            p_capex = float(records[p+1].get('capex'))
            p_change_working_capital = float((records[p+1].get('change_working_capital')))

            period = records[p].get('period')
            rates_growth = {
                'period' : period,
                'lpr' : p_total_revenue,
                'cpr' : c_total_revenue,
                'rev_growth': '{:.2%}'.format(( c_total_revenue / p_total_revenue ) - 1),
                'ebit_growth': '{:.2%}'.format((c_ebit / p_ebit) - 1),
                'taxes_growth':'{:.2%}'.format( c_taxes / p_taxes),
                'depr_amort_growth': '{:.2%}'.format(c_depreciation_amortization / p_depreciation_amortization -1),
                'capex_growth': '{:.2%}'.format(c_capex / p_capex),
                'nwc_growth': '{:.2%}'.format(c_change_working_capital / p_change_working_capital - 1),
            }
            per_period_prev_growth.append(rates_growth)

            #move on to next period
            p += 1

        #place holder for skipped period (first period)
        first_period = {
            'period' : 'N/A',
            'lpr' : 'N/A',
            'cpr' : 'N/A',
            'rev_growth': 'N/A',
            'ebit_growth': 'N/A',
            'taxes_growth': 'N/A',
            'depr_amort_growth': 'N/A',
            'capex_growth': 'N/A',
            'nwc_growth': 'N/A'
        }
        per_period_prev_growth.append(first_period)

        return reversed(per_period_prev_growth)

    @classmethod
    def get_user_valuation_id(cls, valuation_name, user_id):
        """Find user valuation by valuation name`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a valuation whose name matches this valuation name
        and, if it finds such a valuation, returns that valuation object.

        If can't find matching valuation, return False.
        """
        user_valuations = cls.query.filter_by(valuation_name=valuation_name).all()
        
        for v in user_valuations:
            if v.valuation_name == valuation_name: 
                return v.valuation_id
        return False
        

    @classmethod
    def get_user_valuation(cls, id):
        """Find user valuation by valuation name`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a valuation whose name matches this valuation name
        and, if it finds such a valuation, returns that valuation object.

        If can't find matching valuation, return False.
        """

        valuation = cls.query.filter_by(valuation_id=id).all()

        if valuation:
            return valuation
        return False

####################  Favorite Stocks Model - Not Implemented yet ########################

class Favorites(db.Model):
    """Favorited Stocks"""

    __tablename__ = 'favorite_stocks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    stock_id = db.Column(db.Integer,  db.ForeignKey('stocks.id', ondelete='cascade'))



##################################################################### 
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
