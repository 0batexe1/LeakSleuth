# LeakSleuth

**LeakSleuth** is a powerful tool designed for discovering and analyzing leaked sensitive information in web applications. It performs security assessments by scanning URLs for various types of data leaks using a combination of GET and POST requests.

## Features

- **Asynchronous Scanning**: Utilizes asynchronous HTTP requests for faster performance.
- **Pattern Detection**: Detects various types of sensitive data such as email addresses, IP addresses, phone numbers, API keys, and JWT tokens.
- **CSV Reporting**: Saves scan results to a CSV file for easy access and review.
- **Visualization**: Generates visual reports of detected leaks.
- **Categorization**: Categorizes and organizes detected leaks for better analysis.
- **Error Handling**: Provides detailed error messages for troubleshooting.

## Requirements

- Python 3.6 or higher
- `aiohttp` library
- `pandas` library
- `matplotlib` library
- `termcolor` library

## Installation

To install the required libraries, run:

```bash
pip install aiohttp pandas matplotlib termcolor

Usage

    Prepare a text file with a list of URLs to scan.
    Run the program using the following command:
python leaksleuth.py -f <path_to_txt_file> -p <payload>
    -f specifies the path to the text file containing the URLs.
    -p specifies the payload to use for injections.

    Check the output for detected leaks, saved in a CSV file and visualized in a bar chart.

Example
python leaksleuth.py -f urls.txt -p test_payload
This command scans the URLs listed in urls.txt using test_payload for injections.

License

This project is licensed under the MIT License - see the LICENSE file for details.

diff


### Türkçe README.md

```markdown
# LeakSleuth

**LeakSleuth**, web uygulamalarında sızdırılmış hassas bilgileri keşfetmek ve analiz etmek için tasarlanmış güçlü bir araçtır. GET ve POST isteklerini kullanarak URL'lerde çeşitli veri sızıntılarını tarar.

## Özellikler

- **Asenkron Tarama**: Daha hızlı performans için asenkron HTTP isteklerini kullanır.
- **Desen Tespiti**: E-posta adresleri, IP adresleri, telefon numaraları, API anahtarları ve JWT token gibi çeşitli hassas verileri tespit eder.
- **CSV Raporlama**: Tarama sonuçlarını CSV dosyasına kaydeder.
- **Görselleştirme**: Tespit edilen sızıntıların görsel raporlarını oluşturur.
- **Kategorize Etme**: Tespit edilen sızıntıları kategorize eder ve organize eder.
- **Hata Yönetimi**: Sorun giderme için ayrıntılı hata mesajları sağlar.

## Gereksinimler

- Python 3.6 veya daha yüksek sürüm
- `aiohttp` kütüphanesi
- `pandas` kütüphanesi
- `matplotlib` kütüphanesi
- `termcolor` kütüphanesi

## Kurulum

Gerekli kütüphaneleri yüklemek için aşağıdaki komutu çalıştırın:

```bash
pip install aiohttp pandas matplotlib termcolor

Kullanım

    Tarama yapılacak URL'leri içeren bir metin dosyası hazırlayın.
    Programı çalıştırın:

bash

python leaksleuth.py -f <txt_dosya_yolu> -p <payload>

    -f taranacak URL'leri içeren metin dosyasının yolunu belirtir.
    -p enjeksiyonlar için kullanılacak payload'ı belirtir.

    Sonuçları kontrol edin: Tespit edilen sızıntılar CSV dosyasına kaydedilir ve bir çubuk grafikte görselleştirilir.

Örnek

bash

python leaksleuth.py -f urls.txt -p test_payload

Bu komut, urls.txt dosyasında listelenen URL'leri test_payload payload'ını kullanarak tarar.
Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için LICENSE dosyasına bakınız.

css


Bu `README.md` dosyaları, programınızı GitHub'da paylaşırken kullanıcılar için bilgilendirici ve anlaşılır olacaktır. Her iki dosya da projenizin özelliklerini, gereksinimlerini, kurulum ve kullanım talimatlarını açıklar.
