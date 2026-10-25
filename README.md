# Broker Komisi Web

Aplikasi admin berbasis Streamlit dengan database online Supabase.

## Fitur
- Login admin
- Tambah, cari, dan edit anggota beserta sponsor/upline
- Input transaksi dengan perhitungan komisi otomatis
- Pengaturan persentase per level
- Filter laporan tanggal dan unduh CSV

## Cara kerja komisi
Level 1 adalah sponsor langsung dari anggota sumber hasil; level 2 adalah sponsor di atasnya, dan seterusnya. Tarif awal: level 1 = 6%, level 2 = 3%, level 3 = 2%, level 4 = 1%.

Contoh: jika H direkrut G, G direkrut F, F direkrut E, dan E direkrut D; transaksi atas nama H dengan dasar Rp10.000.000 memberi G Rp600.000, F Rp300.000, E Rp200.000, dan D Rp100.000.

## 1. Siapkan Supabase
1. Buat project di https://supabase.com/.
2. Buka SQL Editor, jalankan seluruh isi `schema.sql`.
3. Dari pengaturan API project, salin Project URL dan service-role/secret key. Key ini rahasia, hanya boleh ada di server.

## 2. Jalankan lokal
Perlu Python 3.10 atau lebih baru. Dari folder proyek:

```bash
python -m venv .venv
```

Aktifkan environment Windows PowerShell:
```powershell
.venv\\Scripts\\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Pasang dependensi:
```bash
pip install -r requirements.txt
```

Windows PowerShell:
```powershell
$env:ADMIN_PASSWORD="PASSWORD_ADMIN_KUAT"
$env:SUPABASE_URL="https://PROJECT_ID.supabase.co"
$env:SUPABASE_SERVICE_ROLE_KEY="SERVICE_ROLE_KEY_RAHASIA"
streamlit run app.py
```

macOS/Linux:
```bash
export ADMIN_PASSWORD="PASSWORD_ADMIN_KUAT"
export SUPABASE_URL="https://PROJECT_ID.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="SERVICE_ROLE_KEY_RAHASIA"
streamlit run app.py
```

## 3. Deploy online
1. Push `app.py`, `requirements.txt`, dan `schema.sql` ke repository GitHub (lebih aman privat).
2. Buat app di https://share.streamlit.io/ dan pilih repository serta `app.py`.
3. Pada App Settings > Secrets, isi tiga nilai dari `secrets.toml.example` dengan nilai asli.
4. Deploy dan uji login, tambah anggota, transaksi, serta laporan.

## Keamanan dan batasan
- Login password aplikasi ini adalah starter sederhana, bukan sistem autentikasi produksi. Untuk penggunaan bisnis sungguhan, migrasikan login ke Supabase Auth, gunakan RLS dan least privilege, tambah pembatasan percobaan login, audit log, dan backup.
- Jangan commit secrets ke GitHub atau membagikan service-role key.
- Versi awal menyimpan transaksi dan payout dalam dua operasi API. Untuk produksi, pindahkan keduanya ke satu transaksi database/server function agar tidak ada penyimpanan parsial jika salah satu langkah gagal.
- Komisi dihitung ketika transaksi dibuat. Mengubah tarif hanya memengaruhi transaksi berikutnya.
