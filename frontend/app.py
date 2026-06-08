import streamlit as st
import requests

st.title("🛒 AI Shopping Assistant")

query = st.text_input(
    "What product are you looking for?"
)

if st.button("Search"):

    response = requests.post(
        "http://127.0.0.1:8000/recommend",
        json={"query": query}
    )

    data = response.json()

    best = data["best_product"]

    st.success("Best Product")

    st.subheader("🏆 Best Product")

    st.write(f"Name: {best['name']}")
    st.write(f"Price: ₹{best['price']}")

    st.write("### Pros")
    for p in best["pros"]:
        st.success(p)

    st.write("### Cons")
    for c in best["cons"]:
        st.error(c)

    st.subheader("📦 All Products")

    for product in data["all_products"]:

        st.write("--------------------")

        st.write(f"Name: {product['name']}")
        st.write(f"Price: ₹{product['price']}")

        st.write("Pros:")
        for p in product["pros"]:
            st.write("✅", p)

        st.write("Cons:")
        for c in product["cons"]:
            st.write("❌", c)