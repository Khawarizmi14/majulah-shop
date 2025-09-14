# Proyek Aplikasi Django - Majulah Shop

Repositori ini berisi sebuah aplikasi Football Shop sederhana menggunakan Django yang dibuat untuk memenuhi tugas individu mata kuliah Pemrograman Berbasis Platform.

Repo: https://github.com/Khawarizmi14/majulah-shop

Web: https://khawarizmi-aydin-majulahshop.pbp.cs.ui.ac.id

## Mengapa Perlu Data Delivery?

Data delivery adalah proses fundamental pengiriman data antar sistem. Ini dibutuhkan karena platform modern memiliki arsitektur terdistribusi. Fungsinya:

- **Komunikasi Frontend-Backend**: Memungkinkan antarmuka pengguna (frontend) untuk meminta (`request`) dan menerima (`response`) data dari server (backend).
- **Integrasi API**: Menjadi jembatan komunikasi antara aplikasi Anda dengan layanan eksternal atau pihak ketiga (third-party services).
- **Arsitektur Mi**croservices: Memfasilitasi komunikasi antar layanan independen yang menyusun sebuah platform besar.

Tanpa data delivery, komponen-komponen platform tidak dapat bertukar informasi dan tidak akan berfungsi.

## XML vs JSON

**Untuk pengembangan web modern, JSON lebih unggul.**

1. **XML (eXtensible Markup Language)**: Menggunakan sintaksis berbasis tag (`<tag>data</tag>`). Strukturnya lebih detail (verbose) dan ukuran filenya lebih besar.
2. **JSON (JavaScript Object Notation)**: Menggunakan sintaksis berbasis pasangan kunci-nilai (`"key":"value"`). Strukturnya lebih ringkas dan ringan.

### Alasan JSON lebih populer:

- **Efisiensi**: JSON menghasilkan data yang lebih kecil ukurannya, sehingga transfer data lebih cepat dan proses parsing (analisis data) oleh mesin lebih ringan.
- **Kompatibilitas NATIVE dengan JavaScript**: JSON berasal dari JavaScript, data JSON dapat langsung diolah di lingkungan web tanpa perlu library atau proses konversi yang rumit.

## Fungsi `is_valid()` di Form Django

Method `is_valid()` adalah sebuah fungsi Boolean yang **menjalankan semua proses validasi** yang telah didefinisikan pada sebuah Form Django.

Fungsi utamanya:

1. **Validasi Data**: Memeriksa setiap data yang dikirim pengguna terhadap aturan yang ada di form (misalnya, `required`, `max_length`, `EmailField`).
2. **Pembersihan Data (Sanitization)**: Mengubah input menjadi tipe data Python yang benar dan aman.
3. **Populasi Daftar Error**: Jika ada data yang tidak valid, method ini akan mengisi atribut errors pada form dengan pesan kesalahan yang relevan.

Jika `is_valid()` mengembalikan `True`, maka data yang sudah divalidasi dan dibersihkan dapat diakses melalui kamus (`dictionary`) `form.cleaned_data.`

## Mengapa Perlu `csrf_token`?

`csrf_token` adalah sebuah mekanisme untuk **melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF)**.

### Apa yang terjadi jika tidak dipakai?

Seorang penyerang bisa memaksa browser pengguna yang sudah terautentikasi (login) untuk mengirimkan permintaan HTTP yang tidak diinginkan ke aplikasi Anda. Karena permintaan tersebut dikirim bersama cookie sesi yang valid, aplikasi Anda akan menganggapnya sebagai tindakan yang sah dari pengguna.

### Bagaimana `csrf_token` melindunginya?

1. Django menghasilkan sebuah **token rahasia yang unik** per sesi pengguna.
2. Token ini disisipkan sebagai input tersembunyi di dalam form (`<input type="hidden">`).
3. Saat form dikirim (via `POST`), Django akan membandingkan token dari form dengan token yang tersimpan di sisi server untuk sesi tersebut.
4. Jika token tidak cocok atau tidak ada, permintaan akan **ditolak**.

Penyerang tidak memiliki akses ke token rahasia ini, sehingga setiap upaya pemalsuan permintaan akan gagal.

## Implementasi

### 1. Format XML & JSON

Modifikasi `main/views.py` dan tambah fungsi `show_json`, `show_xml`, `show_json_by_id`, `show_xml_by_id`. Kode ini menggunakan serializer bawaan Django untuk mengubah QuerySet menjadi format JSON dan XML.

### 2. Routing URL

Modifikasi `main/urls.py` dan tambah routing untuk setiap fungsi view yang baru dibuat.

```
path('xml/', show_xml, name='show_xml'),
path('json/', show_json, name='show_json'),
path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
```

### 3. Redirect Halaman Form dan Halaman _Detail Product_

Buat file `base.html` di root folder yang selanjutnya akan digunakan untuk _template inheritance_. Kemudian, modifikasi `main.html` agar menggunakan template dari `base.html` tersebut. Halaman `main.html` ini akan menampilkan daftar semua produk yang ada, lengkap dengan tombol untuk mengarahkan ke halaman tambah produk (`add_product.html`) dan tautan individual pada setiap produk untuk menuju ke halaman detailnya (`product_detail.html`).

### 4. Buat Halaman Form

Buat file `forms.py` di `main` untuk mendefinisikan form produk dan file template `add_product.html` yang akan menggunakan form tersebut dengan placeholder `{{ form.as_table }}`.

### 5. Buat Halaman _Detail Product_

Buat file template `product_detail.html` untuk menampilkan semua detail dari satu objek produk yang dipilih. Halaman ini juga akan menyertakan tombol untuk kembali ke daftar produk utama.

## Postman

https://drive.google.com/drive/u/2/folders/1U_NDSyN_DfNs5Xm1y-IDQDTC6C_KTIlJ

## Feedback

Tutorial diberikan dengan sangat baik
