Proje Hakkında

Bu Python script'i, web uygulamalarında yaygın olarak bulunan çeşitli zafiyetleri (SQL Enjeksiyonu, Cross-Site Scripting - XSS, Yol Gezinmesi - Path Traversal, Komut Enjeksiyonu - Command Injection ve Yerel Dosya Ekleme - Local File Inclusion - LFI) tespit etmek amacıyla tasarlanmış güçlü ve asenkron bir araçtır. Kapsamlı payload listeleri kullanarak, hedef URL'nin farklı parametrelerine ve yollarına enjeksiyon denemeleri yapar. Amacı, güvenlik araştırmacılarının ve sızma testleri uzmanlarının potansiyel zafiyet noktalarını hızlı ve verimli bir şekilde belirlemesine yardımcı olmaktır.

Amaç ve Hedef Kitle

Bu projenin temel amacı, web uygulamalarında en yaygın ve kritik zafiyet türlerini otomatik olarak tespit etmek için bir başlangıç noktası sunmaktır. Özellikle şu kitlelere hitap eder:

    Güvenlik Araştırmacıları: Web uygulamalarındaki bilinen zafiyet kalıplarını hızlıca taramak ve ilk değerlendirmeyi yapmak için.
    Sızma Testleri Uzmanları: Belirli zafiyet türleri için kapsamlı payload setleri ile hedef sistemleri denemek için.
    Geliştiriciler: Kendi uygulamalarının bu tür zafiyetlere karşı ne kadar dirençli olduğunu test etmek için.

Özellikler

    Geniş Zafiyet Kapsamı: SQL Enjeksiyonu, XSS, Yol Gezinmesi, Komut Enjeksiyonu ve LFI için zengin ve çeşitli payload listeleri içerir.
    Asenkron Tarama: asyncio ve aiohttp kütüphanelerini kullanarak yüksek performanslı ve hızlı tarama sağlar.
    Esnek Enjeksiyon Noktaları: Payload'ları URL'nin sorgu parametrelerine, yoluna, HTTP başlıklarına ve çerezlere enjekte etme yeteneği.
    Renkli Çıktı: Terminalde bulguları ve ilerlemeyi görsel olarak ayırt etmek için renkli çıktılar kullanır.
    Akıllı Yanıt Analizi: Yanıtlarda hassas bilgi (e-posta, IP adresi, telefon numarası, API anahtarı, JWT token) ve enjeksiyon başarısını gösteren kalıpları arar.
    Manuel Test Adımları: Tespit edilen potansiyel zafiyetler için manuel doğrulama ve test adımları önerileri sunar.
    Çözüm Önerileri: Her zafiyet türü için genel çözüm ve mitigasyon (hafifletme) önerileri sağlar.

Gereklilikler

Bu aracı kullanmak için sisteminizde aşağıdaki yazılımların kurulu olması gerekir:

    Python 3.7+: Script Python 3.7 ve üzeri ile uyumludur.
    aiohttp kütüphanesi: Asenkron HTTP istekleri için. pip install aiohttp komutu ile kurulabilir.
    termcolor kütüphanesi: Terminal çıktılarını renklendirmek için. pip install termcolor komutu ile kurulabilir.

Kurulum ve Kullanım

    Gerekli Kütüphaneleri Kurun:
    Script'i çalıştırmadan önce, Python ortamınızda aiohttp ve termcolor kütüphanelerinin kurulu olduğundan emin olun:
    pip install aiohttp termcolor

    Script'i İndirin:
    Bu projenin GitHub deposundan 'idsresponsescan.py' dosyasını indirin veya kopyalayın.

    URL Listesi Hazırlayın:
    Taramak istediğiniz URL'leri her satıra bir tane gelecek şekilde bir metin dosyasına kaydedin (örneğin: 'targets.txt').

Örnek targets.txt:
https://example.com/vulnerable_page?param=
https://test.site.org/index.php?id=

    Script'i Çalıştırın: Terminalinizde script'in bulunduğu dizine gidin ve aşağıdaki komutu çalıştırın. Script sizden URL'lerin bulunduğu dosyanın adını isteyecektir. python idsresponsescan.py

İstendiğinde dosya adını girin:
Tarama yapılacak txt dosyasını girin: targets.txt

Bulguları Değerlendirme

Tarama tamamlandığında, terminalde tespit edilen tüm potansiyel sömürü noktalarını renkli olarak göreceksiniz. Her bulgu için aşağıdaki bilgiler listelenir:

    Sömürülen URL: Payload'ın uygulandığı URL.
    Kullanılan Payload: Başarılı olan enjeksiyon payload'ı.
    Zafiyet Nerede: Payload'ın enjekte edildiği parametre veya yol bilgisi.
    Manuel Test Adımları: Zafiyeti tarayıcınızda veya manuel olarak nasıl doğrulayabileceğinize dair adımlar.
    Zafiyetin Sebebi: Genel zafiyet kök nedeni açıklaması (örn. giriş doğrulaması eksikliği).
    Çözüm Önerisi: Zafiyeti düzeltmek için genel mitigasyon önerileri.

Önemli Not: Bu tarayıcı bir otomatik araç olup, sonuçlar hatalı pozitifler (false positives) içerebilir. Yanıtta bulunan anahtar kelimeler her zaman gerçek bir sömürülebilir zafiyeti işaret etmeyebilir. Tespit edilen her bulguyu manuel olarak doğrulamanız ve potansiyel etkisini teyit etmeniz kritik öneme sahiptir. Örneğin, bir SQLi payload'ı yanıtı değiştirdiğinde, bu değişimin gerçekten bir SQL sorgusu enjeksiyonundan kaynaklanıp kaynaklanmadığını anlamalısınız.

Önemli Etik Not

Bu araç, web uygulamalarındaki güvenlik zafiyetlerini tespit etmek için tasarlanmıştır. Bu tür araçların yalnızca yasal ve etik sınırlar içinde kullanılması büyük önem taşımaktadır. Hedef sistemler üzerinde test yapmadan önce kesinlikle sahibinden yazılı izin almalısınız. İzinsiz tarama veya sömürü girişimleri yasa dışıdır ve ciddi hukuki sonuçları olabilir. Bu aracın kötüye kullanımıyla ilgili herhangi bir sorumluluk kabul edilmez.

Katkıda Bulunma

Proje daha fazla geliştirmeye açık! Yeni payload'lar eklemek, zafiyet tespit mantığını iyileştirmek, hata yönetimi geliştirmeleri yapmak veya yeni özellikler önermek isterseniz, geri bildirimleriniz, hata raporlarınız ve katkılarınız her zaman açığız. Bir çekme isteği (pull request) göndermeden önce lütfen mevcut sorunları kontrol edin veya yeni bir sorun açın.

Lisans

Bu proje MIT Lisansı altında yayınlanmıştır. Daha fazla bilgi için 'LICENSE' dosyasına bakın.

İletişim

Sorularınız, önerileriniz veya işbirliği talepleriniz için bana github.com/0batexe1 üzerinden ulaşabilirsiniz.

English Version

Exploitation Scanner

About The Project

This Python script is a powerful, asynchronous tool designed to detect various common vulnerabilities in web applications, including SQL Injection, Cross-Site Scripting (XSS), Path Traversal, Command Injection, and Local File Inclusion (LFI). It attempts injection by sending various payloads to different parameters and paths of a target URL. Its purpose is to help security researchers and penetration testers efficiently and quickly identify potential vulnerability points.

Purpose and Target Audience

The primary goal of this project is to provide a starting point for automatically detecting the most common and critical types of vulnerabilities in web applications. It specifically targets the following audiences:

    Security Researchers: For quickly scanning web applications for known vulnerability patterns and performing initial assessments.
    Penetration Testers: For testing target systems with comprehensive payload sets for specific vulnerability types.
    Developers: For testing the resilience of their own applications against these types of vulnerabilities.

Features

    Broad Vulnerability Coverage: Includes rich and diverse payload lists for SQL Injection, XSS, Path Traversal, Command Injection, and LFI.
    Asynchronous Scanning: Utilizes asyncio and aiohttp libraries for high-performance and fast scanning.
    Flexible Injection Points: Capable of injecting payloads into URL query parameters, paths, HTTP headers, and cookies.
    Colored Output: Uses colored output in the terminal to visually distinguish findings and progress.
    Smart Response Analysis: Searches for sensitive information (email, IP address, phone number, API key, JWT token) and patterns indicating successful injection in responses.
    Manual Testing Steps: Provides suggestions for manual verification and testing steps for detected potential vulnerabilities.
    Remediation Suggestions: Offers general solution and mitigation recommendations for each vulnerability type.

Requirements

To use this tool, the following software must be installed on your system:

    Python 3.7+: The script is compatible with Python 3.7 and above.
    aiohttp library: For asynchronous HTTP requests. Can be installed with pip install aiohttp.
    termcolor library: For coloring terminal output. Can be installed with pip install termcolor.

Installation and Usage

    Install Required Libraries:
    Before running the script, ensure that the aiohttp and termcolor libraries are installed in your Python environment:
    pip install aiohttp termcolor

    Download the Script:
    Download or copy the 'idsresponsescan.py' file from this project's GitHub repository.

    Prepare Your URL List:
    Save the URLs you want to scan in a text file, with one URL per line (e.g., 'targets.txt').

Example targets.txt:
https://example.com/vulnerable_page?param=
https://test.site.org/index.php?id=

    Run the Script: Navigate to the directory where you saved the script in your terminal and run the following command. The script will prompt you for the name of the file containing your URLs. python idsresponsescan.py

Enter the file name when prompted:
Tarama yapılacak txt dosyasını girin: targets.txt

Evaluating Findings

Once the scan is complete, you will see all detected potential exploitation points highlighted in color in your terminal. For each finding, the following information is listed:

    Exploited URL: The URL where the payload was applied.
    Payload Used: The successful injection payload.
    Vulnerability Location: Information about the parameter or path where the payload was injected.
    Manual Test Steps: Steps on how to manually verify the vulnerability in your browser or with other tools.
    Reason for Vulnerability: A general explanation of the vulnerability's root cause (e.g., missing input validation).
    Suggested Solution: General mitigation recommendations to fix the vulnerability.

Important Note: This scanner is an automated tool, and the results may contain false positives. Keywords found in the response do not always indicate a truly exploitable vulnerability. It is crucial to manually verify each detected finding and confirm its potential impact. For example, if an SQLi payload changes the response, you must confirm whether this change genuinely resulted from an SQL query injection.

Important Ethical Note

This tool is designed to identify security vulnerabilities in web applications. It is of utmost importance that such tools are used strictly within legal and ethical boundaries. You must obtain explicit written permission from the owner before conducting any tests on target systems. Unauthorized scanning or exploitation attempts are illegal and can lead to severe legal consequences. No responsibility is assumed for any misuse of this tool.

Contributing

The project is open for further development! If you'd like to add new payloads, improve vulnerability detection logic, enhance error handling, or suggest new features, your feedback, bug reports, and contributions are always welcome. Please check for existing issues or open a new one before submitting a pull request.

License

This project is licensed under the MIT License. See the 'LICENSE' file for more details.

Contact

For any questions, suggestions, or collaboration inquiries, feel free to reach out to me via github.com/0batexe1.
