# My Shopping List

Aplikasi desktop sederhana untuk mencatat daftar belanja, dibuat dengan Python dan Tkinter.
Data disimpan otomatis ke file JSON, jadi daftar tidak hilang saat aplikasi ditutup.

## Fitur

- Tambah barang dengan nama, kategori, jumlah, dan harga satuan
- Cegah barang duplikat (tidak membedakan huruf besar/kecil)
- Ubah nama, kategori, jumlah, dan harga barang
- Tandai barang yang sudah dibeli (klik dua kali atau lewat tombol)
- Hapus satu barang atau hapus semua (dengan konfirmasi)
- Cari barang, filter status (belum/sudah dibeli), dan filter kategori
- Kartu ringkasan: total barang, sudah dibeli, belum dibeli, dan total belanja
- Data tersimpan otomatis di `shopping_data.json`

## Struktur Proyek

| File | Fungsi |
|---|---|
| `Main.py` | Pintu masuk, menjalankan aplikasi |
| `Gui.py` | Tampilan dan logika interaksi (class `ShoppingApp`) |
| `penyimpanan.py` | Menyimpan dan memuat data JSON, daftar kategori |

## Cara Menjalankan

Butuh Python 3.10 atau lebih baru (Tkinter sudah termasuk di instalasi Python untuk Windows).

```
python main.py
```

## Membuat File .exe (Windows)

```
pip install pyinstaller
pyinstaller --onefile --windowed --name MyShoppingList Main.py
```

Hasilnya ada di folder `dist/`. File `shopping_data.json` akan dibuat di folder yang sama
dengan file `.exe` saat ada barang pertama yang ditambahkan.

## Tahap Pengerjaan

1. Memisahkan simpan/muat data ke `penyimpanan.py`
2. Cek duplikat dan fitur ubah nama
3. Jumlah, harga, subtotal, dan total belanja
4. Kategori dan filter status/kategori
5. Memisahkan tampilan ke `gui.py` dan membuat `main.py`
6. Perapian, README, dan build `.exe`