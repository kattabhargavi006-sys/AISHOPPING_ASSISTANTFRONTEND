import streamlit as st
import requests

# Backend URL
server_loc = "http://127.0.0.1:8000"

st.title("🛒 AI Shopping Assistant")

query = st.text_input(
    "What product are you looking for?"
)

if st.button("Search"):

    with st.spinner("Fetching products..."):

        response = requests.post(
            f"{server_loc}/recommend",
            json={"query": query}
        )

        data = response.json()

        best = data["best_product"]

        st.markdown("---")

        st.header("🏆 Best Recommendation")

        st.success(best["name"])

        st.metric(
            label="Price",
            value=f"₹{best['price']}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Pros")
            for p in best["pros"]:
                st.success(p)

        with col2:
            st.subheader("❌ Cons")
            for c in best["cons"]:
                st.error(c)

        st.markdown("---")

        st.header("📦 Product Comparison")

        for product in data["all_products"]:

            st.subheader(product["name"])

            st.write(
                f"💰 Price: ₹{product['price']}"
            )

            c1, c2 = st.columns(2)

            with c1:
                st.write("Pros")
                for p in product["pros"]:
                    st.write("✅", p)

            with c2:
                st.write("Cons")
                for c in product["cons"]:
                    st.write("❌", c)

            st.markdown("---")