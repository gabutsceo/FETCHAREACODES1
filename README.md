# FETCHAREACODES
FETCH AREA CODES US PHONE NUMBER  FOR EDUCATIONAL PURPOSE
# Area Code Fetcher Script

Script ini digunakan untuk mengambil **area codes** berdasarkan nama kota dan negara bagian menggunakan API dari [API Ninjas](https://api-ninjas.com). Hasilnya akan disimpan dalam format JSON, dan data akan disinkronisasi dengan file sebelumnya jika sudah ada.

## Fitur
- Mengambil data area codes dari API berdasarkan kota dan negara bagian.
- Membaca nama kota dari file input.
- Menyimpan hasil dalam file JSON secara terorganisir.
- Sinkronisasi data secara otomatis tanpa menimpa data sebelumnya.
- Menangani duplikasi data secara otomatis.

---

## Persyaratan
1. Python 3.x harus terinstal di sistem Anda.
2. Modul Python yang dibutuhkan:
   - `requests`
   - `json`
   - `os`
   - `time`
3. API Key dari [API Ninjas](https://api-ninjas.com).

---



## Cara Menggunakan

1. **Clone atau Salin Script:**
   Unduh atau salin script ini ke dalam folder lokal Anda.

2. **Siapkan File Input:**
   Buat file teks dengan nama sesuai kebutuhan, misalnya `CA.txt`, yang berisi daftar nama kota (satu nama kota per baris). Contoh isi file:

3. **Jalankan Script:**
Buka terminal atau command prompt, lalu jalankan script menggunakan perintah:
```bash
python index.py

4. **Jalankan Script:**
Enter the file name containing city names (e.g., CA.txt): CA.txt

5. **Jalankan Script:**
Enter the state (e.g., CA, OR, TX): CA
