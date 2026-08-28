from playwright.sync_api import sync_playwright

URL = "https://www.ntebuild.com/codes"


def get_codes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Ouverture de NTEBuild...")
        page.goto(URL, wait_until="networkidle")

        codes = page.locator("h3").evaluate_all("""
            elements => {
                const codes = [];

                for (const element of elements) {
                    const code = element.textContent
                        .replace(/New/g, "")
                        .trim();

                    if (code) {
                        codes.push(code);
                    }
                }

                return codes;
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
