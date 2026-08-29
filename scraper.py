from playwright.sync_api import sync_playwright
from database import init_database, is_new_code, save_code
from discord_bot import send_code

URL = "https://www.ntebuild.com/codes"


def get_codes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Ouverture de NTEBuild...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_selector(
            "h2",
            timeout=30000
        )

        codes = page.locator("h2, h3").evaluate_all("""
            elements => {
                const results = [];
                let active = false;

                for (const element of elements) {
                    const text = element.textContent.trim();

                    if (
                        element.tagName === "H2" &&
                        text === "Active Codes"
                    ) {
                        active = true;
                        continue;
                    }

                    if (
                        element.tagName === "H2" &&
                        text === "Expired Codes"
                    ) {
                        break;
                    }

                    if (
                        active &&
                        element.tagName === "H3"
                    ) {
                        const code = text
                            .replace(/New/g, "")
                            .trim();

                        if (
                            code &&
                            /^[A-Za-z0-9]+$/.test(code) &&
                            code.length >= 4 &&
                            !results.includes(code)
                        ) {
                            results.push(code);
                        }
                    }
                }

                return results;
            }
        """)

        browser.close()

        return codes


if __name__ == "__main__":
    init_database()

    codes = get_codes()

    print()
    print("===== VÉRIFICATION DES CODES =====")

    new_codes = []

    for code in codes:
        if is_new_code(code):
            print(f"[NEW] Nouveau code : {code}")

            save_code(code)
            new_codes.append(code)

            try:
                send_code(code)
            except Exception as error:
                print(f"[ERROR] Impossible d'envoyer {code} sur Discord :")
                print(error)

        else:
            print(f"[OLD] Code déjà connu : {code}")

    print("===================================")
    print(f"Codes trouvés : {len(codes)}")
    print(f"Nouveaux codes : {len(new_codes)}")
