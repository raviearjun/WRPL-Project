import streamlit as st
import pandas as pd
from database import get_connection

def seller_view():
    st.title("👨‍🍳 Dashboard Penjual")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Tambah Menu
    st.subheader("➕ Tambah Menu")
    name = st.text_input("Nama Menu")
    price = st.number_input("Harga", min_value=0.0, format="%.2f")
    available = st.checkbox("Tersedia", value=True)

    if st.button("Tambahkan"):
        if name and price:
            cursor.execute("INSERT INTO menu (name, price, available) VALUES (%s, %s, %s)", (name, price, available))
            conn.commit()
            st.success("Menu berhasil ditambahkan!")
        else:
            st.warning("Harap isi semua field!")

    # Hapus Menu
    st.subheader("❌ Hapus Menu")
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()
    menu_df = pd.DataFrame(menu_items)

    if not menu_df.empty:
        delete_id = st.selectbox("Pilih menu yang akan dihapus", menu_df["id"].tolist())
        if st.button("Hapus"):
            cursor.execute("DELETE FROM menu WHERE id=%s", (delete_id,))
            conn.commit()
            st.success("Menu berhasil dihapus!")

    # Lihat Pendapatan
    st.subheader("💰 Total Pendapatan")
    cursor.execute("SELECT SUM(o.quantity * m.price) AS revenue FROM order_details o JOIN menu m ON o.menu_id = m.id")
    revenue = cursor.fetchone()["revenue"] or 0
    st.metric("Total Pendapatan", f"Rp {revenue:.2f}")

    cursor.close()
    conn.close()
