#                            FILE: SupremeCourt_Judgments.py
#                                           Sarim Rasheed
#                                              22i-1280



import os
import re
import json
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.supremecourt.gov.pk/judgement-search/"
OUTPUT_JSON = "SupremeCourt_Judgments.json"
JUDGMENTS_DIR = Path("judgementpdfs")
JUDGMENTS_DIR.mkdir(exist_ok=True)

TEST_LIMIT =10 


XPATH_SEARCH_BTN = "//*[@id='post-71968']/div[5]/div[5]/div/div[3]/div/div/div/div/input"
XPATH_TABLE_ROWS = "//*[@id='historyBody']/tr"
XPATH_NEXT_PAGE = "//*[@id='resultsTable_next']/a"




def setup_driver():

    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,1000")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)
    return driver




def safe_filename(case_no: str) -> str:

    return re.sub(r"[^\w\-]+", "_", case_no.strip())





def download_file(url: str, out_path: Path) -> str:


    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                if chunk:
                    f.write(chunk)
        size_bytes = out_path.stat().st_size
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes // 1024} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    except Exception as e:
        print(f"[Download Failed] {url} → {e}")
        return "0 KB"







def scrape_judgments():



    driver = setup_driver()
    results = []

    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_SEARCH_BTN)))

        # Click Search button
        search_btn = driver.find_element(By.XPATH, XPATH_SEARCH_BTN)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_btn)
        search_btn.click()
        time.sleep(2)

        sr_no = 1
        page = 1

        while True:
            print(f"[Page {page}] Collecting rows...")
            rows = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, XPATH_TABLE_ROWS))
            )





            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if not cols or len(cols) < 9:
                    continue

                case_subject = cols[1].text.strip()
                case_no = cols[2].text.strip()
                case_title = cols[3].text.strip()
                author_judge = cols[4].text.strip()
                upload_date = cols[5].text.strip()
                judgment_date = cols[6].text.strip()
                citations = cols[7].text.strip()
                sc_citations = cols[8].text.strip()
                tagline = cols[9].text.strip() if len(cols) > 9 and cols[9].text.strip() else "N/A"

       
                if not case_no or case_no == "N/A":
                    continue




                pdf_link = ""
                try:
                    link = cols[-1].find_element(By.TAG_NAME, "a")
                    pdf_link = link.get_attribute("href")
                except:
                    pass





                file_size = "0 KB"
                local_path = "N/A"
                if pdf_link:
                    fname = f"judgement_{safe_filename(case_no)}.pdf"
                    out_path = JUDGMENTS_DIR / fname
                    file_size = download_file(pdf_link, out_path)
                    local_path = f"judgementpdfs/{fname}"





                record = {
                    "SrNo": sr_no,
                    "CaseSubject": case_subject or "N/A",
                    "CaseNo": case_no or "N/A",
                    "CaseTitle": case_title or "N/A",
                    "AuthorJudge": author_judge or "N/A",
                    "UploadDate": upload_date or "N/A",
                    "JudgmentDate": judgment_date or "N/A",
                    "Citations": citations or "N/A",
                    "SCCitations": sc_citations or "N/A",
                    "Download": local_path,
                    "FileSize": file_size,
                    "Tagline": tagline
                }






                results.append(record)
                sr_no += 1




                if TEST_LIMIT and sr_no > TEST_LIMIT:
                    print("[Info] Test limit reached.")
                    return results

        



            try:
                next_btn = driver.find_element(By.XPATH, XPATH_NEXT_PAGE)
                if "disabled" in next_btn.get_attribute("class"):
                    print("[Info] No more pages.")
                    break
                next_btn.click()
                page += 1
                time.sleep(2)
            except:
                print("[Info] Next button not found, stopping.")
                break

    finally:
        driver.quit()

    return results







if __name__ == "__main__":
    judgments = scrape_judgments()
    payload = {"Judgments": judgments}

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(judgments)} judgments → {OUTPUT_JSON}")
