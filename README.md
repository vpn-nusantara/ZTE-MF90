# ZTE MF90 CLI Manager (10 Menu System)

Script otomatisasi berbasis CLI Python untuk melakukan konfigurasi, pembacaan status, dan manajemen SMS pada modem MIFI **ZTE MF90** tanpa harus membuka browser Web UI.

## 📋 Fitur Unggulan (10 Pilihan Menu)
1. **Informasi Perangkat:** Menampilkan Tipe Sinyal, Provider, IMEI, & Versi Firmware.
2. **Pengaturan Jaringan Wi-Fi:** Mengubah SSID Wifi dan WPA Password secara interaktif.
3. **Kunci Jaringan (Network Lock):** Pilihan mengunci ke `4G LTE Only`, `3G Only`, atau `Auto`.
4. **Status Baterai:** Mengecek kapasitas sisa baterai beserta status pengisian dayanya.
5. **Daftar Klien Terhubung:** Menampilkan daftar nama *hostname*, IP address, dan MAC address perangkat yang terhubung.
6. **Kirim SMS:** Fasilitas mengirimkan SMS keluar langsung dari CLI script.
7. **Kotak Masuk SMS:** Menampilkan 5 pesan masuk terakhir beserta detail nomor pengirim.
8. **Statistik Penggunaan Data:** Mengalkulasi jumlah data *download* dan *upload* yang berjalan.
9. **Reboot Jarak Jauh:** Mengirimkan perintah muat ulang (*restart*) sistem modem.
10. **Matikan Sistem:** Perintah mematikan daya (*Power Off*) Mifi langsung melalui script.

## 🚀 Langkah Instalasi & Menjalankan

1. Pastikan Anda telah menginstal **Python 3.x** di komputer Anda.
2. Unduh atau clone repositori ini:
   ```bash
   git clone https://github.com/vpn-nusantara/ZTE-MF90.git
cd ZTE-MF90
   ```
3. Pasang modul dependensi `requests` menggunakan pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Sambungkan PC/Laptop Anda ke jaringan Wi-Fi modem ZTE MF90.
5. Jalankan program dengan perintah:
   ```bash
   python app.py
   ```

## ⚙️ Catatan Konfigurasi
* Secara default program berasumsi IP gateway modem Anda berada di **`192.168.1.1`**. Jika modem Anda menggunakan custom IP (contoh: `192.168.0.1` atau `192.168.8.1`), Anda hanya perlu membuka file `app.py` lalu ubah baris variabel `BASE_URL` di bagian atas kode.
