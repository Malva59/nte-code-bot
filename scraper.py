from playwright.sync_api import sync_playwright
import re

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

                        // Un code ne contient pas d'espaces
                        // et contient uniquement lettres/chiffres
                        if (
                            code &&
                            /^[A-Z0-9]+$/.test(code) &&
                            code.length >= 4 &&
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
    codes = get_codes()

    print()
    print("===== CODES NTE TROUVÉS =====")

    for code in codes:
        print(code)

    print("=============================")
    print(f"Total : {len(codes)}")
