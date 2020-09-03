import re

from requests_html import HTMLSession

TARGET_URL = 'https://***'

def scrape_target_tag():
    session  = HTMLSession()
    response = session.get(TARGET_URL)

    response.html.render(wait=30)

    return response.html.find('***')

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
    match_obj = re.search('[0-9]{5}', row)

    return int(match_obj.group()) # TODO: Consider whether to raise an exception

def download_files(files_num):
    return files_num

def main():
    rows     = scrape_target_tag()
    files_num = scrape_files_num(rows)

    return files_num

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
