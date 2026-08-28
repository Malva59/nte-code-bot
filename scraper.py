import requests
from bs4 import BeautifulSoup

URL = "https://www.ntebuild.com/codes"


def get_codes():
    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    codes = []

    # Recherche des codes dans la section Active Codes
    active_section = soup.find(
        string=lambda text: text and "Active Codes" in text
    )

    if active_section:
        section = active_section.parent

        for element in section.find_all_next():
            text = element.get_text(strip=True)

            if text:
                codes.append(text)

    return codes


if __name__ == "__main__":
    codes = get_codes()

    print("Codes trouvés :")
    for code in codes:
        print(code)
