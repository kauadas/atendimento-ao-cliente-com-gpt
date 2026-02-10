from playwright.sync_api import sync_playwright as playwright
from pathlib import Path
import re

class WhatsAppNotLoggedError(Exception):
    pass

class ChatNotFoundError(Exception):
    pass

class MessageSendError(Exception):
    pass


class Zapy:
    def __init__(self, profile: str = "profile/wpp", headless: bool = False):
        try:
            self.p = playwright().start()
            self.context = self.p.chromium.launch_persistent_context(
                profile,
                headless=headless
            )

            self.page = (
                self.context.pages[0]
                if self.context.pages
                else self.context.new_page()
            )

            self.page.goto("https://web.whatsapp.com", timeout=60000)

        except Exception as e:
            self.close()
            raise RuntimeError(f"Erro ao iniciar WhatsApp Web: {e}")


    def wait_login(self, timeout=90000):
        try:
            self.page.get_by_role("grid").wait_for(timeout=timeout)
            
            print("logado")
        except:
            raise WhatsAppNotLoggedError("Login não realizado dentro do tempo limite")


    def open_chat(self, name: str):
        rows = self.page.locator("div[role='row']")

        for i in range(rows.count()):
            row = rows.nth(i)

            try:
                title_el = row.locator("span[dir='auto']").first
                title = title_el.text_content()

                if not title:
                    continue

                if title.strip() == name:
                    row.click()
                    return

            except Exception:
                continue

        raise ChatNotFoundError(f"Chat '{name}' não encontrado")


    def send_message(self, message: str, timeout=5000):
        try:
            box = self.page.get_by_role("textbox").last
            box.click()
            box.fill(message)
            self.page.keyboard.press("Enter")

            self.page.get_by_text(message).last.wait_for(timeout=timeout)

        except Exception:
            raise MessageSendError("Falha ao enviar mensagem")


    def send_file(self, path: str, label: list = ["Fotos e vídeos","Enviar"]):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo '{path}' nao encontrado")
        
        try:
            
            with self.page.expect_file_chooser() as fc:
            # clique REAL no botão de anexo
                self.page.get_by_role("button", name="Anexar").click()
                self.page.locator(f"div[aria-label*='{label[0]}']").click()

            file_chooser = fc.value
            file_chooser.set_files(str(path.resolve()))

            self.page.locator(f"div[aria-label*='{label[1]}']").wait_for(timeout=5000)
            
            self.page.locator(f"div[aria-label*='{label[1]}']").click()


        except Exception:
            raise MessageSendError("Falha ao enviar mensagem")


    def get_last_message(self):
        try:
            msgs = self.page.locator("div.message-in span.copyable-text")
            if msgs.count() == 0:
                return None
            return msgs.last.text_content()
        except:
            return None

    
    def get_last_bot_message(self):
        try:
            msgs = self.page.locator("div.message-out span.copyable-text")
            if msgs.count() == 0:
                return None
            return msgs.last.text_content()
        
        except:
            return None

    
    def get_new_messages(self, label=("mensagem", "mensagens")):
        result = []
        rows = self.page.locator("div[role='row']")

        for i in range(rows.count()):
            row = rows.nth(i)

            try:
                name = row.locator("span[dir='auto']").first.text_content()
                if not name:
                    continue

                badge = row.locator(
                    f"span[aria-label*='{label[0]}'], span[aria-label*='{label[1]}']"
                )

                if badge.count():
                    count = badge.first.text_content()
                    if count and count.isdigit():
                        result.append([name.strip(), int(count)])

            except Exception:
                continue

        return result
    
    def close(self):
        self.context.close()
        self.p.stop()