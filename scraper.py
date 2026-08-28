from playwright.sync_api import sync_playwright

URL = "https://www.ntebuild.com/codes"


def get_codes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Ouverture de NTEBuild...")
        page.goto(URL, wait_until="networkidle")

        codes = page.locator("h2").filter(has_text="Active Codes").evaluate("""
        active_heading => {
            const codes = [];
            let element = active_heading.nextElementSibling;

            while (element) {
                if (
                    element.tagName === "H2" &&
                    element.textContent.includes("Expired Codes")
                ) {
                    break;
                }

                const headings = element.querySelectorAll("h3");

                for (const heading of headings) {
                    const code = heading.textContent
                        .replace("New", "")
                        .trim();

                    if (code) {
                        codes.push(code);
                    }
                }

                element = element.nextElementSibling;
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
