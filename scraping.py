from requests_html import HTMLSession

def main():
    session = HTMLSession()
    response = session.get('***')
    response.html.render()
    rows = response.html.find('***')

    for row in rows:
        print(row.text)

if __name__ == "__main__":
    main()