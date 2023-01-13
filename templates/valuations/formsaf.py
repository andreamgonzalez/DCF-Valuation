  <div class="col">
    <h4>Trend Analysis: {{stock.symbol}}</h4>
    <p>The percentage changes between prior years for Revenue, EBIT, Taxes, and EBIAT have already been recorded. You can use these to support your assumptions about where the company may be headed in the future.</p>

    <table class="table table-striped table-hover table-dark text-nowrap">
      <thead>
        <tr>
          <th scope="col">STOCK SYMBOL : {{stock.symbol}}</th>
          {% for p in prev_financials %}
          <th style="text-align:right">{{ p["period"]}}</th>
          {% endfor%}
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Revenue</th>
          {% for p in prev_financials %}
          <td>${{ p["total_revenue"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">change %</th>
          {% for p in prev_growth_rates %}
            <td>
              <span class="text-danger">
                <i class="fas fa-caret-down me-1"></i><span>{{p["rev_growth"]}}</span>
              </span>
            </td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">EBIT</th>
          {% for p in prev_financials %}
          <td>${{ p["ebit"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">change %</th>
          {% for p in prev_growth_rates %}
            <td>
              <span class="text-danger">
                <i class="fas fa-caret-down me-1"></i><span>{{p["ebit_growth"]}}</span>
              </span>
            </td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Taxes</th>
          {% for p in prev_financials %}
          <td>${{ p["taxes"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">change %</th>
          {% for p in prev_growth_rates %}
          <td>
            <span class="text-danger">
              <i class="fas fa-caret-down me-1"></i><span>{{p["taxes_growth"]}}</span>
            </span>
          </td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">EBIAT</th>
          {% for p in prev_financials %}
          <td>${{ p["EBIAT"]}}</td>
          {% endfor%}
        </tr>
      
        <tr>
          <th scope="row">change %</th>
          {% for p in prev_financials %}
          <td>
            <span class="text-danger">
              <i class="fas fa-caret-down me-1"></i><span>$-1.78</span>
            </span>
          </td>
          {% endfor%}
        </tr>
      </tbody>
    </table>
  </div>
</div><br><br>

<h6 style="color:#6199f9">Previous Financials (in billions)</h6>
<div class="table-responsive-sm">

    <table class="table table-sm  table-striped table-hover table-dark">
      <thead>
        <tr>
          <th scope="col">STOCK SYMBOL : {{stock.symbol}}</th>
          {% for p in prev_financials %}
          <th scope="col" style="text-align: right">{{p["period"]}}</th>
          {% endfor%}
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="col" class="title">Income Statement :</th>
          {% for p in prev_financials %}
          <td></td>
          {% endfor%}

        </tr>
<!---------------------------------- Income Stmt ------------------------------------>
        <tr>
          <th scope="row">Revenue</th>
          {% for p in prev_financials %}
          <td>${{ p["total_revenue"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Cost of Revenue</th>
          {% for p in prev_financials %}
          <td>${{ p["cost_of_revenue"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Gross Income</th>
          {% for p in prev_financials %}
          <td>${{ p["gross_income"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Interest Expense</th>
          {% for p in prev_financials %}
          <td>${{ p["interest_exp"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Operating Expenses</th>
          {% for p in prev_financials %}
          <td>${{ p["operating_expenses"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Operating Income</th>
          {% for p in prev_financials %}
          <td>${{ p["operating_income"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">EBIT</th>
          {% for p in prev_financials %}
          <td>${{ p["ebit"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Taxes</th>
          {% for p in prev_financials %}
          <td>${{ p["taxes"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">Net Income</th>
          {% for p in prev_financials %}
          <td>${{ p["net_income"]}}</td>
          {% endfor%}
        </tr>

        <tr>
          <th scope="row">EBIAT</th>
          {% for p in prev_financials %}
          <td>${{ p["total_revenue"]}}</td>
          {% endfor%}
        </tr>
      </tbody>
    </table>
<!---------------------------------- CashFlows ------------------------------------>
    <table class="table table-sm table-striped table-hover table-dark">
        <thead>
          <tr><th scope="col" class="title">Cash Flow Statement :</th>
            {% for p in prev_financials %}
            <th scope="col" style="text-align: right">{{p["period"]}}</th>
            {% endfor%}
          </tr>
        </thead>
        <tbody>
        <tr>
          <th scope="row">Operating Cash Flow</th>
          {% for p in prev_financials %}
          <td>${{ p["operating_cashflow"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">Deferred Tax</th>
          {% for p in prev_financials %}
          <td>${{ p["deferred_tax"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">&Delta; Inventory</th>
          {% for p in prev_financials %}
          <td>${{ p["change_inventory"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">&Delta; Acct. Payables</th>
          {% for p in prev_financials %}
          <td>${{ p["change_ap"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">&Delta; Acct. Receivables</th>
          {% for p in prev_financials %}
          <td>${{ p["change_ar"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">Depreciation & Amort.</th>
          {% for p in prev_financials %}
          <td>${{ p["depreciation_amortization"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">Investment Cashflows</th>
          {% for p in prev_financials %}
          <td>${{ p["investment_cashflows"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">CAPEX</th>
          {% for p in prev_financials %}
          <td>${{ p["capex"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="row">&Delta; Working Capital</th>
          {% for p in prev_financials %}
          <td>${{ p["change_working_capital"]}}</td>
          {% endfor%}
        </tr>
      </tbody>
    </table>
<!---------------------------------- Balance Sheet ------------------------------------>
    <table class="table table-sm table-striped table-hover table-dark">
      <thead>
        <tr><th scope="row" class="title">Balance Sheet :</th>
          {% for p in prev_financials %}
          <th scope="col" style="text-align: right">{{p["period"]}}</th>
        {% endfor%}
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="col col-1">Cash and Cash Equiv.</th>
          {% for p in prev_financials %}
          <td>${{ p["cash_equivs_mkt_securities"]}}</td>
          {% endfor%}
        </tr>
        <tr>
          <th scope="col">Debt</th>
          {% for p in prev_financials %}
          <td>${{ p["long_term_debt"]}}</td>
          {% endfor%}
        </tr>
      </tbody>
    </table>

  <h5>About {{stock.symbol}}: </h5>
  <div><p>{{stock.summary}}</p></div>
</div>
{% endblock %}