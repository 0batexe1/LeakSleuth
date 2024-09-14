import asyncio
import aiohttp # type: ignore
import re
import time
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import logging
import argparse
import json
from termcolor import colored # type: ignore

# Sızıntı patternleri ve açıklamaları
patterns = {
    'E-posta': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    'IP Adresi': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    'Telefon Numarası': r'\b\d{10,12}\b',
    'API Anahtarı': r'(?i)api[_\-]?key[=:]\s*[a-zA-Z0-9]{20,}',
    'JWT Token': r'\beyJ[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\b'
}

# Verileri POST isteği ile gönderme ve enjeksiyon yapma
async def send_post_request(session, url, data):
    try:
        async with session.post(url, data=data) as response:
            return await response.text()
    except Exception as e:
        print(f"POST isteği başarısız: {e}")
        return None

# Başlıklara ve çerezlere enjeksiyon yapma
async def send_request_with_headers_cookies(session, url, headers=None, cookies=None):
    try:
        async with session.get(url, headers=headers, cookies=cookies) as response:
            return await response.text()
    except Exception as e:
        print(f"GET isteği başarısız: {e}")
        return None

# URL'nin farklı bölümlerine yük ekleme
def inject_payload_in_url(url, payload):
    # Sorgu parametrelerine yük ekleme
    if '?' in url:
        url_with_payload = url + f"&{payload}=test"
    else:
        url_with_payload = url + f"?{payload}=test"
    
    # URL'nin yoluna yük ekleme
    url_with_path_payload = url.rstrip('/') + f'/{payload}/'

    return url_with_payload, url_with_path_payload

# Sonuçları CSV dosyasına kaydetme
def save_results_to_csv(results, filename='scan_results.csv'):
    df = pd.DataFrame(results, columns=['URL', 'Pattern', 'Match'])
    df.to_csv(filename, index=False)
    print(f"Sonuçlar '{filename}' dosyasına kaydedildi.")

# Sonuçları görselleştirme
def plot_results(results):
    df = pd.DataFrame(results)
    grouped = df.groupby('URL').size()
    
    plt.figure(figsize=(10, 6))
    grouped.plot(kind='bar')
    plt.xlabel('URL')
    plt.ylabel('Sızıntı Sayısı')
    plt.title('URL Başına Sızıntı Sayısı')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Sonuçları kategorize etme
def categorize_results(results):
    categories = {
        'E-posta': [],
        'IP Adresi': [],
        'Telefon Numarası': [],
        'API Anahtarı': [],
        'JWT Token': []
    }
    for result in results:
        categories[result['Pattern']].append(result)
    return categories

def print_categorized_results(categories):
    for category, items in categories.items():
        print(f"\n{category} Sızıntıları:")
        for item in items:
            print(f"URL: {item['URL']}, Match: {item['Match']}")

# Gelişmiş hata yönetimi
def handle_error(e):
    if isinstance(e, aiohttp.ClientError):
        print(f"HTTP isteği hatası: {e}")
    elif isinstance(e, FileNotFoundError):
        print("Dosya bulunamadı.")
    elif isinstance(e, json.JSONDecodeError):
        print("JSON dosyası hatalı.")
    else:
        print(f"Bir hata oluştu: {e}")

# Komut satırı argümanlarını işleme
def parse_args():
    parser = argparse.ArgumentParser(description='Sızıntı tarama aracı')
    parser.add_argument('-f', '--file', required=True, help='Tarama yapılacak txt dosyası')
    parser.add_argument('-p', '--payload', required=True, help='Kullanılacak payload')
    parser.add_argument('-l', '--log', default='scan_results.log', help='Log dosyasının adı')
    parser.add_argument('-d', '--patterns', default='patterns.json', help='Sızıntı desenleri dosyası')
    parser.add_argument('-r', '--report', default='scan_results.csv', help='Rapor dosyası')
    args = parser.parse_args()
    return args

# Desenleri JSON dosyasından yükleme
def load_patterns(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Veritabanını başlatma
def setup_database():
    logging.basicConfig(filename='scan_results.log', level=logging.INFO)

# Ana tarama fonksiyonu
async def scan_url(session, url, payload, patterns, results):
    print(colored(f"Tarama yapılan URL: {url}", 'blue'))
    url_with_query, url_with_path = inject_payload_in_url(url, payload)
    headers = {'User-Agent': 'Mozilla/5.0', 'X-Test-Header': payload}
    cookies = {'session_id': payload}
    response_text = await send_request_with_headers_cookies(session, url_with_query, headers=headers, cookies=cookies)
    if response_text:
        for key, pattern in patterns.items():
            match = re.search(pattern, response_text)
            if match:
                message = f"[Sızıntı] {key}: {match.group()}"
                print(colored(message, 'red'))
                results.append({'URL': url, 'Pattern': key, 'Match': match.group()})
                logging.info(message)
    data = {'username': payload, 'password': 'test'}
    response_post_text = await send_post_request(session, url_with_path, data=data)
    if response_post_text:
        for key, pattern in patterns.items():
            match = re.search(pattern, response_post_text)
            if match:
                message = f"[POST Sızıntı] {key}: {match.group()}"
                print(colored(message, 'red'))
                results.append({'URL': url, 'Pattern': key, 'Match': match.group()})
                logging.info(message)

# Ana fonksiyon
async def main():
    args = parse_args()
    patterns = load_patterns(args.patterns)
    setup_database()
    results = []
    try:
        with open(args.file, "r") as file:
            urls = file.readlines()
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [scan_url(session, url.strip(), args.payload, patterns, results) for url in urls]
            await asyncio.gather(*tasks)
        elapsed_time = time.time() - start_time
        print(f"Tarama tamamlandı. Geçen süre: {elapsed_time:.2f} saniye")
        save_results_to_csv(results, args.report)
        categories = categorize_results(results)
        print_categorized_results(categories)
        plot_results(results)
    except Exception as e:
        handle_error(e)

if __name__ == "__main__":
    asyncio.run(main())
