# 🌐 Aplikasi Flask Sederhana – AWS RDS + S3 + EC2  GitHub Actions

Aplikasi web sederhana berbasis **Flask** untuk pembelajaran AWS.  
Fitur:
- ✅ Signup & Login (menggunakan RDS PostgreSQL)
- ✅ Upload file (disimpan di S3)
- ✅ Auto-deploy ke EC2 Ubuntu via GitHub Actions

📍 **Semua layanan AWS yang digunakan berada di region `ap-southeast-3` (Jakarta).**

---

## 📁 Fitur Aplikasi

| Route     | Deskripsi                            |
|-----------|--------------------------------------|
| `/signup` | Registrasi user baru                 |
| `/login`  | Login user yang sudah terdaftar      |
| `/upload` | Upload file ke S3 (setelah login)    |
| `/logout` | Logout session                       |

---

## 🧰 Prerequisite

Sebelum mulai, ente perlu:

1. AWS Account aktif
2. EC2 instance Ubuntu (region ap-southeast-3)
3. RDS PostgreSQL instance (region ap-southeast-3)
4. S3 bucket (region ap-southeast-3)
5. GitHub repo (clone dari sini)

---

## ☁️ Setup AWS

### 🔹 1. Setup IAM Role untuk EC2 (Akses ke S3)

#### Langkah Membuat IAM Role:

1. Buka AWS Console → **IAM** → **Roles**
2. Klik **Create role**
3. Pilih:
   - **Trusted entity type**: AWS service
   - **Use case**: EC2
4. Di bagian permissions, pilih:
   - ✅ `AmazonS3FullAccess` (untuk demo)
5. Klik **Next**, beri nama: `FlaskS3AccessRole`
6. Klik **Create role**

#### Attach IAM Role ke EC2:

1. Buka **EC2 Dashboard**
2. Pilih instance ente
3. Klik **Actions > Security > Modify IAM Role**
4. Pilih `FlaskS3AccessRole`
5. Klik **Update IAM Role**

---

### 🔹 2. Setup RDS PostgreSQL

#### Buat RDS PostgreSQL Instance

1. Masuk ke AWS RDS → Create Database
2. Pilih:
   - Engine: **PostgreSQL**
   - Template: **Free tier**
   - Instance class: `db.t3.micro`
   - Region: `ap-southeast-3`
3. Enable public access ✅
4. Catat endpoint, username, dan password
5. Tambahkan rule di security group:
   - Port: `5432`
   - Source: IP EC2 ente

#### Buat DB Baru & Tabel

1. SSH ke EC2:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

2. Install PostgreSQL client:
```bash
sudo apt update
sudo apt install postgresql-client -y
```

3. Connect ke RDS:
```bash
psql -h <rds-endpoint> -U <db-user> -d postgres
```

4. Buat DB baru:
```sql
CREATE DATABASE flask_app;
\c flask_app
```

5. Buat tabel users:
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL
);
```

---

### 🔹 3. Setup S3 Bucket

1. Buka AWS S3 → **Create bucket**
2. Region: `ap-southeast-3`
3. Gunakan nama unik (misal: `flask-upload-demo-123`)
4. Public access: biarkan tetap nonaktif
5. Bucket ini diakses lewat IAM Role EC2

📌 Tambahkan `region_name='ap-southeast-3'` saat inisialisasi boto3 di kode.

---

## 🧑‍💻 Setup di GitHub

### 🔐 Tambahkan GitHub Secrets

Masuk ke repo ente → Settings → Secrets → Actions → Tambahkan:

| Secret Name         | Deskripsi                     |
|---------------------|-------------------------------|
| `EC2_HOST`          | IP address EC2 ente           |
| `EC2_SSH_KEY`       | Private key `.pem`            |
| `RDS_HOST`          | Endpoint RDS                  |
| `RDS_DB_NAME`       | Nama database (`flask_app`)   |
| `RDS_USER`          | Username RDS                  |
| `RDS_PASSWORD`      | Password RDS                  |
| `S3_BUCKET_NAME`    | Nama bucket                   |
| `FLASK_SECRET_KEY`  | Random String apa aja bebazzz |

---

## 🚀 Jalankan Aplikasi Lokal (opsional)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set env variables manual:

```bash
export RDS_HOST=...
export FLASK_SECRET_KEY=...
```

Jalankan:

```bash
python app.py
```

---

## 🚀 Deploy Otomatis via GitHub Actions

Push ke branch `main` akan:

1. SSH ke EC2
2. Upload kode via SCP
3. Install dependency
4. Jalankan ulang Flask

CI/CD config ada di `.github/workflows/ci-cd.yaml`

---

## 🔎 Melihat Data di PostgreSQL (RDS)

1. SSH ke EC2:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

2. Masuk ke DB:
```bash
psql -h <rds-endpoint> -U <db-user> -d flask_app
```

3. Cek data:
```sql
SELECT * FROM users;
```

---

## ⚠️ Keamanan

- Jangan commit `.env`
- Simpan semua secrets di GitHub
- Gunakan IAM Role, bukan access key

---

## 🙌 Kontribusi

Silakan fork repo ini, clone, dan sesuaikan.
Repositori ini untuk latihan AWS + Flask.

---

## 🚧 Cara Pakai Project Ini

Kalau kamu ingin menggunakan project ini dari public repository:

1. **Clone Repo ini**
```bash
git clone https://github.com/frhnardigit/flaskapp.git
cd flaskapp
```

2. **Buat Repository GitHub sendiri** (jika belum punya)
   - Push project ini ke repo ente diri:
     ```bash
     git remote set-url origin git@github.com:usernameente/nama-repo.git
     git push -u origin main
     ```

6. **Push ke `main` → aplikasi otomatis ter-deploy ke EC2** 🎉

---