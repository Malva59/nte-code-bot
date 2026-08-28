from playwright.sync_api import sync_playwright
from database import init_database, is_new_code, save_code

URL = "https://www.ntebuild.com/codes"


def get_codes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Ouverture de NTEBuild...")
        page.goto(URL, wait_until="networkidle")

        codes = page.locator("h2").evaluate_all("""
            headings => {
                const active = headings.find(
                    h => h.textContent.trim() === "Active Codes"
                );

                const expired = headings.find(
                    h => h.textContent.trim() === "Expired Codes"
                );

                if (!active || !expired) {
                    return [];
                }

                const results = [];
                let element = active.nextElementSibling;

                while (element && element !== expired) {
                    const headings = element.matches("h3")
                        ? [element]
                        : Array.from(element.querySelectorAll("h3"));

                    for (const heading of headings) {
                        const code = heading.textContent
                            .replace(/New/g, "")
                            .trim();

                        if (
                            code &&
                            /^[A-Za-z0-9]+$/.test(code) &&
                            !results.includes(code)
                        ) {
                            results.push(code);
                        }
                    }

                    element = element.nextElementSibling;
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
        else:
            print(f"[OLD] Code déjà connu : {code}")

    print("===================================")
    print(f"Codes trouvés : {len(codes)}")
    print(f"Nouveaux codes : {len(new_codes)}")
