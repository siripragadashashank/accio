import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
# Fetch the data
import yfinance as yf
from bs4 import BeautifulSoup as BS
import requests


def app():
    # Add a button for user interaction

    local_image_path = 'accio.png'  # Replace with the path to your local image
    st.image(local_image_path, use_column_width=True)
    st.write(
        "Welcome to the era of data-driven excellence! In a world where data reigns supreme, "
        "the ability to seamlessly manage and leverage information from various sources is paramount. "
        "This is where AccIO steps in, revolutionizing the way you handle data complexities. Say goodbye "
        "to isolated data compartments – AccIO transforms raw data into actionable insights, empowering "
        "you to make informed decisions and gain a competitive edge in your industry.")

    st.header('Why Choose AccIO:')
    st.write(
        "- **Simplicity in Complexity:** AccIO simplifies the complexities of data management, offering a user-friendly "
        "experience that caters to both novices and experts within an organization."
    )
    st.write(
        "- **Actionable Insights:** Transform raw data into actionable insights that fuel informed decision-making processes."
    )
    st.write(
        "- **Industry Leadership:** Stay ahead in your industry and save time with AccIO's AI analytics capabilities."
    )
    st.write(
        "- **Data as an Asset:** AccIO helps you view your data not just as information but as a valuable asset. "
        "Harness its potential and propel your organization forward."
    )

    st.write(
        "Embark on a journey where data becomes a catalyst for success. With AccIO, you have the tools to turn data challenges "
        "into opportunities. Join us in transforming your data into a strategic asset. Elevate your decision-making, boost efficiency, "
        "and thrive in the data-driven landscape with AccIO. 🚀📈")

    st.write(
        "In a rapidly evolving landscape flooded with information, the goal of the News Explorer is to offer you a carefully curated and personalized journey through news articles. This initiative centers on presenting news content that is not only relevant and credible but also diverse, meticulously tailored to each organization.")

    button_clicked_news = st.button("Explore today's news!")

    if button_clicked_news:
        st.write("Top relevant news!!")
        gif_runner = st.image("generate.gif")

        url = "https://thewaltdisneycompany.com/news/"

        webpage = requests.get(url)  # YOU CAN EVEN DIRECTLY PASTE THE URL IN THIS
        # HERE HTML PARSER IS ACTUALLY THE WHOLE HTML PAGE
        trav = BS(webpage.content, "html.parser")

        links = trav.find_all('a')

        links_dict = {}

        links_list = []
        href_list = []
        # Extract and print href attributes
        for link in links:

            # print(type(link.string), " ", link.string)
            if (str(type(link.string)) == "<class 'bs4.element.NavigableString'>" and len(link.string) > 50):
                href = link.get('href')
                # print(href)
                # print(str(M)+".", link.string)

                if str(link.string).upper() not in links_dict.keys():
                    # print(str(link.string))
                    # links_dict[link.string.upper()]=href
                    links_list.append(link.string.upper())
                    href_list.append(href)

        links_dict["Headlines"] = links_list
        links_dict["Links"] = href_list

        # print(links_dict)

        news_df = pd.DataFrame.from_dict(links_dict)

        # To make the Links column clickable
        st.data_editor(
            news_df,
            column_config={
                "Links": st.column_config.LinkColumn("News Links")
            },
            hide_index=True,
        )

        ####Stock news

        # st.dataframe(news_df)
        gif_runner.empty()

    st.write(
        "Are you a numbers fanatic? Stay informed with up-to-the-minute financial news. Our app integrates the latest news related to your selected stocks, ensuring you are well-aware of factors that may impact their performance.")

    button_clicked_stock = st.button("Show me the money!!!")

    button_clicked_competitors = st.button("Compare with competitors!!")

    # Respond to button click
    if button_clicked_stock:
        tickers_list = ['DIS']
        data = yf.download(tickers_list, '2021-1-1')['Adj Close']
        ((data.pct_change() + 1).cumprod()).plot(figsize=(10, 7))

        # Show the legend
        plt.legend()

        # Define the label for the title of the figure
        plt.title("Returns", fontsize=16)

        # Define the labels for x-axis and y-axis
        plt.ylabel('Cumulative Returns', fontsize=14)
        plt.xlabel('Year', fontsize=14)

        # Plot the grid lines
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)

        st.pyplot(plt.gcf())

    if button_clicked_competitors:
        st.title('Stock Returns Analysis 📈')
        tickers_list = ['FOXA', 'SIX', 'CMCSA', 'DIS']
        data = yf.download(tickers_list, '2021-1-1')['Adj Close']
        ((data.pct_change() + 1).cumprod()).plot(figsize=(10, 7))

        # Show the legend
        plt.legend()

        # Define the label for the title of the figure
        plt.title("Returns", fontsize=16)

        # Define the labels for x-axis and y-axis
        plt.ylabel('Cumulative Returns', fontsize=14)
        plt.xlabel('Year', fontsize=14)

        # Plot the grid lines
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)

        st.pyplot(plt.gcf())
