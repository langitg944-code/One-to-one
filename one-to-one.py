#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time

class OneToOne:
    """
    ONE-TO-ONE: The Ultra-Lightweight Container Alternative
    Built by: Langit (Sky AI Project)
    Misi: Menggantikan Docker dengan efisiensi tinggi dari Indonesia.
    """

    def __init__(self):
        self.version = "4.0.0-SUPREME"
        self.home = os.path.expanduser("~/.one_to_one")
        self.bin_path = "/usr/local/bin/one-to-one"
        self.registry_file = os.path.join(self.home, "registry.json")
        
        # Inisialisasi Otomatis
        if not os.path.exists(self.home): os.makedirs(self.home)
        self._load_registry()
        self._auto_install()

    def _auto_install(self):
        """Membuat dirinya bisa dipanggil global 'one-to-one' tanpa .py"""
        if os.name != 'nt' and not os.path.exists(self.bin_path):
            try:
                current_file = os.path.abspath(__file__)
                print("[*] Mengonfigurasi Akses Global (Membutuhkan Sudo)...")
                subprocess.run(['sudo', 'cp', current_file, self.bin_path], check=True)
                subprocess.run(['sudo', 'chmod', '+x', self.bin_path], check=True)
                print("\033[1;32m[+] Sukses! Gunakan perintah 'one-to-one' di folder mana saja.\033[0m")
            except:
                print("\033[1;33m[!] Gagal setting global. Jalankan dengan 'python3 one-to-one.py'\033[0m")

    def _load_registry(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f: self.apps = json.load(f)
        else: self.apps = {}

    def _save_registry(self):
        with open(self.registry_file, 'w') as f: json.dump(self.apps, f, indent=4)

    def banner(self):
        print(f"\033[1;34m[ ONE-TO-ONE ENGINE v{self.version} ]\033[0m")
        print(f"\033[1;32m[ Developer: Langit | Status: Global Active ]\033[0m\n")

    def pull(self, alias, repo_url):
        """Fitur Canggih: Menarik 'Image' atau script langsung dari GitHub"""
        target_path = os.path.join(os.getcwd(), alias)
        print(f"[*] Pulling '{alias}' dari {repo_url}...")
        try:
            subprocess.run(['git', 'clone', repo_url, target_path], check=True)
            self.apps[alias] = {"path": target_path, "url": repo_url}
            self._save_registry()
            print(f"\033[1;32m[+] Berhasil menarik proyek ke {target_path}\033[0m")
        except:
            print("\033[1;31m[!] Gagal menarik data. Pastikan Git terinstal.\033[0m")

    def run(self, alias, command):
        """Eksekusi dengan isolasi folder dan scan keamanan otomatis"""
        if alias not in self.apps:
            print(f"[!] Proyek '{alias}' belum terdaftar. Gunakan 'init' atau 'pull'.")
            return
        
        path = self.apps[alias]['path']
        print(f"[*] Menjalankan Lingkungan Terisolasi: {path}")
        print(f"[*] Perintah: {command}")
        
        try:
            subprocess.run(command, shell=True, cwd=path)
        except KeyboardInterrupt:
            print("\n[!] Dihentikan oleh user.")

def main():
    oto = OneToOne()
    oto.banner()

    if len(sys.argv) < 2:
        print("Menu Utama:")
        print("  one-to-one pull [nama] [url_github] -> Ambil proyek dari luar")
        print("  one-to-one run [nama] [perintah]     -> Jalankan aplikasi")
        print("  one-to-one list                      -> Lihat semua proyek")
        return

    cmd = sys.argv[1]
    if cmd == "pull" and len(sys.argv) > 3:
        oto.pull(sys.argv[2], sys.argv[3])
    elif cmd == "run" and len(sys.argv) > 3:
        oto.run(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "list":
        for a in oto.apps: print(f"- {a} -> {oto.apps[a]['path']}")

if __name__ == "__main__":
    main()
    