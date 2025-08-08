from playwright.sync_api import sync_playwright
from config import HEADLESS
import logging

logging.basicConfig(filename="logs/error_log.txt", level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run(profile):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            context = browser.new_context()
            context.clear_cookies()
            page = context.new_page()

            print("🌐 Navigating to optoutprescreen.com...")
            page.goto("https://www.optoutprescreen.com/", timeout=60000)

            try:
                modal_btn = page.locator("#modalContinueBtn")
                if modal_btn.is_visible():
                    print("🔁 Clicking modal 'Continue Session' button...")
                    modal_btn.click()
                    page.wait_for_timeout(2000)
            except Exception:
                print("✅ Modal not found or already handled.")

            real_btn = page.locator("a[href*='optIn']").first
            if real_btn:
                print("▶️ Clicking the Opt-In start button...")
                real_btn.click()
                page.wait_for_url("**", timeout=60000)
            else:
                print("❌ Opt-In button not found.")
                return

            print("✅ Selecting 'Opt-In' radio option...")
            page.check("#optIn")

            print("⏭️ Clicking Continue after Opt-In selection...")
            page.locator("button.primaryBtn:not(#modalContinueBtn)").first.click()
            page.wait_for_url("**", timeout=60000)

            print("✍️ Filling out personal information...")
            page.fill("#opt_fname", profile["first_name"])
            page.fill("#opt_mname", profile["middle_name"])
            page.fill("#opt_lname", profile["last_name"])
            page.fill("#ssn_1", profile["ssn_1"])
            page.fill("#ssn_2", profile["ssn_2"])
            page.fill("#ssn_3", profile["ssn_3"])
            page.fill("#datepicker", profile["dob"])
            page.fill("#opt_street", profile["street"])
            page.fill("#opt_city", profile["city"])
            page.fill("#opt_zip", profile["zip"])
            page.fill("#phone", profile["phone"])

            print("\n🔒 CAPTCHA detected — solve it manually in the browser...")
            input("➡️ Press [ENTER] after completing the CAPTCHA...")

            print("🚀 Submitting the form...")
            page.locator("button.primaryBtn:not(#modalContinueBtn)").first.click()
            page.wait_for_url("**", timeout=60000)

            print("✅ Form submitted successfully.")
            browser.close()

    except Exception as e:
        logging.error(str(e))
        print("❌ An error occurred. See 'logs/error_log.txt' for details.")
