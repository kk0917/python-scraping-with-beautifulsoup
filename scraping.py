import os
import re
import zipfile

from datetime import datetime
import requests
from requests_html import HTMLSession

TARGET_URL    = 'https://...'
DOWNLOAD_PATH = os.getcwd() + '/downloads/zip/'
CSV_FILE_PATH = os.getcwd() + '/downloads/csv/'
ZIP_FILE_NAME = 'diff_csv_unicode_{}_' + datetime.now().strftime("%Y%m%d_%H%M%S" + '.zip') # insert file num to {} when download files

# requests.post parameters defaul config
payload = {
    'event': 'download',
    'selDlFileNo': 0
}

def scrape_target_tag():
    session  = HTMLSession()
    response = session.get(TARGET_URL)

    response.html.render(wait=30)

    return response.html.find('*** set target tag like jQuery... ***')

def scrape_files_num(rows):
    files_num = []

    for row in rows:
        _row: str = row.html
        file_num   = strip_file_num(_row)

        if file_num:
            files_num.append(file_num)
        else:
            print('NoneFileNumException...')

    return files_num

def strip_file_num(row):
    """
        <a href="#" onclick="return doDownload(99999);">zip 999KB</a>
        target number is...                    ^^^^^ here!
    """
    match_obj = re.search('doDownload\([0-9]+\)', row)
    file_num   = re.search('[0-9]+', match_obj.group())

    return file_num.group() # TODO: Consider whether to raise an exception

def download_files(files_num):
    for num in files_num:
        payload['selDlFileNo'] = int(num)

        r = requests.post(TARGET_URL, data=payload)

        zip_file_name = ZIP_FILE_NAME.format(num)
        with open(DOWNLOAD_PATH + zip_file_name, 'wb') as f:
            f.write(r.content)
            f.flush()

        unzip(zip_file_name)

def unzip(zip_file_name):
    with zipfile.ZipFile(DOWNLOAD_PATH + zip_file_name, 'w') as diff_zip:
        diff_zip.extractall(CSV_FILE_PATH) # TODO: change extractall to extract method when upload date could get

def main():
    rows     = scrape_target_tag()
    files_num = scrape_files_num(rows)
    
    # TODO: get files upload date Checking if the file is already gotten

    download_files(files_num)

    # TODO: upload csv data to database

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
