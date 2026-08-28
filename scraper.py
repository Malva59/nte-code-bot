from playwright.sync_api import sync_playwright

URL = "https://www.ntebuild.com/codes"


def get_codes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Ouverture de NTEBuild...")
        page.goto(URL, wait_until="networkidle")

        codes = page.locator("h2").evaluate("""
        headings => {
            const activeHeading = headings.find(
                h => h.textContent.trim() === "Active Codes"
            );

            if (!activeHeading) {
                return [];
            }

            const results = [];
            let element = activeHeading.nextElementSibling;

            while (element) {
                if (
                    element.tagName === "H2" &&
                    element.textContent.includes("Expired Codes")
                ) {
                    break;
                }

                if (element.tagName === "H3") {
                    const code = element.textContent
                        .replace(/New/g, "")
                        .trim();

                    if (code) {
                        results.push(code);
                    }
                }

                const innerHeadings = element.querySelectorAll("h3");

                for (const heading of innerHeadings) {
                    const code = heading.textContent
                        .replace(/New/g, "")
                        .trim();

                    if (code && !results.includes(code)) {
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
