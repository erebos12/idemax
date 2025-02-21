import time
from behave import when, then
from playwright.sync_api import sync_playwright


@when('opening bluconnect login page')
def launch_login_page(context):
    playwright = sync_playwright().start()
    context.browser = playwright.chromium.launch(headless=True)  # or use p.firefox.launch(headless=False) for Firefox
    context.page = context.browser.new_page()
    # TODO: take URL from env var
    context.page.goto('http://frontend:80')


@when('I enter username and password for user "{username}"')
def enter_credentials(context, username):
    try:
        context.page.wait_for_selector('input#username', state='visible')
        context.page.fill('input#username', username)
        context.page.wait_for_selector('input#password', state='visible')
        context.page.fill('input#password', 'bluconnect')
        context.page.click('input#kc-login')
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


@then('I expect to be logged in successfully and see the landing page from BluConnect')
def verify_login(context):
    try:
        context.page.wait_for_selector('div.main-content')
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
