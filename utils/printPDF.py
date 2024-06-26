import base64
import json
import logging
import time
from io import BytesIO
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class PdfGenerator:
    """
    Simple use case:
       pdf_file = PdfGenerator(['https://google.com']).main()
       with open('new_pdf.pdf', "wb") as outfile:
           outfile.write(pdf_file[0].getbuffer())
    """

    driver = None
    # https://chromedevtools.github.io/devtools-protocol/tot/Page#method-printToPDF
    print_options = {
        "landscape": False,
        "displayHeaderFooter": False,
        "printBackground": True,
        "preferCSSPageSize": True,
        "paperWidth": 6.97,
        "paperHeight": 16.5,
    }

    def __init__(self, urls: List[str]):
        self.urls = urls

    def _get_pdf_from_url(self, url, *args, **kwargs):
        self.driver.get(url)
        time.sleep(0.3)  # allow the page to load, increase if needed

        print_options = self.print_options.copy()
        result = self._send_devtools(self.driver, "Page.printToPDF", print_options)
        return base64.b64decode(result["data"])

    @staticmethod
    def _send_devtools(driver, cmd, params):
        """
        Works only with chromedriver.
        Method uses cromedriver's api to pass various commands to it.
        """
        resource = (
            "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        )
        url = driver.command_executor._url + resource
        body = json.dumps({"cmd": cmd, "params": params})
        response = driver.command_executor._request("POST", url, body)
        return response.get("value")

    def _generate_pdfs(self):
        pdf_files = []

        for url in self.urls:
            result = self._get_pdf_from_url(url)
            file = BytesIO()
            file.write(result)
            pdf_files.append(file)

        return pdf_files

    def main(self) -> List[BytesIO]:
        webdriver_options = ChromeOptions()
        webdriver_options.add_argument("--headless")
        webdriver_options.add_argument("--disable-gpu")

        # 특정한 프로필로 열어야 할 경우.
        # webdriver_options.add_argument(
        #     r"--user-data-dir=C:/Users/Genie240223/AppData/Local/Google/Chrome/User Data"
        # )
        # webdriver_options.add_argument(r"--profile-directory=Profile 3")
        # webdriver_options.add_experimental_option("detach", True)

        try:
            self.driver = webdriver.Chrome(
                # service=ChromeService(ChromeDriverManager().install()),
                service=ChromeService(),
                options=webdriver_options,
            )
            result = self._generate_pdfs()
        finally:
            self.driver.close()

        return result


URL = "https://watcha.com/"
pdf_file = PdfGenerator([URL]).main()
# save pdf to file
with open("medium_site.pdf", "wb") as outfile:
    outfile.write(pdf_file[0].getbuffer())
