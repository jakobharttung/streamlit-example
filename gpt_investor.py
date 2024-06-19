import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import anthropic
import openai

# Set up Anthropic API client
client = anthropic.Anthropic(api_key="")

# Function to call Anthropic API for industry and competitor information
def get_company_info(ticker):
    prompt = f"Investor analysis for {ticker}. Provide industry and 5 competitors."
    response = client.completions.create(prompt=prompt, max_tokens=150)
    return response['choices'][0]['text']

# Function to get sentiment analysis
def get_sentiment_analysis(news):
    prompt = f"Perform sentiment analysis on the following news: {news}"
    response = client.completions.create(prompt=prompt, max_tokens=150)
    return response['choices'][0]['text']

# Function to get analyst rating and industry analysis
def get_analyst_industry_analysis(ticker):
    prompt = f"Provide analyst rating and industry analysis for {ticker}."
    response = client.completions.create(prompt=prompt, max_tokens=150)
    return response['choices'][0]['text']

# Function to get news sentiment analysis and generate a recommendation
def generate_recommendation(stock_data, sentiment, analyst_industry):
    # Analyze stock data
    close_prices = stock_data['Close']
    avg_close = close_prices.mean()
    
    recommendation = f"Based on the data, sentiment analysis and industry analysis: \nAverage closing price: {avg_close}\nSentiment: {sentiment}\nAnalyst and Industry Analysis: {analyst_industry}"
    return recommendation

# Streamlit UI
st.title("Investor Analysis Tool")

ticker = st.text_input("Enter stock market ticker:")

if ticker:
    # Call Anthropic API to get industry and competitors
    company_info = get_company_info(ticker)
    industry, competitors = company_info.split("\n")[0], company_info.split("\n")[1:6]

    # Display industry and competitors
    st.write(f"Industry: {industry}")
    st.write(f"Competitors: {', '.join(competitors)}")

    # Get historical data for all tickers
    tickers = [ticker] + competitors
    data = yf.download(tickers, start=datetime.now() - timedelta(days=3*365), end=datetime.now())

    # Plot closing prices
    st.subheader("Closing Prices")
    for t in tickers:
        plt.plot(data['Close'][t], label=t)
    plt.legend()
    st.pyplot()

    # Add date range selector
    st.date_input("Select Date Range", [datetime.now() - timedelta(days=365), datetime.now()])

    # Dropdown to select ticker for candlestick chart
    selected_ticker = st.selectbox("Select ticker for candlestick chart", tickers)
    
    # Plot candlestick chart for selected ticker
    if selected_ticker:
        import plotly.graph_objs as go
        from plotly.subplots import make_subplots

        stock = yf.Ticker(selected_ticker)
        hist = stock.history(period="1y")
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        st.plotly_chart(fig)

    # Get news data and perform sentiment analysis
    stock = yf.Ticker(ticker)
    news = stock.news()
    news_titles = [item['title'] for item in news]
    sentiment = get_sentiment_analysis(news_titles)

    # Get analyst rating and industry analysis
    analyst_industry = get_analyst_industry_analysis(ticker)

    # Generate recommendation
    recommendation = generate_recommendation(data['Close'][ticker], sentiment, analyst_industry)
    st.write(recommendation)

