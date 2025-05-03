# ETL Fashion Studio

![Image](https://github.com/user-attachments/assets/fdea4cf2-7e79-4fe1-b1fe-cb9bd8e1bbab)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-2.2.3-brightgreen)](https://pandas.pydata.org/)
[![Google Sheets API](https://img.shields.io/badge/Google%20Sheets%20API-v4-red)](https://developers.google.com/sheets/api)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-compatible-blue)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Overview

ETL Fashion Studio adalah pipeline data yang mengekstrak, mentransformasi, dan memuat data produk fashion dari sumber web ke berbagai repositori data. Proyek ini memungkinkan analisis data fashion secara otomatis dan terstruktur.

## 🌟 Fitur

- **Ekstraksi Data**: Web scraping data produk fashion secara otomatis
- **Transformasi Data**: Pembersihan dan standardisasi format data produk
- **Loading Data**: Penyimpanan ke berbagai repositori (CSV, Google Sheets, PostgreSQL)
- **Logging**: Pencatatan proses ETL yang komprehensif
- **Error Handling**: Penanganan kesalahan yang robust

## 🛠️ Teknologi

- **Python 3.8+**: Bahasa pemrograman utama
- **BeautifulSoup**: Ekstraksi data dari website
- **Pandas**: Manipulasi dan transformasi data
- **Google Sheets API**: Penyimpanan data ke Google Sheets
- **SQLAlchemy**: Koneksi dan penyimpanan data ke PostgreSQL
- **Pytest**: Testing otomatis

## 🚀 Instalasi

### Prasyarat

- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Akses internet untuk mengunduh dependencies

### Langkah Instalasi

1. Clone repositori:

```bash
   git clone https://github.com/habstrakT808/ETL---Fashion-Studio-Store.git
   cd ETL-Fashion-Studio
```

2. Buat virtual environment (opsional tapi direkomendasikan):

```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   # ATAU
   venv\Scripts\activate  # Untuk Windows
```

3. Instal dependencies:

```bash
   pip install -r requirements.txt
```

4. Setup kredensial Google Sheets API (lihat bagian berikutnya)

## 🔑 Mendapatkan Google Sheets API Credentials

Untuk menggunakan fitur Google Sheets, Anda perlu membuat file kredensial JSON. Ikuti langkah-langkah berikut:

1. **Buat Project di Google Cloud Console**

- Kunjungi [Google Cloud Console](https://console.cloud.google.com/)
- Buat project baru (misalnya "ETL Fashion Studio")
- Catat Project ID yang dibuat

2. **Aktifkan Google Sheets API**

- Di sidebar, pilih "APIs & Services" > "Library"
- Cari "Google Sheets API" dan aktifkan

3. **Buat Service Account**

- Di sidebar, pilih "APIs & Services" > "Credentials"
- Klik "Create Credentials" > "Service Account"
- Isi informasi service account (nama, deskripsi)
- Berikan role "Editor" untuk akses penuh ke spreadsheets
- Klik "Done"

4. **Buat Key untuk Service Account**

- Dalam daftar service account, klik service account yang baru dibuat
- Pilih tab "Keys"
- Klik "Add Key" > "Create new key"
- Pilih format JSON
- Klik "Create" (file JSON akan diunduh otomatis)

5. **Simpan File Kredensial**

- Rename file JSON yang diunduh menjadi `google-sheets-api.json`
- Pindahkan file ke direktori root proyek ETL Fashion Studio

Dengan langkah-langkah di atas, Anda akan memiliki file `google-sheets-api.json` yang diperlukan untuk mengakses Google Sheets API. File ini harus disimpan di direktori proyek dan **JANGAN** di-commit ke repositori Git (sudah ditambahkan ke .gitignore).

## 📊 Penggunaan

### Menjalankan ETL Pipeline

```bash
python main.py
```

### Menjalankan Unit Tests

```bash
python -m pytest tests
```

### Menjalankan Test Coverage

```bash
coverage run -m pytest tests
coverage report
```

## 📁 Struktur Proyek

```javascript
ETL-Fashion-Studio/
├── main.py                   # File utama untuk menjalankan ETL pipeline
├── requirements.txt          # Dependencies proyek
├── .gitignore                # File yang diabaikan oleh Git
├── README.md                 # Dokumentasi proyek
├── products.csv              # Output CSV dari pipeline ETL
├── google-sheets-api.json    # File kredensial Google API (tidak di-commit)
├── utils/                    # Modul utilitas
│   ├── __init__.py
│   ├── extract.py            # Modul ekstraksi data
│   ├── transform.py          # Modul transformasi data
│   └── load.py               # Modul loading data
└── tests/                    # Unit tests
    ├── __init__.py
    ├── test_extract.py
    ├── test_transform.py
    └── test_load.py
```

## 📈 Contoh Output

### CSV Output

![image](https://github.com/user-attachments/assets/86831342-43f5-4ac0-a192-01b57bb5f128)

### Google Sheets

Akses Google Sheets yang dibuat melalui URL:
https://docs.google.com/spreadsheets/d/19_lA9Zj8XaA_Usb5mjo3j5Q48eTdSuHc2HwZXok7bA0/edit

## 🤝 Kontribusi

Kontribusi selalu diterima! Jika Anda ingin berkontribusi pada proyek ini:

1. Fork repositori
2. Buat branch fitur baru (`git checkout -b feature/amazing-feature`)
3. Commit perubahan Anda (`git commit -m 'Add some amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buka Pull Request

## 📝 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file LICENSE untuk detail lebih lanjut.

## 📞 Kontak

Nama Anda - [jhodywiraputra@gmail.com](mailto:jhodywiraputra@gmail.com)

Project Link: https://github.com/habstrakT808/ETL---Fashion-Studio-Store.git




⭐️ Jika Anda menyukai proyek ini, berikan bintang! ⭐️
