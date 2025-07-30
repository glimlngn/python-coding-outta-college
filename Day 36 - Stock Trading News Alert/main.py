import requests
from api_keys import stock_price_api_key, stock_news_api_key
from twilio.rest import Client

STOCK_NAME = "VRT"
COMPANY_NAME = "Vertiv"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_price_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": stock_price_api_key,
}

stock_price_response = requests.get(url=STOCK_ENDPOINT, params=stock_price_params).json()

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

response_days = stock_price_response["Time Series (Daily)"]
closing_prices = [(key, response_days[key]["4. close"]) for (key, value) in response_days.items()]
closing_price_yest = closing_prices[0][1]  # Get the closing price for yesterday
print("Closing Price Yesterday: " + closing_price_yest)

# 2. - Get the day before yesterday's closing stock price

closing_price_day_before_yest = closing_prices[1][1]  # Get the closing price for yesterday
print("Closing Price Day Before Yesterday: " + closing_price_day_before_yest)

# 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = round(float(closing_price_yest) - float(closing_price_day_before_yest), 2)
print("Price Difference: " + str(difference))

# 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage_difference = round((difference / float(closing_price_yest)) * 100, 2)
print("Percentage Difference: " + str(percentage_difference) + " %")

# 5. - If TODO4 percentage is greater than 5 then print("Get News").

# if abs(percentage_difference) > 5:
#     print("Get News")

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

# if abs(percentage_difference) > 5:
stock_news_params = {
    "q": COMPANY_NAME,
    "apiKey": stock_news_api_key,
    "sortBy": "publishedAt",
    "pageSize": 3,
}
stock_news_response = requests.get(url=NEWS_ENDPOINT, params=stock_news_params).json()

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
# N/A, already done in the previous step.

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

news_list = [{"title": news["title"], "description": news["description"]} for news in stock_news_response["articles"]]

#TODO 9. - Send each article as a separate message via Twilio. 

from api_keys import account_sid, auth_token, number_to, number_from

client = Client(account_sid, auth_token)

arrow = "🔺" if percentage_difference > 0 else "🔻"

for news in news_list:

    message_body =  f"*{COMPANY_NAME}* \n\n" \
                    f"*{STOCK_NAME}*: {arrow} {abs(percentage_difference)} % \n\n" \
                    f"*Headline*: {news['title']}\n\n" \
                    f"*Brief*: {news['description']}"

    message = client.messages.create(
        from_='whatsapp:' + number_from,
        body = message_body,
        to='whatsapp:' + number_to
    )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

