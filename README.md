# Open Hutbe API

![Update Status](https://github.com/TalhaY61/open-hutbe-api/actions/workflows/weekly_update.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)

Open Hutbe API is a public, read-only archive for weekly Friday sermons published by the Presidency of Religious Affairs of Türkiye, Diyanet İşleri Başkanlığı.

The goal is simple: instead of every app, website, researcher, or community project scraping Diyanet separately, this repository keeps a structured JSON index and archived PDF links that can be fetched directly.

## What You Can Use It For

- Show the latest weekly hutbe in a mobile app or website.
- Build a searchable khutbah or hutbe archive.
- Download official sermon PDFs by language and date.
- Access standard khutbah prayer PDFs.
- Avoid maintaining your own scraper for Diyanet's pages.

## API Endpoints

All data is served as static files, so you can fetch it from any client that can read JSON.

**All hutbes**

```text
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json
```

**Khutbah prayers**

```text
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/prayers.json
```

The `pdf_url` values in the JSON point to archived PDF files hosted through GitHub Pages:

```text
https://TalhaY61.github.io/open-hutbe-api/
```

## Hutbe Data Format

`hutbes.json` is an array of sermon records. Newer records are inserted near the top when the scraper finds them.

```json
{
  "id": "5f00535280deb99c",
  "title": "Being a family",
  "date": "2026-06-26",
  "year": 2026,
  "language": "en",
  "filename": "being-a-family.pdf",
  "source_pdf_url": "https://dinhizmetleri.diyanet.gov.tr/Documents/Being%20a%20family.pdf",
  "pdf_url": "https://TalhaY61.github.io/open-hutbe-api/pdfs/en/2026/being-a-family.pdf"
}
```

Field meaning:

- `id`: stable ID generated from the original Diyanet PDF URL.
- `title`: sermon title as found on the source page.
- `date`: sermon date in `YYYY-MM-DD` format when available.
- `year`: year used for archive organization.
- `language`: language code, such as `tr`, `en`, `de`, `fr`, `ar`, `ru`, `it`, or `es`.
- `filename`: archived PDF filename in this repository.
- `source_pdf_url`: original PDF URL from Diyanet.
- `pdf_url`: public archived PDF URL you can use in your app.

## Prayer Data Format

`prayers.json` contains static khutbah prayer PDFs, such as Friday and Eid khutbah prayers.

```json
{
  "id": "friday_prayer",
  "title": "Friday Khutbah Prayers",
  "filename": "friday-khutbah-prayers.pdf",
  "pdf_url": "https://TalhaY61.github.io/open-hutbe-api/pdfs/prayers/friday-khutbah-prayers.pdf",
  "source_url": "https://dinhizmetleri.diyanet.gov.tr/HutbeDualari/Cuma%20Hutbesi%20Dualar%C4%B1.pdf"
}
```

## Example Usage

JavaScript example:

```js
const response = await fetch(
  "https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json"
);

const hutbes = await response.json();
const latestTurkishHutbe = hutbes.find((hutbe) => hutbe.language === "tr");

console.log(latestTurkishHutbe.title);
console.log(latestTurkishHutbe.pdf_url);
```

Flutter / Dart example:

```dart
final response = await http.get(
  Uri.parse(
    'https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json',
  ),
);

final hutbes = jsonDecode(response.body) as List<dynamic>;
final latestTurkishHutbe = hutbes.firstWhere(
  (hutbe) => hutbe['language'] == 'tr',
);

print(latestTurkishHutbe['title']);
print(latestTurkishHutbe['pdf_url']);
```

## How Updates Work

The repository is updated automatically with GitHub Actions.

The scraper checks Diyanet's hutbe pages on Thursday late UTC and again on Friday morning UTC. When it finds new PDFs, it downloads and archives them under `pdfs/`, updates `hutbes.json`, and commits the changes back to the repository.

Current scheduled checks:

- Thursday at `22:30` and `23:30` UTC.
- Friday at `07:00` and `10:00` UTC.

If no new hutbe is available, the workflow finishes without creating a commit.

## Notes for App Developers

- Treat this as a public static API. There is no authentication.
- Cache the JSON in your app if you want faster loading, but refresh it regularly around Thursday night and Friday.
- Use `language` to filter for the language your users need.
- Use `pdf_url` for the archived copy and `source_pdf_url` if you want to link back to the original Diyanet file.
- GitHub raw file delivery and GitHub Pages may have their own cache behavior, so very new updates can take a short time to appear everywhere.

## Source and Disclaimer

The sermon and prayer content belongs to Diyanet İşleri Başkanlığı. This repository is an open-source mirror and index created to make public hutbe data easier to access in structured form. It is not an official Diyanet project.

---

# Açık Hutbe API

Açık Hutbe API, Diyanet İşleri Başkanlığı tarafından yayınlanan haftalık Cuma hutbelerini JSON formatında sunan, herkese açık ve salt okunur bir arşiv projesidir.

Amaç basit: Her uygulama, web sitesi veya araştırma projesi Diyanet sitesini ayrı ayrı taramak zorunda kalmasın. Bu depo hutbeleri düzenli bir JSON listesi halinde sunar ve PDF dosyalarının arşivlenmiş bağlantılarını verir.

## Ne İçin Kullanılabilir?

- Mobil uygulamada veya web sitesinde en güncel hutbeyi göstermek.
- Aranabilir bir hutbe arşivi oluşturmak.
- Hutbe PDF dosyalarına dil ve tarihe göre ulaşmak.
- Cuma ve bayram hutbesi dualarına erişmek.
- Kendi Diyanet tarayıcınızı yazmak ve bakımını yapmak zorunda kalmamak.

## API Bağlantıları

Veriler statik JSON dosyaları olarak sunulur. JSON okuyabilen herhangi bir istemciyle kullanabilirsiniz.

**Tüm hutbeler**

```text
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json
```

**Hutbe duaları**

```text
https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/prayers.json
```

JSON içindeki `pdf_url` değerleri GitHub Pages üzerinden yayınlanan arşivlenmiş PDF dosyalarına gider:

```text
https://TalhaY61.github.io/open-hutbe-api/
```

## Hutbe Veri Yapısı

`hutbes.json`, hutbe kayıtlarından oluşan bir listedir. Yeni hutbeler bulundukça listenin üst tarafına eklenir.

```json
{
  "id": "6574eb2570175457",
  "title": "Birlikte Rahmet Vardır",
  "date": "2026-06-19",
  "year": 2026,
  "language": "tr",
  "filename": "birlikte-rahmet-vardir.pdf",
  "source_pdf_url": "https://dinhizmetleri.diyanet.gov.tr/Documents/Birlikte%20Rahmet%20Vard%C4%B1r.pdf",
  "pdf_url": "https://TalhaY61.github.io/open-hutbe-api/pdfs/tr/2026/birlikte-rahmet-vardir.pdf"
}
```

Alanların anlamı:

- `id`: Orijinal Diyanet PDF bağlantısından üretilen benzersiz kimlik.
- `title`: Kaynak sayfada bulunan hutbe başlığı.
- `date`: Varsa `YYYY-MM-DD` formatında hutbe tarihi.
- `year`: Arşiv klasörü için kullanılan yıl.
- `language`: Dil kodu. Örnek: `tr`, `en`, `de`, `fr`, `ar`, `ru`, `it`, `es`.
- `filename`: Bu depodaki arşivlenmiş PDF dosya adı.
- `source_pdf_url`: Diyanet üzerindeki orijinal PDF bağlantısı.
- `pdf_url`: Uygulamanızda kullanabileceğiniz arşivlenmiş PDF bağlantısı.

## Dualar Veri Yapısı

`prayers.json`, Cuma hutbesi ve bayram hutbesi duaları gibi sabit dua PDF dosyalarını içerir.

```json
{
  "id": "friday_prayer",
  "title": "Friday Khutbah Prayers",
  "filename": "friday-khutbah-prayers.pdf",
  "pdf_url": "https://TalhaY61.github.io/open-hutbe-api/pdfs/prayers/friday-khutbah-prayers.pdf",
  "source_url": "https://dinhizmetleri.diyanet.gov.tr/HutbeDualari/Cuma%20Hutbesi%20Dualar%C4%B1.pdf"
}
```

## Kullanım Örneği

JavaScript örneği:

```js
const response = await fetch(
  "https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json"
);

const hutbes = await response.json();
const latestTurkishHutbe = hutbes.find((hutbe) => hutbe.language === "tr");

console.log(latestTurkishHutbe.title);
console.log(latestTurkishHutbe.pdf_url);
```

Flutter / Dart örneği:

```dart
final response = await http.get(
  Uri.parse(
    'https://raw.githubusercontent.com/TalhaY61/open-hutbe-api/main/hutbes.json',
  ),
);

final hutbes = jsonDecode(response.body) as List<dynamic>;
final latestTurkishHutbe = hutbes.firstWhere(
  (hutbe) => hutbe['language'] == 'tr',
);

print(latestTurkishHutbe['title']);
print(latestTurkishHutbe['pdf_url']);
```

## Güncellemeler Nasıl Yapılıyor?

Bu depo GitHub Actions ile otomatik olarak güncellenir.

Tarayıcı, Diyanet hutbe sayfalarını Perşembe gecesi UTC saatine göre ve Cuma sabahı tekrar kontrol eder. Yeni PDF dosyaları bulunursa dosyalar `pdfs/` klasörüne indirilir, `hutbes.json` güncellenir ve değişiklikler depoya commit edilir.

Mevcut otomatik kontrol saatleri:

- Perşembe `22:30` ve `23:30` UTC.
- Cuma `07:00` ve `10:00` UTC.

Yeni hutbe bulunmazsa workflow commit oluşturmadan tamamlanır.

## Uygulama Geliştirenler İçin Notlar

- Bu proje herkese açık statik bir API gibi kullanılabilir. Kimlik doğrulama gerekmez.
- Daha hızlı açılış için JSON verisini uygulamanızda cache'leyebilirsiniz; ancak Perşembe gecesi ve Cuma günü düzenli yenilemek iyi olur.
- Kullanıcı diline göre filtreleme yapmak için `language` alanını kullanın.
- Arşivlenmiş PDF için `pdf_url`, Diyanet'teki orijinal dosyaya gitmek için `source_pdf_url` kullanılabilir.
- GitHub raw dosyaları ve GitHub Pages tarafında cache olabilir. Bu nedenle yeni güncellemelerin her yerde görünmesi kısa bir süre alabilir.

## Kaynak ve Yasal Not

Hutbe ve dua içeriklerinin hakları Diyanet İşleri Başkanlığı'na aittir. Bu depo, herkese açık hutbe verilerini düzenli ve kolay kullanılabilir hale getirmek için oluşturulmuş açık kaynaklı bir ayna ve indeks projesidir. Resmi bir Diyanet projesi değildir.
