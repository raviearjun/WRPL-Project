import streamlit as st
from customer import customer_view
from seller import seller_view

st.sidebar.title("🔀 Pilih Tampilan")
view = st.sidebar.radio("Masuk sebagai:", ["Customer", "Penjual"])

if view == "Customer":
    customer_view()
else:
    seller_view()
