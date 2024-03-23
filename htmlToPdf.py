from glob import glob

import pdfkit
import os
import re

def files_get_ready(folder_path='data\\src_file\\*.html', res_path='data\\convert\\'):
    """# 특정 폴더의 파일명의 특수문자등을 없애 다루기 편하도록 변경하는 함수.

    Args:
        folder_path (str, optional): 원본파일이 있는 폴더. Defaults to 'data\src_file\*.html'.
        res_path (str, optional): 변환파일 저장폴더. Defaults to 'data\convert\'.
    """
    files = glob(folder_path)
    for file in files:
        src = file.split('.')[0]
        src = src[11:]
        src = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", src)
        src = src.replace(" ", "_")
        src = src.replace("__", "_")
        res = res_path+src+'.html'
        os.rename(file, res)

def convert_pdfs(src_path, pdf_path):
    try:
        PATH_EXE = r'D:\Devn_env\util\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=PATH_EXE)
        
        # files = os.listdir(src_path)
        files = glob(src_path)
        for file in files:
            print(file)
            _pdf_path = os.path.join(pdf_path, file.split('.')[0] + '.pdf') 
            pdfkit.from_file(file, _pdf_path, configuration=config) # from_url, from_file
        print(f"PDF generated and saved at {pdf_path}")
        
    except Exception as e:
        print(f"PDF generation failed: {e}")

def convert_pdf(src_path, pdf_path):
    try:
        PATH_EXE = r'D:\Devn_env\util\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=PATH_EXE)
        
        with open(src_path, 'r', encoding='utf=8') as file:
            html_content = file.read()
        pdfkit.from_string(html_content, pdf_path, configuration=config) # from_url, from_file
        print(f"PDF generated and saved at {pdf_path}")
    except Exception as e:
        print(f"PDF generation failed: {e}")


from pyhtml2pdf import converter
def convert_pdfs02(file_path):
    file_list = glob(file_path+'*.html')
    # print(file_list)
    try:
        for file in file_list[:1]:
            src_file = file
            dst_file = file.split('.')[0]+'.pdf'
            converter.convert(src_file, dst_file, compress=True)
    except Exception as e:
        print(f"PDF generation failed: {e}")



# 망할... 다들 뭔가뭔가 이유가 있어서 복잡한 html은 실행이 안된다. 
# folder_path = r'D:\Devn_src\streamlit\data\convert\\'
# print(folder_path)
# convert_pdfs02(folder_path)
# # files = os.listdir(folder_path)

