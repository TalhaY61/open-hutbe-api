# OPEN HUTBE API (Friday Khutbah / Sermon Archive)

![Update Status](https://github.com/TalhaY61/open-hutbe-api/actions/workflows/weekly_update.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)

This repository serves as an automated archive and a JSON-based API for the weekly **Friday Sermons (Hutbe / Khutbah)** published by the Presidency of Religious Affairs (Diyanet).

It allows developers, researchers, and mobile application creators to access **Jumu'ah sermon** data in a structured format without needing to scrape websites manually.

### 🌍 What is this?
This is a read-only API that provides:
* **Weekly Khutbahs:** The text/PDF of the Friday sermon.
* **Multi-Language:** Supports Turkish, English (Khutbah), German (Freitagspredigt), French, Arabic, and more.
* **Prayers (Dualar):** Standard Arabic prayers recited during the Khutbah.
### How to Use in Your Project

**1. Get All Hutbes (Sermons)**
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json

**2. Get Static Prayers (Dualar)**
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/prayers.json

### Data Structure

The `hutbes.json` file contains an array of objects:
* **id:** Unique identifier.
* **title:** Title of the Hutbe.
* **date:** Date (YYYY-MM-DD).
* **language:** Language code (tr, en, de, etc.).
* **pdf_url:** Direct link to the archived PDF.

### Disclaimer
* **Source:** Official Website of the Presidency of Religious Affairs (Diyanet).
* **Ownership:** Content belongs entirely to Diyanet. This is an open-source mirror project.

______________________________________________________________________

# AÇIK HUTBE API

Diyanet İşleri Başkanlığı tarafından haftalık yayınlanan Cuma Hutbelerini otomatik arşivleyen ve JSON formatında sunan açık kaynak veri deposudur.

### Kullanım

**1. Tüm Hutbeler**
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json

**2. Hutbe Duaları**
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/prayers.json

### Veri Yapısı

`hutbes.json` dosyası şunları içerir:
* **id:** Benzersiz kimlik.
* **title:** Hutbe başlığı.
* **date:** Tarih.
* **language:** Dil kodu.
* **pdf_url:** PDF dosyasına giden kalıcı bağlantı.

### Yasal Uyarı
* **Kaynak:** Diyanet İşleri Başkanlığı Resmi Web Sitesi.
* **Mülkiyet:** İçerik mülkiyeti Diyanet'e aittir. Bu proje kâr amacı gütmeyen bir arşivleme hizmetidir.