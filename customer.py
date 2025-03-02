import streamlit as st
import pandas as pd
from database import get_connection

def customer_view():
    st.title("📜 Menu Makanan")
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Tampilkan Menu yang Tersedia
    cursor.execute("SELECT * FROM menu WHERE availability='available'")
    menu_items = cursor.fetchall()
    df = pd.DataFrame(menu_items)

    if not df.empty:
        st.dataframe(df[['productCode', 'productName', 'price']])
        st.subheader("🛒 Buat Pesanan")

        customer_phone = st.text_input("📞 Nomor Telepon Anda", max_chars=15)
        table_number = st.number_input("🍽️ Nomor Meja", min_value=1, value=1)
        payment_method = st.selectbox("💰 Metode Pembayaran", ["cash", "cashless"])

        selected_items = st.multiselect(
            "📌 Pilih Menu", df["productCode"].tolist(), 
            format_func=lambda x: df[df["productCode"] == x]["productName"].values[0]
        )

        quantities = {
            item: st.number_input(
                f"🔢 Jumlah {df[df['productCode'] == item]['productName'].values[0]}", 
                min_value=1, value=1
            ) for item in selected_items
        }

        # Hitung Total Harga
        total_price = sum(df[df["productCode"] == item]["price"].values[0] * qty for item, qty in quantities.items())
        total_price = int(total_price)  # Pastikan tipe data integer
        st.write(f"💵 **Total Harga: Rp {total_price:,.2f}**")

        if st.button("Pesan Sekarang"):
            if customer_phone and selected_items:
                # Konversi tipe data sebelum dikirim ke MySQL
                customer_phone = str(customer_phone)
                table_number = int(table_number)
                payment_method = str(payment_method)

                # Panggil Stored Procedure AddOrder
                args = (customer_phone, table_number, total_price, payment_method)
                cursor.callproc("AddOrder", args)
                
                # Ambil Order Number yang baru dibuat
                cursor.execute("SELECT LAST_INSERT_ID() AS orderNumber")
                orderNumber = cursor.fetchone()["orderNumber"]

                # Masukkan setiap item ke tabel order_details
                for item_id, qty in quantities.items():
                    cursor.execute(
                        "INSERT INTO order_details (orderNumber, productCode, quantityOrdered) VALUES (%s, %s, %s)", 
                        (orderNumber, item_id, qty)
                    )

                # Update totalAmount di tabel orders
                cursor.execute("UPDATE orders SET totalAmount = %s WHERE orderNumber = %s", (total_price, orderNumber))

                conn.commit()
                st.success(f"✅ Pesanan berhasil dibuat! Order No: {orderNumber}")

            else:
                st.warning("⚠️ Harap isi semua field!")

    else:
        st.info("ℹ️ Menu belum tersedia.")

    cursor.close()
    conn.close()
