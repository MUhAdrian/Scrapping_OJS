#KElompok
MUH.aDrian A.F 312310648.
FIkri FIrmansyah.
Endang sirait.
Theresia tababan.


# 📚 Academic Publication Collector (OJS Scraper)

Proyek ini adalah program *Web Scraper* berbasis Command Line Interface (CLI) yang dibangun menggunakan Python. Program ini dirancang khusus untuk mengumpulkan metadata publikasi akademik (Judul, Penulis, Tanggal, dan URL) dari portal jurnal yang menggunakan sistem **Open Journal Systems (OJS)**.

Program ini memenuhi seluruh persyaratan tugas, termasuk penggunaan Regular Expressions, Argumen CLI, pengelolaan file (*saving* CSV & *backup* ZIP), dan penanganan error.

---

## 🛠️ Persyaratan Sistem (Requirements)

Pastikan Anda telah menginstal pustaka eksternal yang dibutuhkan sebelum menjalankan program ini.

Daftar pustaka tersedia di file `requirements.txt` dan dapat diinstal dengan perintah berikut:

```bash
pip install -r requirements.txt
```

Atau Anda dapat menginstalnya secara manual:

```bash
pip install requests beautifulsoup4
```

---

## 🚀 Petunjuk Penggunaan (CLI Arguments)

Program ini dijalankan melalui terminal atau command prompt dengan memasukkan argumen tertentu.

### Sintaks Dasar

```bash
python main.py --url <TARGET_URL> --keyword <KATA_KUNCI> [ARGUMEN_TAMBAHAN...]
```

### Daftar Parameter

| Argumen     | Status   | Deskripsi                                                              |
|-------------|----------|------------------------------------------------------------------------|
| `--url`     | Wajib    | URL halaman pencarian dari target portal OJS.                          |
| `--keyword` | Wajib    | Kata kunci pencarian jurnal yang ingin diambil datanya.                |
| `--limit`   | Opsional | Batas maksimal jumlah data yang diambil (Default: `30`).               |
| `--output`  | Opsional | Nama folder untuk menyimpan hasil scraping (Default: `output_data`).   |
| `--backup`  | Opsional | Tambahkan flag ini untuk mengaktifkan fitur auto-backup ke format `.zip`. |

---

## 💡 Contoh Pemanggilan Program

Berikut adalah contoh untuk mengambil jurnal terkait "sistem" dari portal jurnal OJS kampus:

```bash
python main.py --url https://jurnal.pelitabangsa.ac.id/index.php/sigma --keyword sistem --limit 30 --backup
```

### Alur Kerja Program

1. Program akan mengakses URL target dan melakukan pencarian berdasarkan kata "sistem".
2. Program akan mengekstrak Judul, Penulis, Tanggal Publikasi, dan URL dari maksimal 30 artikel.
3. Regular Expressions (Regex) digunakan untuk membersihkan format teks (*cleaning*) dan memastikan format tanggal sesuai standar (`YYYY-MM-DD`).
4. Hasil (dataset) akan disimpan secara otomatis ke dalam format `jurnal_sistem.csv` di dalam folder `output_data`.
5. Karena flag `--backup` digunakan, program akan membuat salinan folder output ke dalam bentuk file `output_data.zip`.
6. Jika proses selesai, ringkasan pemrosesan akan ditampilkan di layar terminal.

---

## ⚠️ Penanganan Kendala (Error Handling)

Sistem ini telah dilengkapi dengan mekanisme *error handling* untuk mengatasi beberapa skenario:

- **Koneksi Gagal/Timeout:** Menampilkan pesan error spesifik dan menghentikan proses secara aman (tidak *crash*).
- **Data Kosong:** Jika kata kunci tidak ditemukan, program memberikan *warning* dan berhenti dengan status sukses (kode `0`).
- **Format Teks Kotor:** Ditangani dengan Regex agar hasil CSV tetap rapi.

---

*Dibuat untuk memenuhi tugas mata kuliah Praktikum Web Scraping/Pemrograman.*
