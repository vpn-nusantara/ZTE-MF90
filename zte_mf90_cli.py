import requests
import json
import base64
import sys

# Konfigurasi Default Modem ZTE MF90
BASE_URL = "http://192.168.0.1"  # Sesuaikan dengan IP modem Anda jika berbeda
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": f"{BASE_URL}/index.html",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

class ZTEMF90Client:
    def __init__(self):
        self.session = requests.Session()
        self.is_logged_in = False

    def login(self):
        print("\n=== LOGIN MODEM ZTE MF90 ===")
        password = input("Masukkan password webUI: ")
        
        # ZTE menggunakan encoding base64 untuk password pada beberapa firmware
        encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        
        url = f"{BASE_URL}/goform/goform_set_cmd_process"
        payload = {
            "is_com_set": "1",
            "goformId": "LOGIN",
            "password": encoded_password
        }
        
        try:
            response = self.session.post(url, data=payload, headers=HEADERS)
            result = response.json()
            
            if result.get("result") == "0" or result.get("result") == "4":
                self.is_logged_in = True
                print("[+] Login Berhasil!")
            else:
                print("[-] Login Gagal. Periksa password Anda.")
        except Exception as e:
            print(f"[-] Error saat login: {e}")

    def get_cmd(self, cmd_param):
        """Fungsi helper untuk mengambil data dari modem"""
        url = f"{BASE_URL}/goform/goform_get_cmd_process?cmd={cmd_param}&multi_cmd=1"
        try:
            response = self.session.get(url, headers=HEADERS)
            return response.json()
        except Exception as e:
            print(f"[-] Gagal mengambil data ({cmd_param}): {e}")
            return {}

    def set_cmd(self, payload):
        """Fungsi helper untuk mengubah pengaturan pada modem"""
        url = f"{BASE_URL}/goform/goform_set_cmd_process"
        payload["is_com_set"] = "1"
        try:
            response = self.session.post(url, data=payload, headers=HEADERS)
            return response.json()
        except Exception as e:
            print(f"[-] Gagal mengubah pengaturan: {e}")
            return {}

    def show_battery(self):
        print("\n--- INFORMASI BATERAI ---")
        data = self.get_cmd("battery_value,battery_status,battery_pers")
        capacity = data.get("battery_value", "N/A")
        status = data.get("battery_status", "0")
        
        status_map = {"0": "Tidak Mengisi Daya", "1": "Mengisi Daya (Charging)", "2": "Penuh"}
        print(f"Kapasitas Baterai : {capacity}%")
        print(f"Status Baterai    : {status_map.get(status, 'Unknown')}")

    def show_network(self):
        print("\n--- INFORMASI JARINGAN ---")
        data = self.get_cmd("network_type,signalbar,network_provider,rssi,rsrp,wan_ipaddr")
        
        net_type = data.get("network_type", "N/A")
        signal = data.get("signalbar", "0")
        provider = data.get("network_provider", "N/A")
        rssi = data.get("rssi", "N/A")
        ip = data.get("wan_ipaddr", "N/A")

        print(f"Operator     : {provider}")
        print(f"Tipe Jaringan: {net_type}")
        print(f"Sinyal Bar   : {signal}/5")
        print(f"RSSI         : {rssi} dBm")
        print(f"WAN IP Address: {ip}")

    def lock_band(self):
        print("\n--- LOCK BAND / FREKUENSI ---")
        print("1. Auto (Semua Jaringan)")
        print("2. Hanya 4G (LTE Only)")
        print("3. Hanya 3G (WCDMA Only)")
        pilihan = input("Pilih mode jaringan: ")

        mode_map = {"1": "0", "2": "3", "3": "2"} # Kode standar modem ZTE
        if pilihan in mode_map:
            payload = {
                "goformId": "SET_BEARER_PREFERENCE",
                "BearerPreference": mode_map[pilihan]
            }
            res = self.set_cmd(payload)
            if res.get("result") == "success" or res.get("result") == "0":
                print("[+] Mode jaringan berhasil diubah.")
            else:
                print("[-] Gagal mengubah mode jaringan.")
        else:
            print("[-] Pilihan tidak valid.")

    def wifi_settings(self):
        print("\n--- PENGATURAN WIFI ---")
        # Ambil info SSID saat ini
        data = self.get_cmd("ssid,wifi_wpapsk")
        current_ssid = data.get("ssid", "N/A")
        
        print(f"SSID Saat Ini: {current_ssid}")
        new_ssid = input("Masukkan Nama WiFi (SSID) Baru (Kosongkan jika tidak diubah): ")
        new_pass = input("Masukkan Password WiFi Baru (Minimal 8 karakter, Kosongkan jika tidak diubah): ")

        payload = {"goformId": "SET_WLAN_WPA"}
        
        if new_ssid:
            payload["ssid"] = new_ssid
        else:
            payload["ssid"] = current_ssid

        if new_pass:
            if len(new_pass) < 8:
                print("[-] Password minimal harus 8 karakter!")
                return
            payload["wifi_wpapsk"] = new_pass
            
        if new_ssid or new_pass:
            res = self.set_cmd(payload)
            if res.get("result") == "success" or res.get("result") == "0":
                print("[+] Pengaturan WiFi berhasil diperbarui.")
            else:
                print("[-] Gagal memperbarui WiFi.")
        else:
            print("[*] Tidak ada perubahan diterapkan.")

    def block_ip_mac(self):
        print("\n--- BLOCK IP / MAC ADDRESS (Firewall) ---")
        print("1. Lihat Daftar Blokir saat ini")
        print("2. Tambah MAC/IP ke Daftar Blokir")
        aksi = input("Pilih aksi: ")

        if aksi == "1":
            data = self.get_cmd("mac_filter_list")
            print(f"Daftar MAC Terblokir: {data.get('mac_filter_list', 'Kosong')}")
        elif aksi == "2":
            mac_target = input("Masukkan MAC Address yang ingin diblokir (Contoh: AA:BB:CC:DD:EE:FF): ")
            # Mengaktifkan filter MAC
            payload = {
                "goformId": "SET_MAC_FILTER",
                "mac_filter_action": "drop", # 'drop' artinya memblokir MAC terdaftar
                "mac_filter_mac": mac_target
            }
            res = self.set_cmd(payload)
            if res.get("result") == "success" or res.get("result") == "0":
                print(f"[+] Device {mac_target} berhasil diblokir.")
            else:
                print("[-] Gagal menerapkan pemblokiran.")
        else:
            print("[-] Pilihan tidak valid.")

def main():
    client = ZTEMF90Client()
    
    # Jalankan login manual terlebih dahulu
    client.login()
    
    if not client.is_logged_in:
        print("[-] Anda harus login untuk mengakses menu. Keluar.")
        sys.exit()

    while True:
        print("\n===============================️")
        print("    ZTE MF90 UTILITY TOOL      ")
        print("===============================")
        print("1. Cek Informasi Baterai")
        print("2. Cek Informasi Jaringan")
        print("3. Lock Band (2G/3G/4G)")
        print("4. Ubah Pengaturan WiFi")
        print("5. Block IP / MAC Address")
        print("6. Keluar")
        
        pilihan = input("Pilih menu (1-6): ")
        
        if pilihan == "1":
            client.show_battery()
        elif pilihan == "2":
            client.show_network()
        elif pilihan == "3":
            client.lock_band()
        elif pilihan == "4":
            client.wifi_settings()
        elif pilihan == "5":
            client.block_ip_mac()
        elif pilihan == "6":
            print("[*] Terima kasih telah menggunakan tool ini.")
            break
        else:
            print("[-] Pilihan salah, silakan coba lagi.")

if __name__ == "__main__":
    main()
