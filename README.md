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


### Ekran Görüntüleri
![Uygulama Ana Ekranı]
![Ekran görüntüsü 2025-03-09 152439](https://github.com/user-attachments/assets/7c4e0752-8def-4e02-91be-45acdbbeab18)


![Doküman İşleme](![image](https://github.com/user-attachments/assets/18a8ac17-b299-4634-9939-95fa0bef1c59)
)  
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
