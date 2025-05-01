#!/usr/bin/env python3
"""
Module untuk melakukan ekstraksi data dari website fashion studio.
"""
import logging
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Konfigurasi logging
logger = logging.getLogger(__name__)

# URL Target
BASE_URL = "https://fashion-studio.dicoding.dev"
MAX_RETRIES = 3
RETRY_DELAY = 2

def scrape_page(page_number):
    """
    Melakukan scraping pada satu halaman website.
    
    Args:
        page_number (int): Nomor halaman yang akan di-scrape
        
    Returns:
        list: Daftar produk yang berhasil di-scrape dari halaman tersebut
    
    Raises:
        Exception: Jika terjadi kesalahan saat melakukan request atau parsing
    """
    # URL yang diubah
    if page_number == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}/page{page_number}"
    
    products = []
    
    # Implementasi retry untuk mengatasi kendala jaringan
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Mengambil data dari halaman {page_number}...")
            
            # Tambahkan header user-agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Selector baru untuk produk
            product_items = soup.select('.collection-card')
            
            # Debug info
            print(f"Jumlah produk ditemukan: {len(product_items)}")
            
            # Timestamp sebagai penanda waktu scraping
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for item in product_items:
                try:
                    # Ekstrak data sesuai ketentuan
                    product = {}
                    
                    # Ekstrak detail produk dari dalam collection-card
                    details = item.select_one('.product-details')
                    
                    # Ekstrak judul produk
                    title_element = item.select_one('.collection-title') or details.select_one('h3') if details else None
                    product['Title'] = title_element.text.strip() if title_element else "Unknown Product"
                    
                    # Ekstrak harga produk
                    price_element = item.select_one('.collection-price') or details.select_one('.price') if details else None
                    if price_element:
                        price_text = price_element.text.strip()
                        product['Price'] = price_text
                    else:
                        product['Price'] = "Price Unavailable"
                    
                    # Ekstrak rating produk
                    rating_element = item.select_one('.collection-rating') or details.select_one('.rating') if details else None
                    if rating_element:
                        rating_text = rating_element.text.strip()
                        product['Rating'] = rating_text
                    else:
                        product['Rating'] = "Invalid Rating"
                    
                    # Ekstrak warna produk
                    colors_element = item.select_one('.collection-colors') or details.select_one('.colors') if details else None
                    if colors_element:
                        colors_text = colors_element.text.strip()
                        product['Colors'] = colors_text
                    else:
                        product['Colors'] = "Colors Unavailable"
                    
                    # Ekstrak ukuran produk
                    size_element = item.select_one('.collection-size') or details.select_one('.size') if details else None
                    if size_element:
                        size_text = size_element.text.strip()
                        product['Size'] = size_text
                    else:
                        product['Size'] = "Size Unavailable"
                    
                    # Ekstrak gender produk
                    gender_element = item.select_one('.collection-gender') or details.select_one('.gender') if details else None
                    if gender_element:
                        gender_text = gender_element.text.strip()
                        product['Gender'] = gender_text
                    else:
                        product['Gender'] = "Gender Unavailable"
                    
                    # Tambahkan timestamp
                    product['timestamp'] = current_timestamp
                    
                    products.append(product)
                    
                except Exception as e:
                    logger.warning(f"Gagal mengekstrak produk: {str(e)}")
                    continue
                
            logger.info(f"Berhasil mengambil {len(products)} produk dari halaman {page_number}")
            return products
            
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"Percobaan {attempt+1} gagal: {str(e)}. Mencoba kembali dalam {RETRY_DELAY} detik...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Gagal mengambil data setelah {MAX_RETRIES} percobaan: {str(e)}")
                raise Exception(f"Gagal mengakses halaman {page_number}: {str(e)}")
                
    return products

def extract_data(start_page=1, end_page=50):
    """
    Mengekstrak data dari rentang halaman website.
    
    Args:
        start_page (int): Halaman awal untuk ekstraksi
        end_page (int): Halaman akhir untuk ekstraksi
        
    Returns:
        DataFrame: Data hasil ekstraksi dalam format pandas DataFrame
    """
    if start_page < 1:
        logger.warning("Halaman awal minimal adalah 1. Menggunakan halaman awal = 1")
        start_page = 1
        
    if end_page < start_page:
        logger.warning(f"Halaman akhir tidak boleh kurang dari halaman awal. Menggunakan halaman akhir = {start_page}")
        end_page = start_page
    
    all_products = []
    
    try:
        for page in range(start_page, end_page + 1):
            try:
                page_products = scrape_page(page)
                all_products.extend(page_products)
                
                # Delay kecil untuk menghindari rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Gagal mengambil data dari halaman {page}: {str(e)}")
                continue
        
        # Konversi ke DataFrame
        df = pd.DataFrame(all_products)
        logger.info(f"Total data yang berhasil diekstrak: {len(df)}")
        
        # Debug: Cetak sampel data
        if not df.empty:
            logger.info(f"Sampel data yang diekstrak:\n{df.head().to_string()}")
            
            # Cetak nilai unik untuk setiap kolom
            for col in df.columns:
                unique_values = df[col].unique()
                if len(unique_values) < 10:  # Hanya cetak jika jumlah nilai unik sedikit
                    logger.info(f"Nilai unik untuk kolom {col}: {unique_values}")
                else:
                    logger.info(f"Jumlah nilai unik untuk kolom {col}: {len(unique_values)}")
        
        return df
        
    except Exception as e:
        logger.error(f"Terjadi kesalahan pada proses ekstraksi: {str(e)}")
        # Mengembalikan DataFrame kosong daripada gagal sepenuhnya
        return pd.DataFrame()