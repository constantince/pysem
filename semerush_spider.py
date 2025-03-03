from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import time
import pandas as pd


def run(playwright: Playwright, url) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.semrush.fun/index")
    page.get_by_role("textbox", name="账号").click()
    page.get_by_role("textbox", name="账号").fill("ohyeah")
    page.get_by_role("textbox", name="登录密码").click()
    page.get_by_role("textbox", name="登录密码").fill("LWj10233201")
    page.get_by_role("button", name="登录").click()
    count = 0
    while count <= 10:
        try:
            with page.expect_popup() as page1_info:
                page.get_by_role("link", name="guru中文线路二").click()
            break
        except:
            time.sleep(10)
            count += 1
    page1 = page1_info.value
    page2 = context.new_page()
    count = 0
    while count <= 10:
        try:
            # url = f'https://vip3.semrush.fun/analytics/overview/?searchType=domain&q=worldwildlife.org'
            page2.goto(f"https://vip3.semrush.fun/analytics/overview/?q={url}&searchType=domain")
            break
        except:
            time.sleep(10)
            count += 1
    time.sleep(5)
    soup = BeautifulSoup(page2.content(), 'lxml')
    try:
        div = soup.find_all('div', class_='___SRow_a2h7d-red-team')[1]
        country = div.find('span', class_='___SText_d7yy4-red-team _size_200_d7yy4-red-team').get_text()
        num = div.find('span', class_='___SText_pr68d-red-team').get_text()
    except:
        country = ''
        num = 0
    count = 0
    while count <= 10:
        try:

            page2.goto(f"https://vip3.semrush.fun/analytics/organic/overview/?q={url}&searchType=domain")
            break
        except:
            time.sleep(10)
            count += 1
    time.sleep(5)
    soup = BeautifulSoup(page2.content(), 'lxml')
    try:
        divs = \
        soup.find_all('div', class_='_use_secondary_a2h7d-red-team __use_a2h7d-red-team ___SBody_a2h7d-red-team')[1]
        shangwu = divs.find_all('div', class_='___SRow_a2h7d-red-team')[2].find('span',
                                                                                class_='___SText_pr68d-red-team').get_text()
        jiaoyi = divs.find_all('div', class_='___SRow_a2h7d-red-team')[3].find('span',
                                                                               class_='___SText_pr68d-red-team').get_text()
        page2.get_by_role("radio", name="自然搜索").click()
        page2.get_by_label("主要关键词").get_by_label("打开完整的 关键词 报告").click()
        time.sleep(2)
        soup = BeautifulSoup(page2.content(), 'lxml')
        tables = soup.select('#cl-position-table > div.___SBodyWrapper_a2h7d-red-team > div')[0]
        h3s = tables.find_all('h3')[: 5]
        keyword = ''
        catalogy = ''
        for h3 in h3s:
            cata_str = ''
            a = h3.find('a', class_='___SBoxInline_cv2w1-red-team ___SLink_pr68d-red-team __inline_pr68d-red-team '
                                    '___SText_d7yy4-red-team _size_200_d7yy4-red-team __lineHeight_d7yy4-red-team')
            keyword += a.find('span', class_='___SText_pr68d-red-team').get_text() + ';'
            for span in h3.find_all('span', {'data-ui-name': "Text"}):
                cata_str += span.get_text() + ' '
            catalogy += cata_str + ';'
        with open('result.txt', 'a+') as f:
            print(url, str(country), str(num), shangwu, jiaoyi, keyword, catalogy)
            f.write(url + '$' + str(country) + '$' + str(num) + '$' + str(shangwu) + '$' + str(
                jiaoyi) + '$' + keyword + '$' + catalogy + '\n')
        page2.get_by_label("选择关键词意图").click()
        page2.get_by_role("option", name="商务").locator("div").first.click()
        page2.get_by_role("option", name="交易").locator("div").first.click()
        page2.get_by_role("button", name="应用").click()
        url2 = url.replace('https://', '').replace('/', '')
        download_path = f'keywords/{url2}_keyword.xlsx'
        with page2.expect_download() as download_info:
            page2.get_by_label("导出排名变化数据").click(timeout=100000)
            page2.get_by_role("button", name="Excel").click(timeout=100000)
        download = download_info.value
        download.save_as(download_path)
        page2.close()
        page1.close()
        page.close()
    except Exception as e:
        print(e)
        page2.close()
        page1.close()
        page.close()

    # ---------------------
    context.close()
    browser.close()


if __name__ == '__main__':
    df = pd.read_excel('服装品牌.xlsx')
    urls = df['url'].tolist()
    for url in urls:
        time.sleep(1)
        print(f'https://zh01.semrush.fun/analytics/overview/?q={url}&protocol=https&searchType=domain')
        with sync_playwright() as playwright:
            run(playwright, url)
    # with sync_playwright() as playwright:
    #     run(playwright, 'http://au.shopcsb.com')
