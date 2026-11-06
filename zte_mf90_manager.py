import time
import requests

# Konfigurasi Modem ZTE MF90
BASE_URL = "http://192.168.0.1" 
PASSWORD = "femas123"  # Password default WebUI

session = requests.Session()

def login():
    """Melakukan login ke modem untuk mendapatkan session token."""
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    headers = {"Referer": f"{BASE_URL}/index.html"}
    data = {
        "isStringCmd": "false",
        "goformId": "LOGIN",
        "password": PASSWORD
    }
    try:
        response = session.post(url, data=data, headers=headers)
        res_json = response.json()
        if res_json.get("result") == "0":
            return True
        elif res_json.get("result") == "1":
            print("❌ Login gagal: Password salah.")
        else:
            print("❌ Gagal login: Sesi sibuk atau ditolak.")
    except Exception as e:
        print(f"❌ Tidak dapat terhubung ke modem di {BASE_URL}: {e}")
    return False

def get_data(cmd_list):
    """Fungsi helper untuk mengambil informasi dari API modem."""
    url = f"{BASE_URL}/goform/goform_get_cmd_process"
    params = {
        "isStringCmd": "false",
        "cmd": ",".join(cmd_list),
        "_": int(time.time() * 1000)
    }
    headers = {"Referer": f"{BASE_URL}/index.html"}
    try:
        res = session.get(url, params=params, headers=headers)
        return res.json()
    except:
        return {}

def set_data(data_dict):
    """Fungsi helper untuk mengirim konfigurasi ke modem."""
    url = f"{BASE_URL}/goform/goform_set_cmd_process"
    headers = {"Referer": f"{BASE_URL}/index.html"}
    data_dict["isStringCmd"] = "false"
    try:
        res = session.post(url, data=data_dict, headers=headers)
        if res.json().get("result") == "success":
            print("✅ Pengaturan berhasil diterapkan!")
        else:
            print("❌ Modem menolak pengaturan.")
    except Exception as e:
        print(f"❌ Gagal mengirim perintah: {e}")

# ================= MENU UTAMA =================

def menu_wifi():
    print("\n--- Pengaturan WiFi ---")
    data = get_data(["ssid", "cr_wlan_wpa_psk"])
    print(f"SSID Aktif Saat Ini : {data.get('ssid', 'Tidak diketahui')}")
    
    new_ssid = input("Masukkan SSID (Nama WiFi) baru [Kosongkan jika tidak diubah]: ")
    new_pass = input("Masukkan Password WiFi baru (min 8 karakter) [Kosongkan jika tidak diubah]: ")
    
    payload = {"goformId": "SET_WLAN_WPA"}
    if new_ssid: payload["ssid"] = new_ssid
    if new_pass: payload["cr_wlan_wpa_psk"] = new_pass
    
    if len(payload) > 1:
        set_data(payload)
    else:
        print("Tidak ada perubahan.")

def menu_lock_band():
    print("\n--- Lock Band / Jaringan ---")
    print("1. Auto (Semua Jaringan)")
    print("2. Hanya 4G (LTE Only)")
    print("3. Hanya 3G (WCDMA Only)")
    pilihan = input("Pilih mode jaringan (1/2/3): ")
    
    modes = {"1": "NETWORK_auto", "2": "LTE_ONLY", "3": "WCDMA_ONLY"}
    if pilihan in modes:
        set_data({"goformId": "SET_BEARER_PREFERENCE", "BearerPreference": modes[pilihan]})
    else:
        print("Pilihan tidak valid.")

def menu_pesan():
    print("\n--- Kotak Masuk SMS ---")
    data = get_data(["sms_data_tbl"])
    sms_list = data.get("sms_data_tbl", [])
    
    if not sms_list:
        print("Tidak ada pesan masuk.")
        return
        
    for idx, sms in enumerate(sms_list[:5], 1):
        print(f"\n[{idx}] Dari: {sms.get('number')} | Tanggal: {sms.get('date')}")
        print(f"Isi: {sms.get('content')}")

def menu_info_jaringan():
    print("\n--- Informasi Jaringan ---")
    fields = ["network_type", "network_provider", "rssi", "rscp", "lte_rsrp", "wan_ipaddr"]
    data = get_data(fields)
    
    print(f"Provider     : {data.get('network_provider', '-')}")
    print(f"Tipe Sinyal  : {data.get('network_type', '-')}")
    print(f"RSSI         : {data.get('rssi', '-')} dBm")
    print(f"RSRP (4G)    : {data.get('lte_rsrp', '-')} dBm")
    print(f"IP WAN       : {data.get('wan_ipaddr', '-')}")

def menu_info_baterai():
    print("\n--- Informasi Baterai ---")
    data = get_data(["battery_value", "battery_status"])
    status = "Mengisi Daya (Charging)" if data.get("battery_status") == "1" else "Menggunakan Baterai"
    print(f"Persentase Baterai : {data.get('battery_value', '0')}%")
    print(f"Status             : {status}")

def menu_block_ip():
    print("\n--- Block IP / MAC Address ---")
    print("1. Lihat Daftar Perangkat Aktif")
    print("2. Blokir MAC Perangkat")
    pilihan = input("Pilih menu (1/2): ")
    
    if pilihan == "1":
        data = get_data(["station_list"])
        stations = data.get("station_list", [])
        if not stations:
            print("Tidak ada perangkat yang terhubung.")
        for st in stations:
            print(f"Nama: {st.get('hostname')} | IP: {st.get('ip_addr')} | MAC: {st.get('mac_addr')}")
            
    elif pilihan == "2":
        mac_to_block = input("Masukkan MAC Address yang ingin diblokir (Format: AA:BB:CC:DD:EE:FF): ")
        if mac_to_block:
            set_data({
                "goformId": "SET_MAC_FILTER_INFO",
                "macFilterMode": "BlackList", 
                "macaddr": mac_to_block
            })

def main():
    print(f"Mencoba terhubung ke Modem ZTE MF90 di {BASE_URL}...")
    if not login():
        return
        
    print("✅ Berhasil masuk ke sistem modem.")
    
    while True:
        print("\n==============================")
        print("   ZTE MF90 MANAGER SCRIPT    ")
        print("==============================")
        print("1. Pengaturan WiFi")
        print("2. Lock Band (Frekuensi/Jaringan)")
        print("3. Cek Pesan Masuk (SMS)")
        print("4. Informasi Jaringan")
        print("5. Informasi Baterai")
        print("6. Block IP / Perangkat")
        print("7. Keluar")
        
        pilihan = input("Pilih menu [1-7]: ")
        
        if pilihan == "1": menu_wifi()
        elif pilihan == "2": menu_lock_band()
        elif pilihan == "3": menu_pesan()
        elif pilihan == "4": menu_info_jaringan()
        elif pilihan == "5": menu_info_baterai()
        elif pilihan == "6": menu_block_ip()
        elif pilihan == "7": 
            print("Keluar dari script. Sampai jumpa!")
            break
        else:
            print("Pilihan salah, silakan coba lagi.")

if __name__ == "__main__":
    main()
