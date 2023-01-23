# DCF-Valuation
## Use this application to perform what is called a Discounted Cash Flow valuation. What is that you ask?

A discounted cash flow (DCF) valuation is a method used to estimate the value of an investment or asset by projecting its future cash flows and then discounting them back to present value. Here is a step-by-step process for creating a DCF valuation:
<ol>
<li>Identify the cash flows that the investment or asset is expected to generate. These can be projected using financial statements, industry data, and other sources. </li>

<li>Determine the discount rate to use. This is the required rate of return that investors expect for taking on the risk of the investment.</li>

<li>Estimate the terminal value of the investment or asset. This is the value of the investment or asset at the end of the projection period, which can be calculated using a terminal growth rate and a terminal multiple.</li>

<li>Discount the projected cash flows and terminal value back to present value using the discount rate. This can be done using a present value formula or a financial calculator.</li>

<li>Add up the discounted cash flows and terminal value to get the DCF valuation for the investment or asset.</li>
</ol>
It's important to note that a DCF valuation is only as accurate as the assumptions used in the projection. Therefore, it's important to be as realistic and conservative as possible when estimating future cash flows and the discount rate.

## API Selection
This project uses the <a href="https://github.com/ranaroussi/yfinance">yfinance API</a> as it is a reliable and accurate source for getting stock prices and historical financials.

## Database Schema Design

![alt text](https://github.com/andreamgonzalez/DCF-Valuation/blob/main/DCF%20Database%20Schema.png)

To start off, the database for this application will be fairly simple. To facilitate the features desired in this application we will mainly need the four database tables listed below:
<ul>
  <li><b>users</b>: necessary for storing login and user information.<br></li>
  <li><b>user_valuations</b>: necessary in order to store all user inputs for saved valuations.<br></li>
  <li><b>stocks</b>: this table stores the relationship between saved valuations and their creator (user).<br></li>
  <li><b>favorited_stocks</b>: this table stores the relationship between all of the favorited stocks and their favoriting user.<br></li>
</br>
</ul>
**Please note that the above tables and schema are subject to future changes, as needed.
