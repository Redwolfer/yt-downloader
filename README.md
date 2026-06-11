# 📥 YouTube Downloader & Universal Audio Converter

Aplikasi CLI (Command Line Interface) berbasis Python yang mudah digunakan untuk mengunduh video/audio YouTube (mendukung *playlist*) serta mengonversi berkas audio secara massal (*batch conversion*) ke berbagai format populer (MP3, WAV, FLAC, M4A, OGG).

Proyek ini dilengkapi dengan **Wizard Batch Script (.bat)** interaktif sehingga dapat dijalankan cukup dengan sekali klik ganda (*double-click*) tanpa perlu mengetik perintah rumit.

---

## 🚀 Fitur Utama

1. **YouTube Downloader ([download.py](download.py))**
   * Download video tunggal sebagai Audio (MP3) atau Video (MP4 kualitas tertinggi).
   * Download seluruh isi **Playlist YouTube** secara otomatis ke dalam subfolder khusus.
   * **Error Tolerance:** Jika satu video di playlist terblokir (usia/bot), proses download tidak akan crash dan otomatis lanjut ke video berikutnya.
   * Deteksi otomatis tipe link (video vs playlist) dengan kemampuan fallback cerdas.

2. **Universal Audio Converter ([audio_converter/universal_converter.py](audio_converter/universal_converter.py))**
   * Mengonversi audio dari format apa saja yang didukung oleh FFmpeg (MP3, WAV, FLAC, M4A, OGG, OPUS, AAC, WMA, dll.).
   * Mendukung konversi satu berkas (*single file*) atau **satu folder penuh (*batch folder conversion*)** secara cepat.
   * Penyimpanan hasil konversi yang rapi di folder `outputs/converted/[format]`.

3. **Batch Wizard Helper (.bat)**
   * **[yt-downloader.bat](yt-downloader.bat):** Menu utama & wizard interaktif untuk download YouTube.
   * **[audio-converter.bat](audio-converter.bat):** Akses cepat langsung ke wizard konversi berkas audio.

---

## 🛠️ Prasyarat (Kebutuhan Awal)

Sebelum menjalankan aplikasi, pastikan komputer Anda telah terpasang:

### 1. Python 3.8 atau yang Lebih Baru
* Download Python di [python.org](https://www.python.org/downloads/).
* **PENTING:** Saat menginstal, pastikan Anda mencentang opsi **"Add Python to PATH"** di bagian bawah jendela installer.

### 2. FFmpeg (Wajib untuk Konversi Audio)
FFmpeg dibutuhkan oleh library `pydub` untuk membaca dan menulis format audio selain WAV (seperti MP3, OPUS, OGG, M4A).

**Cara Install FFmpeg di Windows:**
1. Download berkas FFmpeg siap pakai (build terbaru) dari [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).
2. Ekstrak file `.7z` tersebut menggunakan WinRAR / 7-Zip.
3. Ubah nama folder hasil ekstrak menjadi `ffmpeg` dan pindahkan ke `C:\ffmpeg`.
4. Tambahkan FFmpeg ke System PATH Windows:
   * Cari **"Edit the system environment variables"** di menu Start Windows.
   * Klik tombol **Environment Variables** di bagian bawah.
   * Di bagian *System variables*, cari variabel bernama `Path`, pilih, lalu klik **Edit**.
   * Klik **New** dan masukkan: `C:\ffmpeg\bin`.
   * Klik **OK** pada semua jendela untuk menyimpan.
5. Verifikasi di Command Prompt dengan mengetik: `ffmpeg -version`. Jika muncul detail versinya, instalasi sukses!

## 📥 Cara Instalasi Instan (Sangat Mudah & Otomatis)

Jika komputer Anda masih baru/bersih (belum ada Python, FFmpeg, atau pustaka lainnya), Anda cukup menggunakan installer otomatis yang sudah disediakan:

1. Buka File Explorer ke folder proyek ini.
2. Klik ganda (**double-click**) berkas **`setup.bat`**.
3. Skrip akan mendeteksi kebutuhan komputer Anda secara otomatis:
   - Jika **Python** belum terpasang, skrip akan mengunduh & menginstalnya via `winget` (Windows Package Manager).
   - Jika **FFmpeg** belum terpasang, skrip akan mengunduh & mengaturnya secara otomatis.
   - Membuat folder Virtual Environment (`venv`) dan menginstal seluruh pustaka pendukung.
4. **Catatan Penting:** Jika Python baru saja diinstal oleh skrip, jendela Command Prompt akan meminta Anda untuk menutupnya terlebih dahulu. Cukup tutup jendela tersebut lalu **klik ganda `setup.bat` sekali lagi** untuk menyelesaikan instalasi virtual environment dan dependensinya.

Setelah proses di atas selesai, aplikasi Anda 100% siap dijalankan!

---

## 🛠️ Alternatif: Langkah Instalasi Manual (Developer/Advance)

Jika Anda ingin menginstal dan mengatur semuanya sendiri secara manual:

### Langkah 1: Pasang Python & FFmpeg
* Unduh & instal Python dari [python.org](https://www.python.org/downloads/) (Pastikan Anda mencentang opsi **"Add Python to PATH"** saat instalasi).
* Unduh dan daftarkan FFmpeg ke PATH komputer Anda (Lihat bagian **Prasyarat (Kebutuhan Awal)** di atas).

### Langkah 2: Siapkan Lingkungan Virtual (Virtual Environment)
Buka terminal (CMD / PowerShell / Git Bash) di folder proyek ini, lalu jalankan secara berurutan:

```cmd
:: 1. Buat folder virtual environment
python -m venv venv

:: 2. Aktifkan venv (CMD)
.\venv\Scripts\activate.bat

:: 3. Upgrade pip dan instal dependensi pustaka
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📖 Panduan Penggunaan

Aplikasi ini bisa dijalankan dengan dua cara: menggunakan **Wizard Klik Ganda** (Sangat Mudah) atau **Perintah Terminal/CMD** (Fleksibel).

### Metode 1: Menggunakan Wizard Klik Ganda (Double-Click)
Cukup buka File Explorer Windows, masuk ke folder proyek Anda, lalu klik ganda file berikut:

1. **`yt-downloader.bat` (Downloader YouTube)**
   * Akan muncul menu utama. Pilih `[1]` untuk download YouTube.
   * Masukkan URL YouTube (video tunggal maupun playlist).
   * Pilih format `1` untuk Audio (MP3) atau `2` untuk Video (MP4).
   * Masukkan lokasi penyimpanan atau biarkan kosong untuk default.
   * Tunggu hingga proses selesai, jendela terminal akan tetap terbuka agar Anda bisa membaca status akhir.

2. **`audio-converter.bat` (Audio Converter)**
   * Akan langsung membuka wizard konversi.
   * Masukkan path berkas audio (contoh: `C:\lagu.opus`) atau folder audio (contoh: `C:\AlbumLagu`).
   * Pilih format output target yang diinginkan (MP3, WAV, FLAC, M4A, OGG).
   * Proses konversi massal akan berjalan dengan progress bar.

---

### Metode 2: Menggunakan Terminal / Command Line (CLI)
Buka terminal (CMD / PowerShell / Git Bash) di folder proyek Anda, lalu jalankan perintah berikut tanpa perlu mengaktifkan venv secara manual:

#### **A. YouTube Downloader**
```cmd
:: Download video tunggal sebagai audio (MP3) ke folder default
yt-downloader.bat "https://www.youtube.com/watch?v=nL2HPPHdPAA"

:: Download video tunggal sebagai video (MP4)
yt-downloader.bat "https://www.youtube.com/watch?v=nL2HPPHdPAA" --type video

:: Download seluruh isi playlist ke folder kustom
yt-downloader.bat "https://www.youtube.com/playlist?list=PLBCF2DAC6FFB574DE" --output_dir "D:\Downloads\Music"
```

#### **B. Universal Audio Converter**
```cmd
:: Konversi satu file audio ke format MP3
audio-converter.bat "C:\Music\rekaman.wav" --to mp3

:: Konversi seluruh file audio di dalam folder ke format FLAC
audio-converter.bat "C:\MyAlbum" --to flac

:: Konversi dengan mengatur bitrate audio secara spesifik
audio-converter.bat "C:\Music\rekaman.wav" --to mp3 --bitrate 320k
```

---

## 📂 Struktur Output File

Semua file hasil unduhan dan konversi Anda akan disimpan dengan struktur rapi berikut:
*   `outputs/audio/` - File MP3 hasil unduhan YouTube (Tunggal).
*   `outputs/audio/[Nama_Playlist]/` - File-file MP3 hasil unduhan YouTube Playlist.
*   `outputs/video/` - File MP4 hasil unduhan YouTube (Tunggal).
*   `outputs/video/[Nama_Playlist]/` - File-file MP4 hasil unduhan YouTube Playlist.
*   `outputs/converted/[format_target]/` - File audio hasil konversi Universal Converter.

---

## ❓ FAQ & Troubleshooting

*   **Error: `ffmpeg` not found / "Converter failed"**
    *   *Penyebab:* Library `pydub` tidak menemukan program `ffmpeg` di komputer Anda.
    *   *Solusi:* Pastikan Anda telah mengikuti langkah instalasi FFmpeg di atas dengan benar dan jalur `C:\ffmpeg\bin` sudah terdaftar di System Path Windows Anda. Tutup dan buka kembali terminal Anda setelah mengedit PATH.
*   **Error: `Warning: Failed to load as playlist` saat download playlist**
    *   *Penyebab:* Playlist tersebut diatur ke **Private** oleh pemiliknya, atau playlist tersebut otomatis buatan YouTube (*My Mix/Liked Videos*) yang membutuhkan otentikasi akun.
    *   *Solusi:* Pastikan playlist yang ingin didownload diatur ke **Public** atau **Unlisted**. Jika playlist adalah video tunggal yang memiliki parameter playlist di link-nya, program akan otomatis melakukan *fallback* cerdas dan mendownload video tunggal tersebut saja.
