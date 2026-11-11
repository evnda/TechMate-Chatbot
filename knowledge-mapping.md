# Knowledge Mapping TechMate

**Tema:** Chatbot diagnosis awal permasalahan laptop berbasis Rule-Based System.

| Tag / Intent | Contoh pattern pengguna | Gambaran response bot |
|---|---|---|
| `salam` | halo, hai, selamat pagi | Menyapa dan mengundang pengguna menyampaikan masalah laptop. |
| `bantuan` | kamu bisa bantu apa, fitur chatbot ini apa | Menjelaskan tujuh kategori masalah yang dapat dibantu. |
| `identitas` | kamu siapa, nama kamu siapa | Memperkenalkan TechMate dan menjelaskan cara kerjanya. |
| `diagnosis_laptop_lemot` | laptop saya lemot, laptop loading terus | Panduan bertahap memeriksa Task Manager, CPU/RAM, startup, dan ruang penyimpanan; lanjutkan ke teknisi jika masih lambat. |
| `diagnosis_laptop_panas` | laptop cepat panas, kipas laptop berisik | Panduan mengurangi beban, menjaga ventilasi, membersihkan bagian luar, mengenali tanda bahaya, dan eskalasi ke teknisi. |
| `diagnosis_baterai_boros` | baterai cepat habis, baterai tidak awet | Panduan pengaturan daya, pemeriksaan aplikasi boros, dan battery report Windows. |
| `diagnosis_wifi` | Wi-Fi tidak tersambung, Wi-Fi tidak muncul | Panduan membedakan gangguan router/laptop, menyambungkan ulang jaringan, troubleshooter, dan adaptor. |
| `diagnosis_penyimpanan_penuh` | memori penuh, drive C penuh | Panduan Storage Settings, file sementara, pemindahan data, dan perlindungan file sistem. |
| `diagnosis_laptop_tidak_menyala` | laptop tidak mau menyala, laptop mati total | Panduan pemeriksaan sumber listrik, adaptor, perangkat eksternal, dan reset daya sederhana yang aman. |
| `diagnosis_aplikasi_error` | aplikasi tidak bisa dibuka, aplikasi crash | Panduan mencatat error, menutup proses macet, repair, update, dan instal ulang dari sumber resmi. |
| `terima_kasih` | terima kasih, makasih | Membalas ucapan terima kasih. |
| `perpisahan` | sampai jumpa, dadah | Menutup percakapan dengan salam perpisahan. |
| `fallback` (khusus) | pertanyaan di luar topik / skor di bawah threshold | Tidak langsung menolak; meminta detail tambahan dan mengarahkan pengguna ke kategori yang tersedia. |

**Catatan:** `fallback` bukan intent biasa di dalam array `intents`. Pada kode contoh dosen, fallback disimpan pada properti tersendiri bernama `fallback`. Setiap intent di dalam array `intents` menggunakan `tag`, `patterns`, dan `responses`.


## Detail respons penanganan

Setiap intent diagnosis menyediakan panduan berurutan, dimulai dari pemeriksaan paling sederhana. Respons juga memuat cara mengecek hasil, hal yang tidak boleh dilakukan, dan kondisi kapan pengguna perlu meminta bantuan teknisi. Panduan ini merupakan pemeriksaan awal umum untuk Windows; menu dapat berbeda menurut versi Windows dan model laptop.
