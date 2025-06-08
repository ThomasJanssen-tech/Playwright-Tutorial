import agentql
from playwright.sync_api import sync_playwright
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def scrape_agentql(playwright):

    page_nr = 0

    #initiate the browser
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir="C:\playwright",
        channel="chrome",
        headless=False,
        no_viewport=True,
    )

    data = []

    page = agentql.wrap(browser.new_page())

    page.goto("https://www.costco.com/candy.html")



    while page_nr <= 4:


        page.goto("https://www.costco.com/candy.html?currentPage="+str(page_nr)+"&pageSize=24")

        # use your own words to describe what you're looking for
        QUERY = """
        {
            products[] {
                title
                price
            }
        }
        """

        # query_data returns data from the page
        response = page.query_data(QUERY)


        for product in response['products']:
            data.append(product)

        page_nr += 1

    return data



with sync_playwright() as playwright:
    products = scrape_agentql(playwright)

    df = pd.DataFrame(products)
    df.to_excel("agentql_products.xlsx",index=False)