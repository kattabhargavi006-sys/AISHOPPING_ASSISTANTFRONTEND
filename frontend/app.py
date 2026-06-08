import streamlit as st
import requests
import json
server_loc=st.secrets["server_url"].rstrip("/")
st.title(" AI Shopping Assistant 🛒")
tab1, tab2, tab3 = st.tabs(["📦 Product API", "🌍 Web Search", "⭐ Review Analyzer"])
with tab1:
    st.header("Product Search")
    product_query = st.text_input("Enter Product Query", key="product_input")

    if st.button("Fetch Products"):
        if not product_query.strip():
            st.warning("Please enter a product query.")
        else:
            with st.spinner("Fetching products..."):
                try:
                    response = requests.post(
                        f"{server_loc}/get_product",
                        params={"product_query": product_query}
                    )
                    data = response.json()

                    if data.get("error"):
                        st.error(f"Error: {data['error']}")

                    elif data.get("products"):
                        for p in data["products"]:
                            with st.container():
                                st.markdown(f"### 🛍️ {p.get('name', 'N/A')}")
                                col1, col2 = st.columns(2)
                                col1.metric("Price", p.get("price", "N/A"))
                                col2.metric("Rating", p.get("rating", "N/A"))
                                st.divider()

                    elif data.get("answer"):
                        st.markdown(data["answer"])

                    else:
                        st.info("No products found.")

                except Exception as e:
                    st.error(f"Request failed: {e}")
with tab2:
    st.header("Price Comparison Between Platforms")
    product = st.text_input("Enter Product", key="price_input")

    if st.button("Compare Prices"):
        if not product.strip():
            st.warning("Please enter a product name.")
        else:
            with st.spinner("Comparing prices..."):
                try:
                    response = requests.post(
                        f"{server_loc}/get_price_compare",
                        params={"product": product}
                    )
                    data = response.json()

                    if data.get("error"):
                        st.error(f"Error: {data['error']}")

                    elif data.get("platforms"):
                        # Structured JSON response → show as cards
                        st.subheader(f"Prices for: {product}")
                        for p in data["platforms"]:
                            col1, col2, col3 = st.columns(3)
                            col1.markdown(f"**{p.get('site', 'N/A')}**")
                            col2.markdown(p.get("price", "N/A"))
                            col3.markdown(f"🏷️ {p.get('discount', 'No discount')}")
                            st.divider()

                    elif data.get("answer"):
                        # Text/table response → render as markdown
                        st.subheader(f"Prices for: {product}")
                        st.markdown(data["answer"])

                    else:
                        st.info("No price data found.")

                except Exception as e:
                    st.error(f"Request failed: {e}")
with tab3:
    st.header("Review Analyzer")
    product_name = st.text_input("Enter Product Name", key="review_product",
                                  placeholder="e.g. iPhone 15, Samsung S24...")

    if st.button("Analyze Reviews"):
        if not product_name.strip():
            st.warning("Please enter a product name.")
        else:
            with st.spinner(f"Fetching and analyzing reviews for {product_name}..."):
                try:
                    response = requests.post(
                        f"{server_loc}/analyze_reviews",
                        params={"product_name": product_name}
                    )
                    data = response.json()

                    if data.get("error"):
                        st.error(f"Error: {data['error']}")
                    else:
                        pros = data.get("pros", [])
                        cons = data.get("cons", [])
                        summary = data.get("summary", "")

                        if pros:
                            st.markdown("### ✅ Pros")
                            for pro in pros:
                                st.markdown(f"- {pro}")

                        if cons:
                            st.markdown("### ❌ Cons")
                            for con in cons:
                                st.markdown(f"- {con}")

                        if summary:
                            st.divider()
                            st.markdown("### 📝 Summary")
                            st.info(summary)

                        # fallback if JSON failed and raw text came back
                        if not pros and not cons and data.get("answer"):
                            st.markdown(data["answer"])

                except Exception as e:
                    st.error(f"Request failed: {e}")