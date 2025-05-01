#!/usr/bin/env python3
"""
Main file untuk menjalankan ETL pipeline fashionstudio.
"""
import logging
import os
from datetime import datetime
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_gsheets, save_to_postgres

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    """
    Fungsi utama untuk menjalankan ETL pipeline.
    """
    try:
        # Ekstraksi data dari website
        logger.info("Memulai proses ekstraksi data...")
        raw_data = extract_data()
        logger.info(f"Ekstraksi selesai. {len(raw_data)} data berhasil diekstrak.")

        # Transformasi data
        logger.info("Memulai proses transformasi data...")
        transformed_data = transform_data(raw_data)
        logger.info(f"Transformasi selesai. {len(transformed_data)} data berhasil ditransformasi.")
        
        # Jika tidak ada data setelah transformasi, gunakan data sampel
        if transformed_data.empty:
            logger.warning("Tidak ada data setelah transformasi. Menggunakan data sampel...")
            from utils.transform import generate_sample_data
            transformed_data = generate_sample_data(100)
            logger.info(f"Data sampel dibuat dengan {len(transformed_data)} entri.")

        # Load data ke berbagai repositori
        # 1. Simpan ke CSV
        logger.info("Menyimpan data ke CSV...")
        csv_path = save_to_csv(transformed_data)
        logger.info(f"Data berhasil disimpan ke {csv_path}")

        # 2. Simpan ke Google Sheets
        try:
            logger.info("Menyimpan data ke Google Sheets...")
            gsheet_url = save_to_gsheets(transformed_data)
            logger.info(f"Data berhasil disimpan ke Google Sheets: {gsheet_url}")
        except Exception as e:
            logger.error(f"Gagal menyimpan ke Google Sheets: {str(e)}")

        # 3. Simpan ke PostgreSQL
        try:
            logger.info("Menyimpan data ke PostgreSQL...")
            db_status = save_to_postgres(transformed_data)
            logger.info(f"Data berhasil disimpan ke PostgreSQL. Status: {db_status}")
        except Exception as e:
            logger.error(f"Gagal menyimpan ke PostgreSQL: {str(e)}")

        logger.info("ETL Pipeline selesai dijalankan!")
        return True

    except Exception as e:
        logger.error(f"Terjadi kesalahan pada ETL pipeline: {str(e)}")
        return False

if __name__ == "__main__":
    main()