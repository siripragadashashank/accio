import streamlit as st
from dotenv import load_dotenv
import plotly.express as px
from .utils import *


def main():
    load_dotenv()

    st.title("Extract your invoices and analyze.💁 ")
    st.subheader("Drowning in paper receipts and invoice PDFs?  "
                 "Untangle the financial knots with our AI-powered invoice extractor. "
                 "Analyze spending and reclaim control of your finances.")

    pdf = st.file_uploader("Upload invoices here, only PDF files allowed", type=["pdf"], accept_multiple_files=True)

    submit = st.button("Extract Data")

    if submit:
        with st.spinner('Analyzing...'):
            df = create_docs(pdf)
            st.write(df.head())

            data_as_csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download data as CSV",
                data_as_csv,
                "benchmark-tools.csv",
                "text/csv",
                key="download-tools-csv",
            )
            df["Total"] = [float(str(i).replace(",", "")) for i in df["Total"]]
            total_amount = int(df["Total"].astype(float).sum())
            total_products = int(df["Quantity"].astype(float).sum())

            left_column, middle_column = st.columns(2)
            with left_column:
                st.subheader("Total Sales:")
                st.subheader(f"US $ {total_amount:,}")

            with middle_column:
                st.subheader("Total Products:")
                st.subheader(f"{total_products:,}")

            st.markdown("---")
            # product bar graph
            fig_products = px.bar(
                df,
                x="Description", y="Quantity",

                title="<b> Product by sale quantity</b>",
                color_discrete_sequence=["#0083B8"],
                template="plotly_white",
            )
            fig_products.update_layout(
                xaxis=dict(tickmode="linear"),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False))
            )
            # product sale amount
            st.plotly_chart(fig_products)
            fig_sales = px.bar(
                df,
                x="Description",
                y="Total",
                title="<b>Over all sales</b>",
                color_discrete_sequence=["#0083B8"],
                template="plotly_white",
            )

            fig_sales.update_layout(
                xaxis=dict(tickmode="linear"),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
            )
            st.plotly_chart(fig_sales)
        # left_column, right_column = st.columns(2)
        # left_column.plotly_chart(fig_sales, use_container_width=True)
        # right_column.plotly_chart(fig_products, use_container_width=True)

        # st.bar_chart(df,x="Description",y="Quantity")
        # st.success("Hope I was able to save your time❤️")


# Invoking main function
if __name__ == '__main__':
    main()
