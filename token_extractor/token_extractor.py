import time

from playwright.sync_api import sync_playwright
from common.end_points import UiEndpoints

#todo: PoM
def extract_token_from_ui(username, password):
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False
                                             )
        context = browser.new_context()
        context.tracing.start(snapshots=True, screenshots=True,sources=True)
        try:
            page = context.new_page()
            page.goto(UiEndpoints.LOGIN, wait_until="commit")
            page.get_by_label("אימייל / מספר נייד / שם משתמש").click()
            page.get_by_label("אימייל / מספר נייד / שם משתמש").fill(username)
            page.get_by_label("אימייל / מספר נייד / שם משתמש").press("Enter")
            page.wait_for_selector("#password")

            page.get_by_label("מה הסיסמה?").click()
            page.get_by_label("מה הסיסמה?").fill(password)
            page.get_by_label("מה הסיסמה?").press("Enter")
            time.sleep(2)
            storage = context.storage_state()
            auth_token = [token.get("value") for token in storage["cookies"] if token.get("name") == "token"][0]
            return auth_token

            # page.get_by_role("button", name="כניסה").click()

            context.close()
            browser.close()
            browser.stop_tracing()

        except(Exception) as e:
                context.tracing.stop(path="trace.zip")
                raise e
