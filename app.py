import os

from flask import Flask, redirect, render_template, request, flash, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import *
from models import db, connect_db, User, Financial, Stock, Valuation, Favorites


CURR_USER_KEY = "curr_user"

app = Flask(__name__)


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///valuation'))


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:

        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)
        do_login(user)
        return redirect("/")
    else:
        return render_template("signup.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/dashboard/{user.id}")
        flash("Invalid credentials.", 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Logged out successfully.", "success")
    return redirect('/login')


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/")


##############################################################################
# Template routes:

@app.route('/')
def homepage():
    """Show public homepage"""
    return render_template('public.html')


@app.route('/dashboard/<user_id>', methods=["GET", "POST"])
def show_dashboard(user_id):
    """Show the users dashboard"""

    if not g.user:
        return redirect('/')
    else:
        user = User.query.get_or_404(user_id)
        return render_template("/users/dashboard.html", user=user)

@app.route("/stocks", methods=["GET", "POST"])
def show_search_page():
    """Show the stock search page"""
    return render_template('valuations/stocksSearch.html')


@app.route('/search', methods=["POST"])
def searches_stock():
    """Search for a typed stock"""

    ticker = request.form["search"]

    if len(ticker) > 0:
        return redirect(f'/stock/{ticker}')
    
    flash("Please enter a search term", 'warning')
    return redirect('/')


@app.route('/stock/<ticker>', methods=["GET", "POST"])
def show_stock_detail(ticker):
    """Show the stock detail page with historical data"""
    stock = Stock.get_stock_data(ticker)
    prev_financials = Financial.get_all_historical_financials(ticker)
    prev_growth_rates = list(Valuation.get_prev_growth_rates(ticker))


    return render_template("/valuations/stockDetail.html", stock=stock, prev_financials=prev_financials, prev_growth_rates=prev_growth_rates)


@app.route('/valuation/<ticker>', methods=["GET", "POST"])
def valuation_assumptions_form(ticker):
    """Start a valuation by presenting form and the historical data for the stock"""
    stock = Stock.get_stock_data(ticker)
    prev_financials = Financial.get_all_historical_financials(ticker)
    prev_growth_rates = list(Valuation.get_prev_growth_rates(ticker))
    
    if not g.user:
        form = PublicValuationForm(symbol=ticker)
        if request.method == 'POST':
            if form.validate_on_submit():
                        valuation = Valuation.calculate_user_valuation(
                        symbol = ticker,
                        revenue_growth = form.revenue_growth.data,
                        ebit_rate = form.ebit_rate.data,
                        tax_rate = form.tax_rate.data,
                        depr_amort_rate = form.depr_amort_rate.data,
                        capex_rate = form.capex_rate.data,
                        nwc = form.nwc.data,
                        wacc = form.wacc.data,
                        tgr = form.terminal_growth.data,
                        shares = form.shares.data,
                    )

                        return render_template('/valuations/valuationDetail.html', valuation=valuation, stock=stock)

        return render_template("/valuations/publicValuationForm.html", stock=stock, form=form, prev_financials=prev_financials, prev_growth_rates=prev_growth_rates)
    
    form = UserValuationForm(symbol=ticker)
    if request.method == 'POST':
        valuation = Valuation.calculate_and_save_valuation(
                valuation_name = form.valuation_name.data,
                user_id = g.user.id,
                symbol = ticker,
                revenue_growth = form.revenue_growth.data,
                ebit_rate = form.ebit_rate.data,
                tax_rate = form.tax_rate.data,
                depr_amort_rate = form.depr_amort_rate.data,
                capex_rate = form.capex_rate.data,
                nwc = form.nwc.data,
                wacc = form.wacc.data,
                tgr = form.terminal_growth.data,
                shares = form.shares.data,
            )
        db.session.add(valuation)
        db.session.commit()

        #get valuation id from db by name
        valuation_id = Valuation.get_user_valuation_id(form.valuation_name.data, g.user.id)

        return redirect(f'/valuation/{g.user.id}/{ticker}/{valuation_id}')

    return render_template("/valuations/valuationForm.html", stock=stock, form=form, prev_financials=prev_financials, prev_growth_rates=prev_growth_rates)


@app.route('/valuation/<user_id>/<stock>/<valuation_id>')
def show_user_valuation(user_id, valuation_id, stock):
    """Show valuation results"""
    stock = Stock.get_stock_data(stock)
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    valuation = Valuation.get_user_valuation(valuation_id)
        
    return render_template("/valuations/valuationDetail.html", valuation=valuation, stock=stock)


########################The below are not implemented yet###########################
# @app.route('/valuation/delete/<int:valuation_id>/<int:user_id>', methods=["POST"])
# def delete_user_valuation(valuation_id):
#     """Delete a valuation"""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     valuation = Valuation.query.get_or_404(valuation_id)
#     if valuation.user_id != g.user.id:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")
    
#     valuation = db.session.query(valuation).where(valuation.valuation_id == valuation_id)

#     db.session.delete(valuation) ##deletes all the periods valuated for valuation of this id
#     db.session.commit()

#     return redirect(f"/dashboard/{g.user.id}")


# @app.route('/stock/favorite/<stock>/<int:user_id>', methods=['POST'])
# def add_favorite_stock(stock):
#     """Favorite a stock for currently-logged-in user."""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     favorited_stock = Favorites.query.get_or_404(stock)
#     if favorited_stock.user_id == g.user.id:
#         return abort(403)

#     user_favorites = g.user.favorites

#     if favorited_stock in user_favorites:
#         g.user.favorites = [fav for fav in user_favorites if fav != favorited_stock]
#     else:
#         g.user.favorites.append(favorited_stock)

#     db.session.commit()

#     return redirect(f"/dashboard/{g.user.id}")






















##############################################################################
# API request/response routes:

@app.route('/valuation/<ticker>/info')
def info(ticker):
    """Show the create valuation page"""
    stock_data = Stock.get_stock_info(ticker)
    return stock_data


@app.route('/valuation/<ticker>/cashflow')
def cashflow(ticker):
    """Show the create valuation page"""
    # stock_cf = Stock.get_stock_cashflow(ticker)
    stock_cf = Stock.get_stock_cashflow(ticker)
    
    return stock_cf


@app.route('/valuation/<ticker>/bs')
def balance_sheet(ticker):
    """Show the create valuation page"""
    stock_bs = Stock.get_stock_balance_sheet(ticker)
    return stock_bs


@app.route('/valuation/<ticker>/is')
def income_stmt(ticker):
    """Show the create valuation page"""
    stock_income_stmt = Stock.get_stock_income_stmt(ticker)
    return stock_income_stmt


@app.route('/valuation/<ticker>/shares')
def shares(ticker):
    """Show the create valuation page"""
    stock_shares = Stock.get_stock_shares(ticker)
    return stock_shares
