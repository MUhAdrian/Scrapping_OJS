import argparse
import sys
import requests
import re
import csv
import shutil
from bs4 import BeautifulSoup
from pathlib import Path

#pip install requests beautifulsoup4 terlebih dahulu di terminal ya geys


def setup_argparse():
    parser = argparse.ArgumentParser(description="Academic Publication Collector (Target: jurnal.pelitabangsa.ac.id)")
    
    # Syarat 6: Sedikitnya 3 argumen CLI (Di sini kita sediakan 5)
    parser.add_argument('--url', default='https://jurnal.pelitabangsa.ac.id/', help='Base URL target scraping')
    parser.add_argument('--keyword', required=True, help='Kata kunci pencarian publikasi (wajib)')
    parser.add_argument('--limit', type=int, default=30, help='Jumlah maksimal data yang diambil (default: 30)')
    parser.add_argument('--output', default='output_data', help='Nama folder output (default: output_data)')
    parser.add_argument('--backup', action='store_true', help='Tambahkan flag ini untuk membuat file backup .zip')
    
    return parser.parse_args()

def clean_text(text):
    # Syarat 2 (Regex 1): Pembersihan data
    # Menghapus enter (\n), tab (\t), dan spasi ganda menjadi satu spasi saja
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()

def extract_date(text):
    # Syarat 2 (Regex 2): Ekstraksi data spesifik
    # Mencari pola 4 digit angka yang diawali 19 atau 20 (contoh: 2021, 1998)
    match = re.search(r'\b\d{4}-\d{2}-\d{2}\b', text)
    return match.group(0) if match else "Tidak diketahui"

def scrape_ojs(args):
    # Parameter pencarian jurnal (mengambil 50 data per halaman agar aman untuk limit 30)
    search_url = f"{args.url}/search/search?query={args.keyword}"
    
    print(f"[INFO] Menghubungi: {search_url}")
    
    try:
        # Syarat 7: Menangani kegagalan koneksi
        response = requests.get(search_url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal terhubung ke website: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='obj_article_summary') 

    # Syarat 7: Menangani data kosong
    if not results:
        print(f"[WARNING] Tidak ada publikasi ditemukan untuk kata kunci '{args.keyword}'.")
        sys.exit(0)

    publications = []
    
    for item in results:
       
        # Stop jika sudah mencapai limit yang diminta
        if len(publications) >= args.limit:
            break

        # Ambil Judul
        title_tag = item.find('h2', class_='title')
        title = clean_text(title_tag.text) if title_tag else "Tanpa Judul"
        if args.keyword.lower() not in title.lower():
            continue

        # Ambil Penulis
        authors_tag = item.find('div', class_='authors')
        authors = clean_text(authors_tag.text).replace("Authors:", "").strip() if authors_tag else "Tanpa Penulis"

        # Ambil Tanggal & Ekstrak Tahun menggunakan Regex
        date_tag = item.find('div', class_='published')
        tanggal = extract_date(date_tag.text) if date_tag else "Tidak diketahui"

        # Ambil Link
        #link_tag = item.find('p', class_='list-title is-inline-block')
        #link = link_tag.find('a')['href'] if link_tag and link_tag.find('a') else "Tidak ada link"
        link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else "Tidak ada link"

        publications.append({
            'Judul': title,
            'Penulis': authors,
            'Tanggal': tanggal,
            'URL': link
        })
        
    return publications

def save_and_backup(publications, args):
    # Syarat 4: Membuat folder output secara otomatis menggunakan pathlib
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / f"jurnal_{args.keyword}.csv"
    
    try:
        # Syarat 3: Menyimpan data dalam format .csv
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Judul', 'Penulis', 'Tanggal', 'URL'])
            writer.writeheader()
            writer.writerows(publications)
    except IOError as e:
        # Syarat 7: Menangani kegagalan tulis file
        print(f"[ERROR] Gagal menyimpan file: {e}")
        sys.exit(1)

    backup_status = "Tidak ada"
    # Syarat 5: Membuat backup hasil pemrosesan dalam format .zip
    if args.backup:
        try:
            shutil.make_archive(str(output_dir), 'zip', str(output_dir))
            backup_status = f"{args.output}.zip"
        except Exception as e:
            print(f"[ERROR] Gagal membuat backup: {e}")

    return file_path, backup_status

def main():
    args = setup_argparse()
    
    print("="*50)
    print("Mulai Proses Scraping...")
    print("="*50)
    
    # Ambil data
    publications = scrape_ojs(args)
    
    # Simpan dan backup
    file_path, backup_status = save_and_backup(publications, args)
    
    # Syarat 8: Menampilkan ringkasan pemrosesan pada terminal
    print("\n" + "="*50)
    print("RINGKASAN PEMROSESAN")
    print("="*50)
    print(f"Kata Kunci       : {args.keyword}")
    print(f"Data Ditemukan   : {len(publications)} records")
    print(f"File Tersimpan   : {file_path}")
    print(f"Backup ZIP       : {backup_status}")
    print("="*50)
    print("Proses Selesai!")

if __name__ == "__main__":
    main()