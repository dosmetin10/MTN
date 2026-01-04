# MTN Enerji Muhasebe ve Stok Backend

Bulut tabanlı muhasebe ve stok yönetimi için temel bir FastAPI + SQLModel backend başlangıcı.

## Özellik Özeti (ilk sürüm)
- Health endpoint (`/api/v1/health`).
- Cari/Müşteri temel CRUD (listeleme, oluşturma).
- Stok modülü: ürün, depo, stok hareketi (giriş/çıkış/transfer) ve stok bakiye sorgusu (ürün/depo kırılımı).
- SQLModel + SQLite varsayılan veritabanı (`.env` ile Postgres vb. uyarlanabilir).

## Kurulum
1. Python 3.10+ kurulu olmalı.
2. Bağımlılıkları yükleyin:
   ```bash
   pip install -e .[dev]
   ```
3. Ortam değişkenleri için `.env.example` dosyasını kopyalayın ve gerekirse düzenleyin:
   ```bash
   cp .env.example .env
   ```

## Çalıştırma
```bash
uvicorn app.main:app --reload
```

Arayüz: `http://localhost:8000/docs` (Swagger UI)

## API Kısa Kılavuz
- **Health**: `GET /api/v1/health`
- **Customers**:
  - `POST /api/v1/customers` (name, title, phone, email, tax_office, tax_number, currency, notes)
  - `GET /api/v1/customers`
  - `GET /api/v1/customers/{id}`
- **Stock**:
  - `POST /api/v1/stock/products` (name, sku, category, unit, currency, price, track_inventory)
  - `GET /api/v1/stock/products`
  - `POST /api/v1/stock/warehouses` (name, location)
  - `GET /api/v1/stock/warehouses`
  - `POST /api/v1/stock/movements` (movement_type: in|out|transfer, quantity, product_id, source_warehouse_id?, target_warehouse_id?, note)
  - `GET /api/v1/stock/movements`
  - `GET /api/v1/stock/balances` (opsiyonel `product_id`, `warehouse_id` filtreleri ile ürün/depo bazlı stok bakiyesi)

## Notlar ve Yol Haritası
- Yetkilendirme, rol bazlı izinler, kur takibi, teklif/sipariş/fatura zinciri ve kasa/banka akışları için modüler genişleme planlanmalıdır.
- Postgres geçişi için `DATABASE__URL` değerini değiştirin; SQLModel `create_all` şemayı otomatik oluşturur.
- Testler ve CI için `pytest`, `ruff` (lint) yapılandırması eklenmiştir.
