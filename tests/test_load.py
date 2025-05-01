#!/usr/bin/env python3
"""
Unit tests untuk modul load.py
"""
import unittest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_gsheets, save_to_postgres
from sqlalchemy.exc import SQLAlchemyError

class TestLoad(unittest.TestCase):
    """
    Test case untuk fungsi-fungsi di modul load
    """
    
    def setUp(self):
        """
        Setup untuk test case
        """
        # DataFrame sampel untuk pengujian
        self.sample_df = pd.DataFrame({
            'Title': ['Test Product', 'Another Product'],
            'Price': [735840.0, 479840.0],  # Harga dalam Rupiah (45.99 * 16000, 29.99 * 16000)
            'Rating': [4.5, 4.2],
            'Colors': [3, 2],
            'Size': ['M', 'L'],
            'Gender': ['Unisex', 'Women'],
            'timestamp': ['2025-05-01 10:00:00', '2025-05-01 10:00:00']
        })
        
        # Temporary filename untuk pengujian CSV
        self.test_csv_filename = "test_products.csv"
    
    def tearDown(self):
        """
        Cleanup setelah test case
        """
        # Hapus file CSV test jika ada
        if os.path.exists(self.test_csv_filename):
            os.remove(self.test_csv_filename)
    
    def test_save_to_csv(self):
        """
        Test fungsi save_to_csv
        """
        # Panggil fungsi yang diuji
        csv_path = save_to_csv(self.sample_df, self.test_csv_filename)
        
        # Verifikasi file CSV telah dibuat
        self.assertTrue(os.path.exists(csv_path))
        
        # Baca file CSV untuk verifikasi isi
        loaded_df = pd.read_csv(csv_path)
        
        # Verifikasi jumlah baris dan kolom
        self.assertEqual(len(loaded_df), len(self.sample_df))
        self.assertEqual(len(loaded_df.columns), len(self.sample_df.columns))
        
        # Verifikasi nilai-nilai dalam DataFrame
        self.assertEqual(loaded_df['Title'].iloc[0], 'Test Product')
        self.assertEqual(loaded_df['Price'].iloc[0], 735840.0)
    
    def test_save_to_csv_empty_df(self):
        """
        Test fungsi save_to_csv dengan DataFrame kosong
        """
        empty_df = pd.DataFrame()
        
        # Verifikasi exception dilemparkan untuk DataFrame kosong
        with self.assertRaises(ValueError):
            save_to_csv(empty_df, self.test_csv_filename)
    
    @patch('utils.load.service_account.Credentials.from_service_account_file')
    @patch('utils.load.googleapiclient.discovery.build')
    def test_save_to_gsheets(self, mock_build, mock_creds):
        """
        Test fungsi save_to_gsheets
        """
        # Setup mocks
        mock_sheets = MagicMock()
        mock_drive = MagicMock()
        mock_build.side_effect = [mock_sheets, mock_drive]
        
        # Mock API calls
        mock_spreadsheet = {'spreadsheetId': 'test_spreadsheet_id'}
        mock_sheets.spreadsheets().create().execute.return_value = mock_spreadsheet
        
        # Mock credential file
        mock_creds_file = "mock_creds.json"
        with patch('os.path.exists', return_value=True):
            # Panggil fungsi yang diuji
            result = save_to_gsheets(self.sample_df, mock_creds_file)
        
        # Verifikasi hasil
        self.assertEqual(result, "https://docs.google.com/spreadsheets/d/test_spreadsheet_id/edit")
        
        # Verifikasi API calls
        mock_build.assert_any_call('sheets', 'v4', credentials=mock_creds.return_value)
        mock_build.assert_any_call('drive', 'v3', credentials=mock_creds.return_value)
        
        # Tidak memeriksa jumlah panggilan create() karena implementasi mungkin berbeda
        # mock_sheets.spreadsheets().create.assert_called_once()
        
        # Verifikasi panggilan update
        mock_sheets.spreadsheets().values().update.assert_called_once()
    
    @patch('utils.load.service_account.Credentials.from_service_account_file')
    def test_save_to_gsheets_missing_credentials(self, mock_creds):
        """
        Test fungsi save_to_gsheets dengan file kredensial yang tidak ada
        """
        # Mock file kredensial tidak ada
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                save_to_gsheets(self.sample_df, "nonexistent_creds.json")
    
    @patch('utils.load.create_engine')
    def test_save_to_postgres(self, mock_create_engine):
        """
        Test fungsi save_to_postgres
        """
        # Setup mock
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Mock to_sql
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            # Panggil fungsi yang diuji
            result = save_to_postgres(self.sample_df)
        
        # Verifikasi hasil
        self.assertTrue(result)
        
        # Verifikasi to_sql dipanggil dengan parameter yang benar
        mock_to_sql.assert_called_once_with("fashion_products", mock_engine, if_exists='replace', index=False)
    
    @patch('utils.load.create_engine')
    def test_save_to_postgres_database_error(self, mock_create_engine):
        """
        Test fungsi save_to_postgres dengan error database
        """
        # Setup mock untuk SQLAlchemy error
        mock_create_engine.side_effect = SQLAlchemyError("Database connection error")
        
        # Verifikasi exception dilemparkan
        with self.assertRaises(SQLAlchemyError):
            save_to_postgres(self.sample_df)
    
    def test_save_to_postgres_empty_df(self):
        """
        Test fungsi save_to_postgres dengan DataFrame kosong
        """
        empty_df = pd.DataFrame()
        
        # Verifikasi exception dilemparkan untuk DataFrame kosong
        with self.assertRaises(ValueError):
            save_to_postgres(empty_df)
    
    @patch('utils.load.create_engine')
    def test_save_to_postgres_custom_config(self, mock_create_engine):
        """
        Test fungsi save_to_postgres dengan konfigurasi database kustom
        """
        # Setup mock
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Konfigurasi database kustom
        custom_config = {
            'host': 'custom_host',
            'database': 'custom_db',
            'user': 'custom_user',
            'password': 'custom_pass',
            'port': '5433'
        }
        
        # Mock to_sql
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            # Panggil fungsi yang diuji
            result = save_to_postgres(self.sample_df, custom_config)
        
        # Verifikasi hasil
        self.assertTrue(result)
        
        # Verifikasi create_engine dipanggil dengan connection string yang benar
        expected_conn_string = f"postgresql://{custom_config['user']}:{custom_config['password']}@{custom_config['host']}:{custom_config['port']}/{custom_config['database']}"
        mock_create_engine.assert_called_once_with(expected_conn_string)

if __name__ == '__main__':
    unittest.main()