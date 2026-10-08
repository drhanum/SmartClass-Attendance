# Smart Class Attendance & Analytics System (CLI)

import json

NAMA_FILE = "data.json"

# 1. PENGELOLA DATA (membaca & menyimpan data.json)
def baca_data():
    # Membaca data.json dan mengembalikannya sebagai dictionary
    file = open(NAMA_FILE, "r")
    data = json.load(file)
    file.close()
    return data


def simpan_data(data):
    # Menyimpan dictionary data ke data.json
    file = open(NAMA_FILE, "w")
    json.dump(data, file, indent=2)
    file.close()


# 2. SEARCHING (Binary Search)
def binary_search(daftar, target):
    kiri = 0
    kanan = len(daftar) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        if daftar[tengah][0] == target:
            return tengah
        elif daftar[tengah][0] < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1


# 3. SORTING (Selection Sort manual)
def selection_sort(arr, turun):
    n = len(arr)
    for i in range(n - 1):
        pilih = i
        for j in range(i + 1, n):
            if turun == True:
                if arr[j][0] > arr[pilih][0]:
                    pilih = j
            else:
                if arr[j][0] < arr[pilih][0]:
                    pilih = j
        # tukar posisi i dengan elemen terpilih
        sementara = arr[i]
        arr[i] = arr[pilih]
        arr[pilih] = sementara
    return arr


# 4. REKURSI (tanpa for / while)
def hitung_rekursif(matriks, baris, kolom):
    # Menghitung total [Hadir, Sakit, Izin, Alpha] dari array 2D
    if baris == len(matriks):                  # base case 1: semua baris selesai
        return [0, 0, 0, 0]
    if kolom == len(matriks[baris]):           # base case 2: kolom habis -> baris berikutnya
        return hitung_rekursif(matriks, baris + 1, 0)

    hasil = hitung_rekursif(matriks, baris, kolom + 1)   # hitung sisa sel di kanan
    status = matriks[baris][kolom]
    if status == "H":
        hasil[0] = hasil[0] + 1
    elif status == "S":
        hasil[1] = hasil[1] + 1
    elif status == "I":
        hasil[2] = hasil[2] + 1
    elif status == "A":
        hasil[3] = hasil[3] + 1
    return hasil


def hitung_iteratif(matriks):
    # Versi LOOP dari hitung_rekursif (pembanding), hasil sama
    hasil = [0, 0, 0, 0]
    for baris in matriks:
        for status in baris:
            if status == "H":
                hasil[0] = hasil[0] + 1
            elif status == "S":
                hasil[1] = hasil[1] + 1
            elif status == "I":
                hasil[2] = hasil[2] + 1
            elif status == "A":
                hasil[3] = hasil[3] + 1
    return hasil


# 5. FUNGSI BANTU
def hitung_persen(hasil):
    # Persentase hadir = jumlah hadir / total pertemuan x 100
    total = hasil[0] + hasil[1] + hasil[2] + hasil[3]
    if total == 0:
        return 0.0
    return hasil[0] / total * 100


def cari_nama(users, nim):
    # Mencari nama mahasiswa dari NIM
    for user in users:
        if user["role"] == "mahasiswa" and user["nim"] == nim:
            return user["nama"]
    return "-"


def matkul_dosen(data, nidn):
    # Mengambil daftar matkul milik seorang dosen (dicari lewat NIDN)
    hasil = []
    for m in data["matkul"]:
        if m["dosen"] == nidn:
            hasil.append(m)
    return hasil

# 6. MENU MAHASISWA
def view_presensi(data, user):
    # Menampilkan rekap presensi mahasiswa untuk setiap matkul
    print("\nNama :", user["nama"])
    print("NIM  :", user["nim"])
    print("-" * 85)
    print("Matkul".ljust(20), "Kode".ljust(7), "Persen".ljust(8),
          "Hadir".ljust(7), "Sakit".ljust(7), "Izin".ljust(7), "Alpha")
    print("-" * 85)

    for m in data["matkul"]:
        presensi_matkul = data["presensi"][m["kode"]]
        if user["nim"] in presensi_matkul:
            riwayat = presensi_matkul[user["nim"]]
            hasil = hitung_rekursif([riwayat], 0, 0)
            persen = round(hitung_persen(hasil), 1)
            print(m["nama"].ljust(20), m["kode"].ljust(7), (str(persen) + "%").ljust(8),
                  str(hasil[0]).ljust(7), str(hasil[1]).ljust(7),
                  str(hasil[2]).ljust(7), hasil[3])

    print("\nx. keluar")
    pilihan = input("Pilih: ")
    while pilihan != "x":
        pilihan = input("Ketik x untuk keluar: ")


def menu_mahasiswa(data, user):
    # Menu untuk mahasiswa
    while True:
        print("\n=== MENU MAHASISWA ===")
        print("1. View Presensi")
        print("2. Log Out")
        pilihan = input("Pilih: ")
        if pilihan == "1":
            view_presensi(data, user)
        elif pilihan == "2":
            return
        else:
            print("Pilihan tidak valid")


# 7. MENU DOSEN
def view_lap_kehadiran(data, user):
    # Laporan kehadiran per matkul, diurutkan dari persentase tertinggi
    for m in matkul_dosen(data, user["nidn"]):
        rekap = []
        for nim in data["presensi"][m["kode"]]:
            riwayat = data["presensi"][m["kode"]][nim]
            hasil = hitung_rekursif([riwayat], 0, 0)
            persen = hitung_persen(hasil)
            # persen ditaruh di indeks 0 karena selection_sort mengurutkan indeks 0
            rekap.append([persen, cari_nama(data["users"], nim), nim])

        rekap = selection_sort(rekap, True)

        print("\n=== " + m["kode"] + " - " + m["nama"] + " ===")
        print("Nama".ljust(20), "NIM".ljust(10), "Persentase")
        for baris in rekap:
            print(baris[1].ljust(20), baris[2].ljust(10), str(round(baris[0], 1)) + "%")


def minta_status(label):
    # Meminta input H/S/I/A
    # Mengembalikan 'X' jika dosen berhenti, '' (kosong) jika dilewati
    while True:
        status = input(label + " (H/S/I/A, Enter=lewati, x=berhenti): ").upper()
        if status in ["H", "S", "I", "A", "X", ""]:
            return status
        print("Input salah, isi H / S / I / A")
 
 
def proses_matkul(data, matkul):
    # Input presensi untuk satu matkul
    riwayat = data["presensi"][matkul["kode"]]
 
    # Buat list [nim, nama] lalu urutkan berdasarkan NIM (syarat binary search)
    daftar = []
    for nim in riwayat:
        daftar.append([nim, cari_nama(data["users"], nim)])
    daftar = selection_sort(daftar, False)
 
    jumlah = len(riwayat[daftar[0][0]])
    print("\nPertemuan tercatat:", jumlah)
    pilihan = input("Ketik nomor pertemuan, 'n' untuk pertemuan baru, 'x' keluar: ")
 
    if pilihan == "x":
        return
    elif pilihan == "n":
        # tambah 1 kolom baru di array 2D (default Alpha)
        for nim in riwayat:
            riwayat[nim].append("A")
        simpan_data(data)
        idx = jumlah
        print("Pertemuan ke-" + str(jumlah + 1) + " dibuat (semua diisi A dulu).")
    elif pilihan.isdigit() and 1 <= int(pilihan) <= jumlah:
        idx = int(pilihan) - 1
    else:
        print("Pertemuan tidak valid")
        return
 
    # TAHAP 1: isi status semua mahasiswa secara berurutan (tanpa pilih / ketik NIM)
    print("\nPertemuan ke-" + str(idx + 1) + ": isi status mahasiswa satu per satu")
    for i in range(len(daftar)):
        nim = daftar[i][0]
        nama = daftar[i][1]
        label = str(i + 1) + ". " + nama + " - " + nim + " : [" + riwayat[nim][idx] + "]"
        status = minta_status(label)
        if status == "X":
            break
        elif status != "":
            riwayat[nim][idx] = status
    simpan_data(data)
 
    # TAHAP 2 (opsional): koreksi mahasiswa tertentu
    while True:
        print("\nPertemuan ke-" + str(idx + 1))
        for i in range(len(daftar)):
            nim = daftar[i][0]
            nama = daftar[i][1]
            print(str(i + 1) + ". " + nama + " - " + nim + " : [" + riwayat[nim][idx] + "]")
        print("x. keluar")
 
        pilihan = input("Koreksi? Ketik NIM atau nomor urut (x = selesai): ")
        if pilihan == "x":
            return
 
        posisi = binary_search(daftar, pilihan)  # cari NIM dengan binary search
        if posisi == -1 and pilihan.isdigit() and 1 <= int(pilihan) <= len(daftar):
            posisi = int(pilihan) - 1            # kalau bukan NIM, anggap nomor urut
 
        if posisi == -1:
            print("Mahasiswa tidak ditemukan")
        else:
            nim = daftar[posisi][0]
            status = minta_status(daftar[posisi][1])
            if status != "X" and status != "":
                riwayat[nim][idx] = status
                simpan_data(data)


def input_presensi(data, user):
    # Menampilkan pilihan matkul milik dosen
    while True:
        daftar = matkul_dosen(data, user["nidn"])
        print("\n=== PILIH MATAKULIAH ===")
        for i in range(len(daftar)):
            print(str(i + 1) + ". " + daftar[i]["nama"])
        print("x. keluar")

        pilihan = input("Pilih: ")
        if pilihan == "x":
            return
        elif pilihan.isdigit() and 1 <= int(pilihan) <= len(daftar):
            proses_matkul(data, daftar[int(pilihan) - 1])
        else:
            print("Pilihan tidak valid")


def menu_dosen(data, user):
    # Menu untuk dosen
    while True:
        print("\n=== MENU DOSEN ===")
        print("Nama :", user["nama"])
        print("NIDN :", user["nidn"])
        print("1. View Lap Kehadiran")
        print("2. Input Presensi")
        print("3. Log Out")
        pilihan = input("Pilih: ")
        if pilihan == "1":
            view_lap_kehadiran(data, user)
        elif pilihan == "2":
            input_presensi(data, user)
        elif pilihan == "3":
            return
        else:
            print("Pilihan tidak valid")


# 8. LOGIN & MAIN
def login(data):
    # Meminta username & password. Jika salah tampil 'salah' lalu ulangi
    daftar = []
    for i in range(len(data["users"])):
        daftar.append([data["users"][i]["username"], i])   # [username, index asli]
    daftar = selection_sort(daftar, False)

    while True:
        print("\n=== LOGIN ===")
        username = input("Username (x = batal): ")
        if username == "x":
            return {}
        password = input("Password: ")

        posisi = binary_search(daftar, username)
        if posisi != -1:
            user = data["users"][daftar[posisi][1]]
            if user["password"] == password:
                return user
        print("salah")


def main():
    # Fungsi utama: mengatur Main Menu
    data = baca_data()

    while True:
        print("\n=== SMART CLASS ATTENDANCE & ANALYTICS SYSTEM ===")
        print("1. Login")
        print("2. Exit Program")
        pilihan = input("Pilih: ")

        if pilihan == "1":
            user = login(data)
            if user != {}:
                if user["role"] == "mahasiswa":
                    menu_mahasiswa(data, user)
                else:
                    menu_dosen(data, user)
        elif pilihan == "2":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid")


main()