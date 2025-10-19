# Kelompok 
1. Muhammad Kheisar Katsmara Chendu 102022330184
2. Raiyan Faizan 102022300369
3. M. Alvi Choirudin 102022300326
4. I Ketut Bisma Rahman Putra 102022300402

# Simple Marketplace API with JWT

Proyek ini adalah contoh API sederhana yang dibuat dengan Flask untuk sebuah marketplace. API ini mengimplementasikan autentikasi menggunakan JSON Web Token (JWT) untuk melindungi beberapa endpoint.

## Fitur

-   **Framework**: Python 3 & Flask
-   **Autentikasi**: JWT (HS256)
-   **Endpoint Publik**: `/items` untuk melihat daftar produk.
-   **Endpoint Terproteksi**: `/profile` untuk mengubah data user.
-   **Konfigurasi**: Menggunakan file `.env` untuk menyimpan variabel sensitif.

---

## 1. Persiapan & Instalasi

Pastikan Anda memiliki Python 3 dan `pip` terinstal.

**a. Clone Repositori**

```bash
git clone <url-repo-anda>
cd simple-jwt-api
```

**b. Buat Virtual Environment (Direkomendasikan)**

```bash
# Untuk Windows
python -m venv venv
venv\Scripts\activate

# Untuk macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**c. Instal Dependensi**

```bash
pip install -r requirements.txt
```

**d. Konfigurasi Environment**

Buat file bernama `.env` di root direktori dan isi dengan konten berikut. Ganti `JWT_SECRET` dengan string acak yang panjang dan aman.

```ini
JWT_SECRET="bisma-ganteng-banget"
PORT=5000
```

---

## 2. Menjalankan Aplikasi

Untuk menjalankannya, gunakan perintah berikut:

```
pyton app.py
```

Server akan berjalan di `http://127.0.0.1:5000`.

---

## 3. Pengujian API (Menggunakan cURL)

Anda bisa menggunakan Postman atau cURL untuk menguji endpoint.

### Data User Demo

Untuk login, gunakan kredensial berikut:
-   **Email**: `user1@example.com`
-   **Password**: `password123`

### a. Login untuk Mendapatkan Token

Kirim request `POST` ke `/auth/login` untuk mendapatkan `access_token`.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@example.com", "password": "password123"}' \
  [http://127.0.0.1:5000/auth/login](http://127.0.0.1:5000/auth/login)
```

**Respon Sukses (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImVtYWlsIjoidXNlcjFAZXhhbXBsZS5jb20iLCJleHAiOjE3NjA3MjE1NDQsImlhdCI6MTc2MDcyMDY0NH0.doeMB-vjVFbSkWWiYcdUP3ZXdcQWCwjknlH-qSRxUg0"
}
```

### b. Mengakses Endpoint Publik

Endpoint `/items` tidak memerlukan token.

```bash
curl [http://127.0.0.1:5000/items](http://127.0.0.1:5000/items)
```

**Respon Sukses (200 OK):**
```json
{
  "items": [
    { "id": 1, "name": "Laptop Lenovo Legion", "price": 25000000 },
    { "id": 2, "name": "Mechanical Keyboard Logitech", "price": 1500000 },
    { "id": 3, "name": "Wireless Mouse Ignix F1", "price": 750000 }
  ]
}
```

### c. Mengakses Endpoint Terproteksi

Untuk mengakses `/profile`, Anda **wajib** menyertakan token di header `Authorization`.

**1. Simpan token ke variabel (bash/zsh):**

```bash
# Simpan token dari response login ke variabel TOKEN
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" -d '{"email": "user1@example.com", "password": "password123"}' [http://127.0.0.1:5000/auth/login](http://127.0.0.1:5000/auth/login) | jq -r .access_token)
```
> **Catatan:** Perintah di atas menggunakan `jq`. Jika belum terinstal, Anda bisa menyalin token secara manual.

**2. Gagal - Tanpa Token:**

```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"name": "Bisma Ganteng"}' \
  [http://127.0.0.1:5000/profile](http://127.0.0.1:5000/profile)
```
**Respon Gagal (401 Unauthorized):**
```json
{ "error": "Missing or invalid Authorization header" }
```

**3. Sukses - Dengan Token:**

Gunakan variabel `TOKEN` yang sudah disimpan.

```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Kei ganteng"}' \
  [http://127.0.0.1:5000/profile](http://127.0.0.1:5000/profile)
```
**Respon Sukses (200 OK):**
```json
{
  "message": "Profile updated",
  "profile": {
    "name": "Kei ganteng",
    "email": "user1@example.com"
  }
}
```
## Kasus Uji Minimal (Checklist)

* [:white_check_mark:] Login sukses mengembalikan `access_token` valid (de-code JWT cek `sub`, `email`, `exp`).
* [:white_check_mark:] `/items` dapat diakses tanpa header Authorization.
* [:white_check_mark:] `/profile` menolak akses tanpa/invalid/expired token (**401**).
* [:white_check_mark:] `/profile` berhasil update profil milik user sesuai klaim token (**200**).
* [:white_check_mark:] Semua respons berbentuk JSON, status code tepat, error message jelas.
* [:white_check_mark:] Secret tidak hardcode di kode (gunakan `.env`).
* [:white_check_mark:] README berisi perintah run & contoh cURL/Postman.