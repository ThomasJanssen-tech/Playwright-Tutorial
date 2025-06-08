from patchright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_indeed(playwright):
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir="C:\playwright",
        channel="chrome",
        headless=False,
        no_viewport=True,
    )


    page = browser.new_page()


    page_count = 0

    jobs = []



    while page_count < 2:

        print("SCRAPING LIST ITEMS")

        time.sleep(2)

        page.goto('https://www.indeed.com/jobs?q=python+developer&start='+str(page_count * 10))

        vacancies = page.locator('.cardOutline')

        for vacancy in vacancies.element_handles():
            item = {}

            item['Title'] = vacancy.query_selector("h2").inner_text()
            item['URL'] = "https://www.indeed.com"+vacancy.query_selector("a").get_attribute("href")

            jobs.append(item)
    
        page_count += 1

    all_items = []

    for job in jobs:

        print("SCRAPING DETAILS PAGE")

        
        page.goto(job['URL'])

        time.sleep(2)

        item = {}

        item["Title"] = job['Title']
        item["URL"] = job["URL"]
        item["CompanyName"] = ""
        item["Location"] = ""
        item["Salaryinfo"] = ""

        company_name = page.get_by_test_id("inlineHeader-companyName")

        if company_name.count() > 0:  
            item["CompanyName"] = company_name.inner_text()

        company_location = page.get_by_test_id("inlineHeader-companyLocation")

        if company_location.count() > 0:  
            item["Location"] = company_location.inner_text()


        salaryinfo = page.get_by_test_id("jobsearch-OtherJobDetailsContainer")

        if(salaryinfo.count() > 0):
            item["Salaryinfo"] = salaryinfo.inner_text()


        all_items.append(item)


    browser.close()

    return all_items



with sync_playwright() as playwright:
    jobs = scrape_indeed(playwright)

    df = pd.DataFrame(jobs)
    df.to_excel("jobs.xlsx",index=False)
    