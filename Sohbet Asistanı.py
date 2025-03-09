import gradio as gr
from google import genai
from api_read import GEMINI_API_KEY
import PIL.Image
from bs4 import BeautifulSoup
import io
import requests

class DocumentChat:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.chat = None
        self.normal_chat = None
        self.document_content = ""
        self.normal_chat_history = []

    # Görsel analiz fonksiyonu kaldırıldı

    def process_document(self, file):
        """Doküman işleme fonksiyonu"""
        if file is None:
            return "Lütfen bir doküman yükleyin."

        try:
            import os
            import shutil
            from datetime import datetime
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            original_filename = os.path.basename(file.name)
            file_extension = original_filename.split('.')[-1].lower()
            new_filename = f"{timestamp}_{original_filename}"
            file_path = os.path.join(upload_dir, new_filename)

            # Save the uploaded file
            shutil.copy2(file.name, file_path)

            if file_extension == 'pdf':
                with open(file_path, 'rb') as pdf_file:
                    # Burada PyPDF2 importunun eklenmesi gerekebilir
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        except Exception as e:
                            print(f"Sayfa okuma hatası: {e}")
                            continue

                if not text.strip():
                    return "PDF'den metin çıkarılamadı. Dosya boş veya okunamıyor olabilir."

                self.document_content = text

            elif file_extension in ['docx', 'doc']:
                import docx
                doc = docx.Document(file_path)
                self.document_content = "\n".join([para.text for para in doc.paragraphs])

            elif file_extension == 'txt':
                with open(file_path, 'r', encoding='utf-8') as txt_file:
                    self.document_content = txt_file.read()

            else:
                return "Desteklenmeyen dosya formatı. Lütfen PDF, DOCX veya TXT dosyası yükleyin."

            if not self.document_content.strip():
                return "Dokümandan metin çıkarılamadı."

            self.chat = self.client.chats.create(model="gemini-2.0-flash")

            max_chunk_size = 4000
            content_chunks = [
                self.document_content[i:i + max_chunk_size]
                for i in range(0, len(self.document_content), max_chunk_size)
            ]

            for chunk in content_chunks:
                try:
                    self.chat.send_message(f"Doküman içeriği (devam): {chunk}")
                except Exception as e:
                    print(f"Chunk gönderme hatası: {e}")
                    continue

            return "Doküman başarıyla yüklendi ve işlendi."

        except Exception as e:
            error_msg = str(e)
            print(f"Hata detayı: {error_msg}")
            return f"Doküman işlenirken hata oluştu: {error_msg}"

    def process_website(self, url):
        """Web sitesi işleme fonksiyonu"""
        if not url:
            return "Lütfen bir URL girin."

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            for tag in soup(['script', 'style', 'meta', 'link']):
                tag.decompose()

            text = soup.get_text(separator='\n', strip=True)
            self.document_content = text

            self.chat = self.client.chats.create(model="gemini-2.0-flash")

            max_chunk_size = 4000
            content_chunks = [
                self.document_content[i:i + max_chunk_size]
                for i in range(0, len(self.document_content), max_chunk_size)
            ]

            for chunk in content_chunks:
                try:
                    self.chat.send_message(f"Web sitesi içeriği (devam): {chunk}")
                except Exception as e:
                    print(f"Chunk gönderme hatası: {e}")
                    continue

            return "Web sitesi içeriği başarıyla işlendi."

        except Exception as e:
            return f"Web sitesi işlenirken hata oluştu: {str(e)}"

    def chat_with_doc(self, message, history):
        """Doküman tabanlı sohbet fonksiyonu"""
        if not self.chat or not self.document_content:
            return "Lütfen önce bir doküman yükleyin veya web sitesi URL'si girin."

        try:
            prompt = f"""Soru: {message}

Lütfen bu soruyu sadece verilen doküman içeriğine dayanarak yanıtla.
Eğer cevap dokümanda yoksa, bunu belirt."""
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Sohbet sırasında hata oluştu: {str(e)}"

    def normal_chat_response(self, message, history):
        """Normal sohbet yanıtları için (hafıza modu ile)"""
        try:
            if not self.normal_chat:
                self.normal_chat = self.client.chats.create(model="gemini-2.0-flash")

            # Geçmiş sohbeti birleştir
            full_conversation = ""
            for user_msg, bot_msg in history:
                full_conversation += f"Kullanıcı: {user_msg}\nAsistan: {bot_msg}\n"

            # Yeni mesajı geçmişe ekle
            full_conversation += f"Kullanıcı: {message}\nAsistan: "

            # Modelden yanıt al
            response = self.normal_chat.send_message(full_conversation)
            return response.text

        except Exception as e:
            return f"Sohbet sırasında hata oluştu: {str(e)}"


def create_chat_interface():
    chat_bot = DocumentChat()

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
        neutral_hue="slate"
    ).set(
        body_background_fill="*neutral_50",
        button_primary_background_fill="*primary_600",
        button_primary_background_fill_hover="*primary_700",
        button_primary_text_color="white",
        block_title_text_weight="600",
        block_border_width="2px",
        block_shadow="*shadow_md",
        block_background_fill="white",
        input_background_fill="*neutral_50"
    )

    with gr.Blocks(theme=theme) as interface:
        with gr.Column(scale=1):
            gr.Markdown(""" 
# 🤖 Çok Amaçlı Sohbet Asistanı

### Özellikler
- 💬 Normal Sohbet
- 📚 Doküman Analizi
- 🌐 Web Sitesi Analizi
""")

            with gr.Tabs() as tabs:
                with gr.Tab("💬 Normal Sohbet", id=0):
                    with gr.Column():
                        normal_chat = gr.ChatInterface(
                            fn=chat_bot.normal_chat_response,
                            title="Genel Sohbet",
                            description="Herhangi bir konu hakkında sohbet edebilirsiniz",
                            examples=[
                                "Merhaba, nasılsın?",
                                "Bana Python programlama hakkında bilgi verir misin?",
                                "Yapay zeka nedir?",
                                "En son teknolojik gelişmeler nelerdir?"
                            ],
                            theme=theme
                        )

                with gr.Tab("📂 Doküman İşleme", id=1):
                    with gr.Column():
                        file_input = gr.File(
                            label="Doküman Seçin",
                            file_types=[".pdf", ".docx", ".doc", ".txt"]
                        )
                        upload_status = gr.Textbox(
                            label="İşlem Durumu",
                            interactive=False
                        )
                        with gr.Column():
                            doc_chat = gr.ChatInterface(
                                fn=chat_bot.chat_with_doc,
                                title="Doküman Sohbet",
                                description="Yüklenen doküman hakkında sorularınızı sorun",
                                examples=[
                                    "Bu dokümanın ana konusu nedir?",
                                    "Önemli noktaları özetler misin?",
                                    "Bu içerikte hangi tarihler geçiyor?"
                                ],
                                theme=theme
                            )

                with gr.Tab("🌐 Web Sitesi İşleme", id=2):
                    with gr.Column():
                        url_input = gr.Textbox(
                            label="Web Sitesi URL",
                            placeholder="https://example.com"
                        )
                        url_button = gr.Button(
                            "🔍 Siteyi Analiz Et",
                            variant="primary"
                        )
                        url_status = gr.Textbox(
                            label="İşlem Durumu",
                            interactive=False
                        )
                        with gr.Column():
                            web_chat = gr.ChatInterface(
                                fn=chat_bot.chat_with_doc,
                                title="Web İçerik Sohbet",
                                description="Web sitesi içeriği hakkında sorularınızı sorun",
                                examples=[
                                    "Bu web sitesinin ana konusu nedir?",
                                    "Önemli bilgileri özetler misin?",
                                    "Site içeriğinde hangi konular ele alınmış?"
                                ],
                                theme=theme
                            )

        # Event handlers
        file_input.upload(
            fn=chat_bot.process_document,
            inputs=[file_input],
            outputs=[upload_status]
        )

        url_button.click(
            fn=chat_bot.process_website,
            inputs=[url_input],
            outputs=[url_status]
        )

    return interface

if __name__ == "__main__":
    interface = create_chat_interface()
    interface.launch(
        debug=True,
        show_error=True,
        share=True,
        server_port=7860,
        server_name="0.0.0.0"
    )
