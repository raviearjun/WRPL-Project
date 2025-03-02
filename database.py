import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Sesuaikan dengan username MySQL Anda
        password="",  # Sesuaikan dengan password MySQL Anda
        database="seafood_database"
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        if conn.is_connected():
            print("✅ Koneksi ke database berhasil!")
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ Gagal terhubung ke database: {err}")

    input("Tekan ENTER untuk keluar...")
