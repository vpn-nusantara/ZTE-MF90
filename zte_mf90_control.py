import requests
import json
import base64
import time
import sys

class ZTE_MF90_Controller:
    def __init__(self, base_url="http://192.168.0.1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Referer": f"{self.base_url}/index.html",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        })

    def login(self, password):
        """Melakukan login ke Web UI ZTE MF90 menggunakan password Base64."""
        url = f"{self.base_url}/goform/goform_set_cmd_process"
        password_b64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        
        payload = {
            "isFormSubmit": "true",
            "goformId": "LOGIN",
            "password": password_b64
        }
        
        try:
            response = self.session.post(url, data=payload, timeout=5)
            result = response.json()
            if result.get("result") in ["0", "4"]:
                print("[+] Login Berhasil!")
                return True
            else:
                print(f"[-] Login Gagal. Response: {result}")
                return False
        except Exception as e:
            print(f"[-] Error saat koneksi login: {e}")
            return False

    def set_wifi(self, ssid, password):
        """Mengubah SSID (Nama Wi-Fi) dan Password."""
        url = f"{self.base_url}/goform/goform_set_cmd_process"
        payload = {
            "isFormSubmit": "true",
            "goformId": "SET_WLAN_WPA",
            "wlan_ssid": ssid,
            "wpa_mode": "wpa_wpa2_psk",
            "wpa_psk_key": password
        }
        response = self.session.post(url, data=payload)
        if response.status_code == 200:
            print(f"[+] Wi-Fi sukses diubah ke -> SSID: {ssid}")
        else:
            print("[-] Gagal memperbarui setelan Wi-Fi.")

    def block_device_mac(self, mac_address, device_name="Blocked_Device"):
        """Memblokir perangkat tertentu via kebijakan MAC Address Filter Blacklist."""
        url = f"{self.base_url}/goform/goform_set_cmd_process"
        payload = {
            "isFormSubmit": "true",
            "goformId": "ADD_MAC_FILTER_ENTRY",
            "mac_filter_interface": "wlan0",
            "mac_filter_policy": "black_list",
            "mac_filter_mac": mac_address,
            "mac_filter_device_name": device_name
        }
        response = self.session.post(url, data=payload)
        if response.status_code == 200:
            print(f"[+] Sukses memblokir MAC Address: {mac_address}")
        else:
            print("[-] Gagal mengeksekusi pemblokiran MAC.")

    def lock_band(self, mode):
        """Mengunci preferensi jaringan (AUTO, 2G, 3G, atau 4G)."""
        url = f"{self.base_url}/goform/goform_set_cmd_process"
        mapping = {"AUTO": "0", "2G": "1", "3G": "2", "4G": "3"}
        
        if mode not in mapping:
            print("[-] Mode tidak valid! Gunakan: AUTO, 2G, 3G, atau 4G.")
            return

        payload = {
            "isFormSubmit": "true",
            "goformId": "SET_BEARER_PREFERENCE",
            "BearerPreference": mapping[mode]
        }
        response = self.session.post(url, data=payload)
        if response.status_code == 200:
            print(f"[+] Jaringan berhasil dikunci (Lock Band) ke: {mode}")
        else:
            print("[-] Gagal melakukan Lock Band.")

    def send_sms(self, phone_number, message):
        """Mengirim pesan SMS dari nomor SIM di dalam modem menggunakan encoding Unicode Hex."""
        url = f"{self.base_url}/goform/goform_set_cmd_process"
        message_hex = message.encode('utf-16be').hex().upper()
        current_time = time.strftime("%y;%m;%d;%H;%M;%S;+7", time.localtime())

        payload = {
            "isFormSubmit": "true",
            "goformId": "SEND_SMS",
            "notCallback": "true",
            "Number": phone_number,
            "sms_time": current_time,
            "MessageBody": message_hex,
            "encode_type": "UNICODE",
            "ID": "-1"
        }
        response = self.session.post(url, data=payload)
        if response.status_code == 200 and response.json().get("result") == "success":
            print(f"[+] SMS berhasil dikirim ke {phone_number}!")
        else:
            print(f"[-] Gagal mengirim SMS: {response.text}")

    def display_data_usage(self):
        """Mengambil dan menampilkan statistik kuota data sesi aktif."""
        url = f"{self.base_url}/goform/goform_get_cmd_process?cmd=realtime_time,realtime_tx_bytes,realtime_rx_bytes"
        try:
            res = self.session.get(url).json()
            rx = round(int(res.get("realtime_rx_bytes", 0)) / (1024**2), 2)
            tx = round(int(res.get("realtime_tx_bytes", 0)) / (1024**2), 2)
            print("\n=== PENGGUNAAN DATA ===")
            print(f"Durasi Sesi: {res.get('realtime_time')} detik")
            print(f"Download   : {rx} MB")
            print(f"Upload     : {tx} MB")
            print(f"Total Sesi : {round(rx + tx, 2)} MB\n=======================")
        except Exception as e:
            print(f"[-] Gagal memuat data statistik: {e}")

    def display_network_info(self):
        """Mengambil info sinyal, nama operator, dan IP WAN publik."""
        url = f"{self.base_url}/goform/goform_get_cmd_process?cmd=network_type,network_provider,signalbar,wan_ipaddr,ppp_status"
        try:
            res = self.session.get(url).json()
            net_map = {"0": "No Service", "1": "2G", "2": "EDGE", "3": "3G", "8": "4G LTE"}
            net_code = res.get("network_type", "0")
            
            print("\n=== INFORMASI JARINGAN ===")
            print(f"Operator    : {res.get('network_provider', 'Unknown')}")
            print(f"Tipe Sinyal : {net_map.get(net_code, f'Code {net_code}')}")
            print(f"Sinyal Bar  : {res.get('signalbar', '0')}/5")
            print(f"IP WAN      : {res.get('wan_ipaddr', '0.0.0.0')}")
            print(f"Status PPP  : {res.get('ppp_status', 'Disconnected')}\n==========================")
        except Exception as e:
            print(f"[-] Gagal memuat info jaringan: {e}")

if __name__ == "__main__":
    # Memuat file konfigurasi eksternal
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("[-] File config.json tidak ditemukan! Silakan buat berkas konfigurasi terlebih dahulu.")
        sys.exit(1)

    modem = ZTE_MF90_Controller(base_url=config.get("modem_ip", "http://192.168.0.1"))
    
    if modem.login(config.get("password", "admin")):
        # Panggil fungsi monitoring bawaan skrip secara langsung
        modem.display_network_info()
        modem.display_data_usage()
        
        # Eksekusi Otomatisasi Fitur berdasarkan isi config.json jika diaktifkan
        actions = config.get("actions", {})
        
        if actions.get("change_wifi", False):
            modem.set_wifi(actions["wifi_ssid"], actions["wifi_password"])
            
        if actions.get("block_mac", False):
            modem.block_device_mac(actions["mac_to_block"], actions["mac_device_name"])
            
        if actions.get("lock_band", False):
            modem.lock_band(actions["band_mode"])
            
        if actions.get("send_sms", False):
            modem.send_sms(actions["sms_target"], actions["sms_message"])
