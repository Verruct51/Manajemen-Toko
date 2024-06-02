from tabulate import tabulate

# Fungsi untuk membaca data buah dari file
def baca_data_buah():
    data_buah = []
    try:
        with open('DataBuah.txt', 'r') as file:
            for line in file:
                data = line.strip().split(';')
                data_buah.append({
                    'kode': data[0],
                    'nama': data[1],
                    'stok': int(data[2]),
                    'harga': int(data[3]),
                    'stok_terakhir': int(data[2]),
                    'total_penjualan': 0,  
                    'jumlah_terjual': 0  
                })
    except FileNotFoundError:
        print("File 'DataBuah.txt' tidak ditemukan. Buat file tersebut terlebih dahulu.")
    return data_buah

# Fungsi untuk menulis data buah ke file
def tulis_data_buah(data_buah):
    with open('DataBuah.txt', 'w') as file:
        for buah in data_buah:
            file.write(f"{buah['kode']};{buah['nama']};{buah['stok']};{buah['harga']}\n")

# Fungsi untuk melakukan penjualan
def penjualan_buah(data_buah):
    print("====================================================================")
    print("Toko Buah Tropic Palette".center(60))
    print("====================================================================")

    manage_buah(data_buah)

    # Meminta input untuk setiap jenis buah yang ingin dibeli
    beli_buah = []
    banyak_jenis = int(input("\nMasukkan Banyak Jenis Buah : "))
    
    for i in range(banyak_jenis):
        while True:
            print("\nJenis Buah Ke-", i + 1)
            kode_buah = input("Masukkan kode buah : ")
            jumlah_beli = int(input("Jumlah Pembelian   : "))

            buah_valid = False
            for buah in data_buah:
                if buah['kode'] == kode_buah:
                    buah_valid = True
                    break

            if not buah_valid:
                print(f"Kode buah '{kode_buah}' tidak valid. Silakan masukkan kode buah yang benar.")
            else:
                buah['jumlah_terjual'] += jumlah_beli  # Update jumlah_terjual
                beli_buah.append({'kode': kode_buah, 'jumlah': jumlah_beli})
                break

    # Tampilan struk
    print("====================================================================")
    print("Toko Buah Tropic Palette".center(60))
    print("Jalan raya tangkis".center(60))
    print("08324354542".center(60))
    print("====================================================================")
    print("Jenis Buah                    Qty         Subtotal")
    print("====================================================================")

    total_harga = 0

    for pembelian in beli_buah:
        kode_buah = pembelian['kode']
        jumlah = pembelian['jumlah']

        for buah in data_buah:
            if buah['kode'] == kode_buah:
                subtotal = jumlah * buah['harga']
                total_harga += subtotal
                buah['total_penjualan'] += subtotal  # Update total_penjualan
                print(f"{buah['nama'].ljust(30)} {jumlah}          Rp {subtotal}")

                # Mengurangi stok setelah penjualan
                buah['stok'] -= jumlah
                buah['stok_terakhir'] -= jumlah

    print("====================================================================")
    print(f"Total   : Rp {total_harga}")

    bayar = int(input("Bayar   : Rp "))
    kembali = bayar - total_harga
    print("--------------------------------------------------------------------")
    print(f"Kembali : Rp {kembali}")
    
    print("====================================================================")
    print("TERIMAKASIH".center(60))
    print("SILAKAN DATANG KEMBALI".center(60))
    print("====================================================================")

# Fungsi untuk merekap penjualan
def rekap_penjualan(data_buah):
    print("\nRekap Penjualan")
    headers = ["Kode", "Nama Buah", "Stok Terakhir", "Jumlah Terjual", "Total Penjualan"]
    table_data = []

    for buah in data_buah:
        table_data.append([buah['kode'], buah['nama'], buah['stok_terakhir'], buah['jumlah_terjual'], f"Rp {buah['total_penjualan']}"])

    print(tabulate(table_data, headers, tablefmt="grid"))

    # Reset stok_terakhir, jumlah_terjual, dan total_penjualan setelah rekap
    for buah in data_buah:
        buah['stok_terakhir'] = buah['stok']
        buah['jumlah_terjual'] = 0
        buah['total_penjualan'] = 0

# Fungsi untuk menampilkan menu dan meminta input pengguna
def tampilkan_menu():
    print("\nMenu:")
    print("1. Manage Buah")
    print("2. Penjualan Buah")
    print("3. Pengadaan Buah")
    print("4. Rekap Penjualan")
    print("5. Keluar")

    pilihan = input("\nPilih menu (1-5): ")
    return pilihan

# Fungsi untuk mengelola buah
def manage_buah(data_buah):
    table_data = []
    print("\nDaftar Data Buah")
    for buah in data_buah:
        table_data.append([buah['kode'], buah['nama'], buah['stok'], f"Rp {buah['harga']}"])

    headers = ["Kode", "Nama Buah", "Stok", "Harga"]
    print(tabulate(table_data, headers, tablefmt="grid"))

# Fungsi untuk melakukan pengadaan buah
def pengadaan_buah(data_buah):
    print("\nPengadaan Buah")
    manage_buah(data_buah)
    kode_buah = input("\nKode Buah     : ")

    # Check apakah kode buah valid
    buah_valid = False
    for buah in data_buah:
        if buah['kode'] == kode_buah:
            buah_valid = True
            break

    if not buah_valid:
        print(f"Kode buah '{kode_buah}' tidak valid. Tidak dapat melakukan pengadaan.")
    else:
        tambah_stok = int(input("Jumlah Tambah : "))

        # Menambah stok setelah pengadaan
        for buah in data_buah:
            if buah['kode'] == kode_buah:
                buah['stok'] += tambah_stok
                print(f"\nStok buah {buah['nama']} ({buah['kode']}) sebanyak {tambah_stok} buah berhasil ditambahkan!!.")
                buah['stok_terakhir'] += tambah_stok  # Update stok_terakhir

# Fungsi utama
def main():
    data_buah = baca_data_buah()

    while True:
        pilihan = tampilkan_menu()

        if pilihan == '1':
            manage_buah(data_buah)
        elif pilihan == '2':
            penjualan_buah(data_buah)
        elif pilihan == '3':
            pengadaan_buah(data_buah)
        elif pilihan == '4':
            rekap_penjualan(data_buah)
        elif pilihan == '5':
            tulis_data_buah(data_buah)
            print("Program selesai. Data tersimpan.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()