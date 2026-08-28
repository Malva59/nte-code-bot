from playwright.sync_api import sync_playwright

URL = "https://www.ntebuild.com/codes"


def get_codes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Ouverture de NTEBuild...")
        page.goto(URL, wait_until="networkidle")

        codes = page.locator("h2, h3").evaluate_all("""
            elements => {
                const results = [];
                let active = false;

                for (const element of elements) {
                    const text = element.textContent.trim();

                    // Début de la section des codes actifs
                    if (
                        element.tagName === "H2" &&
                        text === "Active Codes"
                    ) {
                        active = true;
                        continue;
                    }

                    // Fin de la section des codes actifs
                    if (
                        element.tagName === "H2" &&
                        text === "Expired Codes"
                    ) {
                        break;
                    }

                    // Récupération uniquement des H3 de la section Active Codes
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
    codes = get_codes()

    print()
    print("===== CODES NTE TROUVÉS =====")

    for code in codes:
        print(code)

    print("=============================")
    print(f"Total : {len(codes)}")
