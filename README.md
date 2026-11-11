# TechMate — Chatbot Diagnosis Permasalahan Laptop

TechMate adalah chatbot tematik berbasis **rule-based** yang membantu pengguna mengenali masalah laptop sehari-hari dan memperoleh saran penanganan awal. Proyek ini dibuat menggunakan Python, Flask, JSON, dan pencocokan kemiripan teks. Chatbot **tidak menggunakan LLM atau API AI generatif**.

## Fitur

- 13 intent: salam, bantuan, identitas, 7 kategori masalah laptop, terima kasih, dan perpisahan.
- Pencocokan pesan berdasarkan `patterns` pada file JSON.
- Respons dipilih dari `responses` sesuai intent yang terdeteksi.
- Panduan penanganan dibuat lebih rinci dan bertahap untuk tujuh kategori masalah, termasuk pemeriksaan hasil, langkah lanjutan, dan batasan keselamatan.
- Fallback yang mengarahkan pengguna untuk menjelaskan masalah lebih spesifik atau memilih topik yang tersedia.
- Antarmuka chat berbasis Flask; pesan dikirim tanpa reload halaman.
- Chatbot dapat dicoba melalui terminal.
- Riwayat percakapan dan statistik disimpan menggunakan SQLite.
- Evaluasi intent menggunakan file CSV.

## Daftar kategori masalah

1. Laptop lemot
2. Laptop cepat panas
3. Baterai boros
4. Wi-Fi bermasalah
5. Penyimpanan penuh
6. Laptop tidak menyala
7. Aplikasi error

## Struktur repository

```text
TechMate-Chatbot/
├── app.py                  # Aplikasi web Flask dan REST API
├── cli.py                  # Chatbot versi terminal
├── evaluate.py             # Evaluasi akurasi intent dari CSV
├── requirements.txt        # Daftar pustaka Python
├── chatbot/
│   ├── __init__.py
│   ├── engine.py           # Mesin rule-based dan pencocokan intent
│   └── database.py        # Penyimpanan riwayat SQLite
├── themes/
│   └── techmate.json       # Knowledge base: tag, patterns, responses, fallback
├── evaluasi/
│   └── techmate.csv        # Data uji kalimat dan label intent
├── templates/              # Template HTML Flask
├── static/                 # CSS dan JavaScript antarmuka chat
├── tests/                  # Pengujian otomatis
└── screenshots/            # Bukti tampilan dan pengujian chatbot
```

## Cara menjalankan di Windows (PowerShell)

Buka terminal pada folder repository, lalu jalankan:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika PowerShell menolak aktivasi environment, jalankan perintah berikut satu kali untuk akun pengguna saat ini, lalu ulangi aktivasi:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Menjalankan chatbot web

```powershell
python app.py
```

Buka browser pada alamat **http://127.0.0.1:5000**. Biarkan terminal server tetap aktif selama chatbot digunakan. Tekan `Ctrl + C` untuk menghentikan server.

### Menjalankan chatbot terminal

Buka terminal kedua pada folder repository, aktifkan environment yang sama, lalu jalankan:

```powershell
python cli.py --tema techmate
```

Ketik `keluar` untuk mengakhiri percakapan.

### Menguji evaluasi intent

```powershell
python evaluate.py --tema techmate --ambang 0.45
python evaluate.py --tema techmate --sweep
```

Data uji berada di `evaluasi/techmate.csv`. Kolom `kalimat` berisi pesan uji, sedangkan kolom `intent` berisi label yang diharapkan. Label `fallback` digunakan untuk pertanyaan di luar topik TechMate.

### Menjalankan pengujian otomatis

```powershell
pytest -q
```

## Cara kerja singkat

1. Pengguna mengirim pesan.
2. Sistem melakukan praproses teks, seperti mengubah huruf menjadi kecil dan menormalisasi beberapa kata tidak baku.
3. Sistem membandingkan pesan dengan seluruh pola (`patterns`) dalam file `themes/techmate.json`.
4. Intent dengan skor tertinggi dipilih jika skornya mencapai threshold.
5. Chatbot mengambil salah satu jawaban dari `responses` milik intent tersebut.
6. Jika skor tidak mencapai threshold, chatbot memberikan respons `fallback` yang mengarahkan pengguna ke topik yang tersedia.

## Mengubah knowledge base

Edit file `themes/techmate.json`. Setiap intent memiliki tiga bagian utama:

- `tag`: nama/kode intent.
- `patterns`: contoh kalimat yang mungkin dikirim pengguna.
- `responses`: variasi jawaban untuk intent tersebut.

Tambahkan variasi kalimat yang benar-benar mungkin digunakan pengguna. Hindari pattern yang terlalu umum atau sama pada dua intent berbeda. Setelah mengubah JSON, jalankan kembali evaluasi CSV untuk melihat apakah pola baru sudah dikenali.

## Catatan evaluasi

Evaluasi menggunakan 40 kalimat uji yang dipisahkan dari pattern utama dalam JSON. Pada konfigurasi threshold `0.45`, hasil pengujian awal mencapai **100% (40 dari 40 kalimat)**. Nilai ini adalah hasil pada dataset uji yang disiapkan untuk proyek ini, bukan jaminan bahwa semua variasi bahasa pengguna akan selalu dikenali. Perluas data uji dengan kalimat dari pengguna sebenarnya untuk evaluasi yang lebih representatif.

## Batasan

TechMate memberikan saran awal berdasarkan pola dan pengetahuan yang telah ditulis. Chatbot tidak memeriksa perangkat secara langsung dan tidak dapat memastikan kerusakan komponen. Untuk masalah yang berlanjut atau berisiko, pengguna disarankan meminta bantuan teknisi.



## Catatan Rule-Based

Pengenalan kalimat tetap menggunakan pattern, normalisasi kata, skor kemiripan, dan threshold. Fallback memiliki dua bentuk: meminta konfirmasi topik terdekat untuk pesan yang hampir cocok, atau meminta pengguna menjelaskan gejala dan memilih kategori untuk pesan yang belum cocok.
