import requests
import json
import sys

# Sesuaikan IP jika gateway modem Anda berbeda (misal: 192.168.0.1)
BASE_URL = "http://192.168.0.1"
HEADERS = {
    "Referer": f"{BASE_URL}/index.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

def check_login():
    url = f"{BASE_URL}/goform/goform_get_cmd_process?cmd=is_login&multi_cmd=1"
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        return res.json().get("is_login") == "1"
    except Exception:
        return False

def login(password="admin"):
    if check_login():
        return True
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    payload = {"goformId": "LOGIN", "password": password}
    try:
        res = requests.post(url, data=payload, headers=HEADERS, timeout=5)
        return res.json().get("result") == "0"
    except Exception:
        return False

# 1. Informasi Perangkat
def get_device_info():
    cmd = "modem_main_state,pin_status,wa_inner_version,hardware_version,imei,signalbar,network_type,network_provider"
    url = f"{BASE_URL}/goform/goform_get_cmd_process?cmd={cmd}&multi_cmd=1"
    try:
        data = requests.get(url, headers=HEADERS, timeout=5).json()
        print("\n[+] INFORMASI PERANGKAT")
        print(f"    Provider     : {data.get('network_provider', 'N/A')}")
        print(f"    Tipe Jaringan: {data.get('network_type', 'N/A')}")
        print(f"    Sinyal       : {data.get('signalbar', '0')}/5")
        print(f"    IMEI         : {data.get('imei', 'N/A')}")
        print(f"    Versi FW     : {data.get('wa_inner_version', 'N/A')}")
    except Exception as e:
        print(f"[-] Gagal mengambil data: {e}")

# 2. Pengaturan Wi-Fi (SSID & Password)
def set_wifi_settings():
    print("\n[+] PENGATURAN WI-FI")
    ssid = input("    Masukkan Nama Wi-Fi (SSID) Baru: ")
    pwd = input("    Masukkan Password Baru (Min. 8 Karakter): ")
    if len(pwd) < 8:
        print("[-] Password kurang dari 8 karakter!")
        return
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    payload = {
        "goformId": "SET_WIFI_INFO",
        "wlan_ssid": ssid,
        "wpa_shared_key": pwd,
        "security_mode": "WPAPSKWPA2PSK",
        "wpapsk_crypto_type": "TKIPAES"
    }
    try:
        res = requests.post(url, data=payload, headers=HEADERS, timeout=5).json()
        if res.get("result") in ["success", "0"]:
            print("[+] Wi-Fi Berhasil Diubah! Perangkat Wi-Fi akan memuat ulang.")
        else:
            print("[-] Gagal mengubah konfigurasi.")
    except Exception as e:
        print(f"[-] Terjadi kesalahan: {e}")

# 3. Kunci Jaringan (4G/3G/Auto)
def set_network_mode():
    print("\n[+] KUNCI JARINGAN\n    1. Auto\n    2. 3G Only\n    3. 4G Only")
    pilihan = input("    Pilih mode (1-3): ")
    mode_map = {"1": "Auto", "2": "UMTS_ONLY", "3": "LTE_ONLY"}
    mode = mode_map.get(pilihan)
    if not mode:
        print("[-] Pilihan tidak valid.")
        return
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    payload = {"goformId": "SET_BEARER_PREFERENCE", "BearerPreference": mode}
    try:
        res = requests.post(url, data=payload, headers=HEADERS, timeout=5).json()
        print(f"[+] Jaringan berhasil diubah ke {mode}." if res.get("result") in ["success", "0"] else "[-] Gagal mengubah jaringan.")
    except Exception as e:
        print(f"[-] Terjadi kesalahan: {e}")

# 4. Status Baterai & Daya
def get_battery_status():
    url = f"{BASE_URL}/goform/goform_get_cmd_process?cmd=battery_value,battery_pers,battery_status&multi_cmd=1"
    try:
        data = requests.get(url, headers=HEADERS, timeout=5).json()
        status_map = {"0": "Tidak Mengisi Daya", "1": "Mengisi Daya (Charging)", "2": "Penuh"}
        st = data.get("battery_status", "0")
        print("\n[+] STATUS BATERAI")
        print(f"    Kapasitas: {data.get('battery_pers', '0')}%")
        print(f"    Status   : {status_map.get(st, 'Unknown')}")
    except Exception as e:
        print(f"[-] Gagal mengecek baterai: {e}")

# 5. Cek Pengguna Terkoneksi (Klien Wi-Fi)
def get_connected_users():
    url = f"{BASE_URL}/goform/goform_get_cmd_process?cmd=station_list&multi_cmd=1"
    try:
        data = requests.get(url, headers=HEADERS, timeout=5).json()
        stations = data.get("station_list", [])
        print("\n[+] PENGGUNA TERKONEKSI")
        if not stations:
            print("    Tidak ada perangkat terhubung atau fitur tidak merespon.")
            return
        for idx, user in enumerate(stations, 1):
            print(f"    {idx}. Nama: {user.get('hostname', 'Unknown')} | MAC: {user.get('mac_addr')} | IP: {user.get('ip_addr')}")
    except Exception as e:
        print(f"[-] Gagal mengecek pengguna: {e}")

# 6. Kirim SMS
def send_sms():
    print("\n[+] KIRIM SMS")
    number = input("    Masukkan Nomor Tujuan: ")
    msg = input("    Masukkan Isi Pesan: ")
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    payload = {
        "goformId": "SEND_SMS",
        "Number": number,
        "Message": msg,
        "sms_time": "00,00,00,00,00,00"
    }
    try:
        res = requests.post(url, data=payload, headers=HEADERS, timeout=5).json()
        print("[+] SMS Berhasil Dikirim!" if res.get("result") in ["success", "0"] else "[-] Gagal mengirim SMS.")
    except Exception as e:
        print(f"[-] Terjadi kesalahan SMS: {e}")

# 7. Cek SMS Masuk (Inbox)
def read_sms_inbox():
    url = f"{BASE_URL}/goform/goform_get_cmd_process?cmd=sms_data_tbl&page=0&smsCount=5&sortType=DESC&tag=1"
    try:
        data = requests.get(url, headers=HEADERS, timeout=5).json()
        messages = data.get("messages", [])
        print("\n[+] KOTAK MASUK SMS (5 Terakhir)")
        if not messages:
            print("    Kotak masuk kosong.")
            return
        for sms in messages:
            print(f"    Dari : {sms.get('number')}\n    Tgl  : {sms.get('date')}\n    Isi  : {sms.get('content')}\n    ---")
    except Exception as e:
        print(f"[-] Gagal membaca SMS: {e}")

# 8. Statistik Penggunaan Data
def get_data_statistics():
    url = f"{BASE_URL}/goform/goform_get_cmd_process?cmd=data_volume_stats&multi_cmd=1"
    try:
        data = requests.get(url, headers=HEADERS, timeout=5).json()
        rx = int(data.get("rx_volume", 0)) / (1024 * 1024)
        tx = int(data.get("tx_volume", 0)) / (1024 * 1024)
        print("\n[+] STATISTIK PENGGUNAAN DATA")
        print(f"    Download: {rx:.2f} MB")
        print(f"    Upload  : {tx:.2f} MB")
        print(f"    Total   : {(rx+tx):.2f} MB")
    except Exception as e:
        print(f"[-] Gagal memuat statistik data: {e}")

# 9. Restart Modem
def reboot_modem():
    if input("\n[!] Yakin ingin merestart modem? (y/n): ").lower() != 'y': return
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    try:
        requests.post(url, data={"goformId": "REBOOT"}, headers=HEADERS, timeout=3)
        print("[+] Perintah dikirim. Perangkat sedang melakukan reboot...")
        sys.exit(0)
    except Exception:
        sys.exit(0)

# 10. Matikan Modem (Shutdown)
def power_off_modem():
    if input("\n[!] Yakin ingin mematikan modem? (y/n): ").lower() != 'y': return
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    try:
        requests.post(url, data={"goformId": "POWER_OFF"}, headers=HEADERS, timeout=3)
        print("[+] Perintah dikirim. Perangkat dimatikan.")
        sys.exit(0)
    except Exception:
        sys.exit(0)

def main():
    print("[*] Menghubungkan ke modem ZTE MF90...")
    pwd = input("Masukkan password WebUI (default: admin): ")
    if not login(pwd):
        print("[-] Login gagal! Periksa kembali kecocokan password atau koneksi Wi-Fi Anda.")
        return

    while True:
        print("\n" + "="*35 + "\n      ZTE MF90 AUTOMATION TOOL\n" + "="*35)
        menus = [
            "Cek Informasi Perangkat", "Atur Nama & Password Wi-Fi", 
            "Kunci Jaringan (4G/3G/Auto)", "Cek Status Baterai",
            "Lihat Perangkat Terhubung", "Kirim SMS Baru",
            "Baca SMS Masuk (Inbox)", "Cek Statistik Data Klien",
            "Restart (Reboot) Modem", "Matikan Perangkat (Power Off)", "Keluar"
        ]
        for idx, m in enumerate(menus, 1):
            print(f"{idx:2d}. {m}")
        print("="*35)
        
        pilih = input("Pilih Menu (1-11): ")
        if pilih == "1": get_device_info()
        elif pilih == "2": set_wifi_settings()
        elif pilih == "3": set_network_mode()
        elif pilih == "4": get_battery_status()
        elif pilih == "5": get_connected_users()
        elif pilih == "6": send_sms()
        elif pilih == "7": read_sms_inbox()
        elif pilih == "8": get_data_statistics()
        elif pilih == "9": reboot_modem()
        elif pilih == "10": power_off_modem()
        elif pilih == "11": 
            print("[+] Keluar sistem. Terima kasih."); break
        else: 
            print("[-] Pilihan tidak valid.")

if __name__ == "__main__":
    main()
