# ZTE MF90 Advanced API Controller

Skrip Python otomatisasi kontrol panel untuk modem Mifi **ZTE MF90** via HTTP API. Memungkinkan eksekusi konfigurasi cepat tanpa perlu membuka Web UI browser.

## 🚀 Fitur Utama
- **Autentikasi Otomatis:** Enkripsi password menggunakan struktur Base64 bawaan pabrik.
- **Setelan Wi-Fi:** Mengubah SSID dan password jaringan secara langsung.
- **Blokir IP/Perangkat:** Memutus akses internet client penyusup menggunakan fitur MAC Address Blacklist.
- **Lock Band:** Mengunci frekuensi jaringan ke spesifik mode (`4G Only`, `3G Only`, `2G`, atau `AUTO`).
- **Kirim SMS:** Mengirim pesan singkat langsung dari nomor SIM card modem.
- **Informasi Jaringan & Kuota:** Menampilkan info live bandwidth, sinyal bar, status IP WAN, serta nama provider telekomunikasi.

## 🛠️ Cara Penggunaan

1. Clone repositori ini:
   ```bash
   git clone https://github.com/vpn-nusantara
   cd ZTE-MF90
   ```
2. Install modul dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Sesuaikan setelan modem serta aksi yang ingin dijalankan di file `config.json` (ubah nilai `false` menjadi `true` pada fitur yang ingin dieksekusi otomatis).
4. Jalankan skrip:
   ```bash
   python zte_mf90_control.py
   ```
