# Çok Amaçlı Sohbet Asistanı

Bu proje, Gradio arayüzü kullanılarak oluşturulmuş, belgeler, web siteleri ve normal sohbet işlemlerini gerçekleştirebilen çok amaçlı bir sohbet asistanıdır. Google Gemini API entegrasyonu sayesinde, doküman ve web sitesi içeriklerinden metin çıkarımı yapıp, sohbet tabanlı yanıtlar üretmektedir.

## Özellikler
- 💬 **Normal Sohbet:** Genel sohbet fonksiyonu ile çeşitli konularda etkileşim kurun.
- 📚 **Doküman Analizi:** PDF, DOCX, DOC ve TXT formatındaki dokümanları yükleyip, içerisindeki metin üzerinden soru-cevap gerçekleştirin.
- 🌐 **Web Sitesi Analizi:** Belirtilen URL'deki web sitesinin içeriğini işleyip analiz edin.
- *(Not: Görsel analiz fonksiyonu kaldırılmıştır.)*

## Demo

### Video Demo
[Demo Videosu](https://youtu.be/your-demo-video-link)  
*Not: Lütfen bu bağlantıyı kendi demo video URL'niz ile güncelleyin.*

### Ekran Görüntüleri
![Uygulama Ana Ekranı](images/main_screen.png)  
*Uygulamanın ana ekranı*

![Doküman İşleme](images/document_processing.png)  
*Doküman yükleme ve işleme ekranı*

## Kurulum ve Kullanım

### Gereksinimler
- Python 3.7 veya üstü
- [Gradio](https://gradio.app/)
- [google-genai](https://pypi.org/project/google-genai/)
- [Pillow (PIL)](https://pillow.readthedocs.io/)
- [BeautifulSoup (bs4)](https://www.crummy.com/software/BeautifulSoup/)
- [requests](https://requests.readthedocs.io/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [python-docx](https://python-docx.readthedocs.io/)

### Adım Adım Kurulum

1. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/kullanici_adiniz/cok-amacli-sohbet-asistani.git
   cd cok-amacli-sohbet-asistani
