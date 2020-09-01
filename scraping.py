import re

from requests_html import HTMLSession

def main():
    session  = HTMLSession()
    response = session.get('***')

    response.html.render()

    rows = response.html.find('***')

    for row in rows:
        # r = re.search('[0-9]{5}', row.full_text)
        print(row.html) # TODO: delete before commit

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
