import streamlit as st
import pandas as pd
from database import get_connection

def seller_view():
    st.title("👨‍🍳 Dashboard Penjual")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Tampilkan antrean pesanan dari customer
    st.subheader("📋 Antrean Pesanan")
    queue_df = pd.read_sql("SELECT * FROM order_details WHERE queue_status='waiting' ORDER BY orderNumber ASC", conn)
    if not queue_df.empty:
        st.dataframe(queue_df)
    else:
        st.info("Tidak ada pesanan yang sedang menunggu.")

    # Konfirmasi pesanan yang sudah selesai
    st.subheader("✅ Konfirmasi Pesanan")
    confirmed_order_id = st.number_input("Masukkan Nomor Pesanan", min_value=1)
    if st.button("Konfirmasi"):
        cursor.callproc("UpdateQueueStatus", (confirmed_order_id,))
        conn.commit()
        st.success("✅ Pesanan berhasil dikonfirmasi!")

    # Tambah Menu
    st.subheader("➕ Tambah Menu")
    product_code = st.text_input("Kode Produk")
    name = st.text_input("Nama Menu")
    price = st.number_input("Harga", min_value=0, format="%d")
    category = st.selectbox("Kategori", ["food", "drink", "snack"])
    available = st.selectbox("Ketersediaan", ["available", "not available"])
    
    if st.button("Tambahkan"):
        if product_code and name and price:
            cursor.callproc("AddMenu", (product_code, name, price, category, available))
            conn.commit()
            st.success("✅ Menu berhasil ditambahkan!")
        else:
            st.warning("⚠️ Harap isi semua field!")

    # Hapus Menu
    # st.subheader("❌ Hapus Menu")
    cursor.execute("SELECT productCode, productName FROM menu")
    menu_items = cursor.fetchall()
    menu_df = pd.DataFrame(menu_items)

    # if not menu_df.empty:
    #     delete_code = st.selectbox("Pilih menu yang akan dihapus", menu_df["productCode"].tolist())
    #     if st.button("Hapus"):
    #         cursor.callproc("DeleteMenu", (delete_code,))
    #         conn.commit()
    #         st.success("✅ Menu berhasil dihapus!")

    # Update Ketersediaan Menu
    st.subheader("🔄 Update Ketersediaan Menu")
    update_code = st.selectbox("Pilih menu yang akan diperbarui", menu_df["productCode"].tolist())
    new_availability = st.selectbox("Status Ketersediaan", ["available", "not available"])
    if st.button("Update Ketersediaan"):
        cursor.callproc("UpdateMenuAvailability", (update_code, new_availability))
        conn.commit()
        st.success("✅ Ketersediaan menu berhasil diperbarui!")

    # Lihat Pendapatan
    st.subheader("💰 Total Pendapatan")
    start_date = st.date_input("Dari Tanggal")
    end_date = st.date_input("Sampai Tanggal")
    
    if st.button("Cek Pendapatan"):
        cursor.callproc("GetIncomeInRange", (start_date, end_date))
        income = cursor.fetchone()["totalIncome"] or 0
        st.metric("Total Pendapatan", f"Rp {income:,.2f}")



    cursor.close()
    conn.close()
