from bs4 import BeautifulSoup
import os

def _content_cleaner(src_folder = 'data/convert/', dst_folder = 'data/'):
    """BeautifulSoup 패밀리인 'BeautifulSoupTransformer'와 'BSHTMLLoader'를 써줄 수도 있었지만, 
    읽어온 문서를 통째로 넣던가, bs4보다 요소 추출과정이 번거로워서, bs4를 사용.

    Args:
        src_folder (str, optional): _description_. Defaults to 'data/convert/'.
        dst_folder (str, optional): _description_. Defaults to 'data/'.

    Returns:
        None
    """
    src_list = os.listdir(src_folder)
    dst_list = os.listdir(dst_folder)

    for file in src_list:
        if file not in dst_list:
            src_path = src_folder + file
            dst_path = dst_folder + file

            with open(src_path, 'r', encoding='utf-8') as f:
                html_doc = f
                soup = BeautifulSoup(html_doc, 'html.parser')
                
            htmls = soup.find_all('div', class_='article-body')

            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(file + str(htmls[0]))
            
            count += 1        
        else: 
            continue

# ------------------------- 이름 변경 ------------------------- #
from glob import glob
import os
import re

def _name_cleaner(src_path='data\\src_file\\*.html', dst_path='data\\convert\\'):
    """
    특정 폴더의 파일명의 특수문자등을 없애 다루기 편하도록 변경하는 함수.
    - 함수의 위치에 따른 상대경로를 잘 따져서 path를 넣을 것.
    - 작업이 완료되면 src 폴더는 비게 된다.

    Args:
        src_path (str, optional): 원본파일이 있는 폴더. Defaults to 'data\src_file\*.html'.
        res_path (str, optional): 변환파일 저장폴더. Defaults to 'data\convert\'.
    """
    # ['../data/src_file\\AI 고수의 팁_ 6가지 사례로 보는 제미나이 프롬프트 작성 가이드 (+프롬프트 10종 제공) - PUBLY.html',
    try:
        files = glob(src_path+'*.html')
        # print(files)
        for file in files:
            src = file[len(src_path):]
            src = src.split('.html')[0]
            src = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", src)
            src = src.replace(" ", "_")
            src = src.replace("__", "_")
            dst = dst_path+src+'.html'
            os.rename(file, dst)
    except Exception as e:
        print(e)


import pdfkit

def _convert_pdfs(html_path='../data/convert/', pdf_path='../data/pdf/'):
    try:
        count = 0
        PATH_EXE = 'D:\Devn_env\\util\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=PATH_EXE)

        files = glob(html_path+'*.html')
        for file in files:
            file_name = file[len(html_path):].split('.html')[0]
            _pdf_path = pdf_path + file_name +'.pdf'
            print(file_name)
            print(_pdf_path)
            pdfkit.from_file(file, _pdf_path, configuration=config, verbose=False) # from_url, from_file
        print(f"{count} of PDF generated and saved at {pdf_path}")

    except Exception as e:
        print(f"PDF generation failed: {e}")

def main():
    _name_cleaner()
    _content_cleaner()
    _convert_pdfs()

if __name__ == '__main__':
    main()