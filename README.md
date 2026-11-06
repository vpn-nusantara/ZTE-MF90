# ZTE MF90 Modem Manager (CLI)

Script Python berbasis Command Line Interface (CLI) untuk mengelola pengaturan dan melihat informasi pada modem **ZTE MF90** melalui koneksi lokal WebUI.

## ✨ Fitur
*   **Pengaturan WiFi:** Mengubah SSID (Nama WiFi) dan Password.
*   **Lock Band:** Mengunci mode jaringan ke *Auto*, *4G LTE Only*, atau *3G WCDMA Only*.
*   **Kotak Masuk SMS:** Membaca pesan masuk terbaru langsung dari modem.
*   **Informasi Jaringan:** Memantau tipe sinyal, provider, kekuatan sinyal (RSSI/RSRP), dan IP WAN.
*   **Informasi Baterai:** Mengecek persentase baterai serta status pengisian daya (*charging/discharging*).
*   **Block IP / MAC:** Melihat daftar perangkat aktif dan memblokir perangkat asing via MAC Address Filter.

## 🛠️ Prasyarat
*   Python 3.x telah terinstal di komputer.
*   Komputer terhubung ke jaringan modem ZTE MF90 (via WiFi atau kabel USB).
*   IP default modem berada di **`192.168.0.1`**.

## 🚀 Cara Penggunaan

1.  **Clone Repositori ini:**
    ```bash
    git clone https://github.com/vpn-nusantara/ZTE-MF90.git
    cd ZTE-MF90
    ```

2.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Script:**
    ```bash
    python zte_mf90_manager.py
    ```

## ⚙️ Konfigurasi Kustom
Jika password WebUI modem Anda bukan default (`admin`), buka file `zte_mf90_manager.py` dan ubah variabel berikut pada baris teratas:
```python
PASSWORD = "password_baru_anda"
```

## 📝 Catatan Kontribusi
Kontribusi, perbaikan *bug*, atau penambahan fitur baru sangat dipersilakan. Silakan buka *Issue* atau kirimkan *Pull Request*.
