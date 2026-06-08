import streamlit as st
import requests

# Backend URL
server_loc = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 AI Shopping Assistant")

tab1, tab2, tab3 = st.tabs(
    ["📦 Product API", "🌍 Web Search", "⭐ Review Analyzer"]
)

# -------------------------------
# PRODUCT API TAB
# -------------------------------

with tab1:

    st.header("📦 Product Search")

    query = st.text_input(
        "Enter Product Query",
        key="product_search"
    )

    if st.button("Fetch Products"):

        with st.spinner("Fetching products..."):

            response = requests.post(
                f"{server_loc}/get_product",
                params={"product_query": query}
            )

            data = response.json()

            if data.get("products"):

                for product in data["products"]:

                    st.subheader(product.get("name", "Unknown"))

                    st.write(
                        f"💰 Price: {product.get('price', 'N/A')}"
                    )

                    st.write(
                        f"⭐ Rating: {product.get('rating', 'N/A')}"
                    )

                    st.markdown("---")

            else:
                st.warning("No products found")

# -------------------------------
# WEB SEARCH TAB
# -------------------------------

with tab2:

    st.header("🌍 Price Comparison Between Platforms")

    product = st.text_input(
        "Enter Product",
        key="price_compare"
    )

    if st.button("Compare Prices"):

        with st.spinner("Comparing prices..."):

            response = requests.post(
                f"{server_loc}/get_price_compare",
                params={"product": product}
            )

            data = response.json()

            if data.get("platforms"):

                for item in data["platforms"]:

                    st.subheader(
                        item.get("site", "Unknown Site")
                    )

                    st.write(
                        f"💰 Price: {item.get('price', 'N/A')}"
                    )

                    st.write(
                        f"🏷️ Discount: {item.get('discount', 'N/A')}"
                    )

                    st.markdown("---")

            else:

                st.info(
                    data.get(
                        "answer",
                        "No comparison data found"
                    )
                )

# -------------------------------
# REVIEW ANALYZER TAB
# -------------------------------

with tab3:

    st.header("⭐ Review Analyzer")

    product_name = st.text_input(
        "Enter Product Name",
        key="review_product"
    )

    if st.button("Analyze Reviews"):

        with st.spinner("Analyzing reviews..."):

            response = requests.post(
                f"{server_loc}/analyze_reviews",
                params={
                    "product_name": product_name
                }
            )

            data = response.json()

            st.subheader("📝 Summary")

            st.info(
                data.get(
                    "summary",
                    "No summary available"
                )
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("✅ Pros")

                for pro in data.get("pros", []):

                    st.success(pro)

            with col2:

                st.subheader("❌ Cons")

                for con in data.get("cons", []):

                    st.error(con)