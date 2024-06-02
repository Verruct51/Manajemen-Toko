from tabulate import tabulate

def read_data():
    data_buku = []
    with open('DataBuku.txt', 'r') as file:
        for line in file:
            data = line.strip().split(';')
            data_buku.append({
                "Kode": data[0],
                "Judul": data[1],
                "Penulis": data[2],
                "Penerbit": data[3],
                "Tahun": int(data[4]),
                "Harga": int(data[5]),
                "Stok": int(data[6])
            })
    return data_buku

def manage_buku(data_buku):
    table_data = []
    print("DAFTAR DATA BUKU")
    for buku in data_buku:
        table_data.append([buku['Kode'], buku['Judul'], buku['Penulis'], buku['Penerbit'], buku['Tahun'], f"Rp {buku['Harga']}", buku['Stok']])

    headers = ["Kode", "Judul", "Penulis", "Penerbit", "Tahun", "Harga", "Stok"]
    print(tabulate(table_data, headers, tablefmt="grid"))

def input_buku():
    kode = input('Masukkan Kode : ')
    judul = input('Masukkan Judul Buku   : ')
    penulis = input('Masukkan Penulis      : ')
    penerbit = input('Masukkan Penerbit     : ')
    tahun = input('Masukkan tahun terbit : ')
    harga = input('Masukkan Harga        : ')
    stok = input('Masukkan Stok         : ')

    return {
        "Kode": kode,
        "Judul": judul,
        "Penulis": penulis,
        "Penerbit": penerbit,
        "Tahun": int(tahun),
        "Harga": int(harga),
        "Stok": int(stok)
    }

def update_data(data_buku):
    print("\nMENAMBAHKAN / UPDATE BUKU BARU")
    manage_buku(data_buku)
    while True:
        kode = input('Masukkan Kode : ')
        existing_book = next((buku for buku in data_buku if buku['Kode'] == kode), None)

        if existing_book:
            print(f"\nUpdate data untuk buku dengan kode {kode}")
            existing_book['Judul'] = input('Masukkan Judul Buku   : ')
            existing_book['Penulis'] = input('Masukkan Penulis      : ')
            existing_book['Penerbit'] = input('Masukkan Penerbit     : ')
            existing_book['Tahun'] = int(input('Masukkan tahun terbit : '))
            existing_book['Harga'] = int(input('Masukkan Harga        : '))
            existing_book['Stok'] = int(input('Masukkan Stok         : '))
            print('Data buku berhasil diupdate')
        else:
            print('\nMenambahkan Buku Baru')
            new_book = input_buku()
            data_buku.append(new_book)
            print('Buku berhasil ditambahkan ke dalam file')

        is_done = input('DONE/NOT? ')
        if is_done.upper() == 'DONE':
            write_data(data_buku)
            break

def write_data(data):
    with open("DataBuku.txt", "w") as f:
        for buku in data:
            f.write(f"{buku['Kode']};{buku['Judul']};{buku['Penulis']};{buku['Penerbit']};{buku['Tahun']};{buku['Harga']};{buku['Stok']}\n")

def delete_data(data_buku):
    print("\nHAPUS DATA BUKU\n")
    manage_buku(data_buku)
    kode = input("Masukkan kode buku yang akan dihapus: ")
    deleted_book = next((buku for buku in data_buku if buku['Kode'] == kode), None)

    if deleted_book:
        data_buku.remove(deleted_book)  # Hapus buku dari data_buku
        write_data(data_buku)  # Simpan perubahan ke dalam file DataBuku.txt
        print(f"\nBuku dengan kode {kode} berhasil dihapus.")
        manage_buku(data_buku)
    else:
        print(f"\nBuku dengan kode {kode} tidak ditemukan.")

def penjualan(data_buku, no_transaksi):
    def garis_1():
        print('-' * 100)

    def garis_2():
        print('=' * 100)

    manage_buku(data_buku)
    beli_buku = []
    banyak_buku = int(input("\nMasukkan banyak buku yang dibeli: "))
    
    for i in range(banyak_buku):
        while True:
            print("\nJenis Buku Ke-", i + 1)
            kode_buku = input("Masukkan kode buku: ")
            jumlah_beli = int(input("Jumlah Pembelian   : "))
            
            buku_found = next((buku for buku in data_buku if buku['Kode'] == kode_buku), None)

            if buku_found and jumlah_beli <= buku_found['Stok']:
                buku_found['Stok'] -= jumlah_beli  # Kurangi stok buku
                beli_buku.append({'kode': kode_buku, 'jumlah': jumlah_beli})
                break
            elif buku_found:
                print("Maaf, stok tidak mencukupi.")
            else:
                print("Maaf, kode buku tidak valid. Silakan coba lagi.")

    garis_2()
    print("TRI MEDIA BOOK STORE".center(100))
    print("Jln Jayabaya No 12 KEDIRI".center(100))
    print("081515572295".center(100))
    garis_2()
    print("Judul buku                                   Qty                                         Subtotal")
    garis_2()

    subtotal = 0
    for pembelian in beli_buku:
        kode_buku = pembelian['kode']
        jumlah = pembelian['jumlah']

        for buku in data_buku:
            if buku['Kode'] == kode_buku:
                subtotal += jumlah * buku['Harga']
                print(f"{buku['Judul'].ljust(45)} {jumlah}                                          Rp {subtotal}")
                break  # Hentikan loop setelah menemukan buku yang sesuai

    garis_2()
    print(f"Total   : Rp {subtotal}")

    total_pembayaran = int(input("Bayar   : Rp "))
    kembali = total_pembayaran - subtotal
    garis_1()
    print(f"Kembali : Rp {kembali}")

    garis_2()
    print("TERIMAKASIH".center(100))
    print("SILAKAN DATANG KEMBALI".center(100))
    garis_2()

    # Simpan informasi transaksi ke dalam file rekap_penjualan.txt
    with open("rekap_penjualan.txt", "a") as rekap_file:
        kode_buku_list = [pembelian['kode'] for pembelian in beli_buku]
        jumlah_pembelian_list = [str(pembelian['jumlah']) for pembelian in beli_buku]
        rekap_file.write(f"{no_transaksi};{','.join(kode_buku_list)};{','.join(jumlah_pembelian_list)};{subtotal}\n")
        no_transaksi += 1

    write_data(data_buku)  # Menyimpan perubahan stok ke dalam file DataBuku.txt

    return no_transaksi

def rekap():
    print('\nRekap Penjualan')
    print("No Transaksi  | Kode Buku                      | Jumlah Pembelian   | Subtotal")
    print('-' * 100)

    with open("rekap_penjualan.txt", "r") as rekap_file:
        for line in rekap_file:
            data_rekap = line.strip().split(';')
            no_transaksi = data_rekap[0]
            kode_buku = data_rekap[1].split(',')
            jumlah_pembelian = data_rekap[2].split(',')
            subtotal = data_rekap[3]

            print(f"{no_transaksi.ljust(13)} | {', '.join(kode_buku).ljust(30)} | {', '.join(jumlah_pembelian).ljust(17)}  | Rp {subtotal}")

    print('-' * 100)


def menu():
    print("\nSELAMAT DATANG DI BOOK STORE")
    print("MENU : ")
    print("1.Manage Buku")
    print("2.Update Buku ")
    print("3.Delete Buku ")
    print("4.Penjualan Buku ")
    print("5.Rekap Penjualan")
    print("6.Keluar")
    pilihan = input("\nPilih menu (1-6): ")
    return pilihan

def main():
    data_buku = read_data()
    no_transaksi = 1  # Inisialisasi nomor transaksi

    while True:
        pilihan = menu()

        if pilihan == '1':
            manage_buku(data_buku)
        elif pilihan == '2':
            update_data(data_buku)
        elif pilihan == '3':
            delete_data(data_buku)
        elif pilihan == '4':
            no_transaksi = penjualan(data_buku, no_transaksi)
        elif pilihan == '5':
            rekap()
        elif pilihan == '6':
            print("\nProgram selesai. Data tersimpan.\n")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()
