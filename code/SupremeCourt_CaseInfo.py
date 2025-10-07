#                            FILE: SupremeCourt_Judgments_FinalClean.py
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
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



BASE_URL = "https://www.scp.gov.pk/OnlineCaseInformation.aspx"
OUTPUT_JSON = "SupremeCourt_CaseInfo.json"




MEMO_DIR = Path("memopdfs")
JUDGMENT_DIR = Path("judgementpdfs")
MEMO_DIR.mkdir(exist_ok=True)
JUDGMENT_DIR.mkdir(exist_ok=True)



YEARS = [str(y) for y in range(1980, 2026)]
REGISTRIES = ["I", "L", "K", "Q", "P"]





def setup_driver():
    options = Options()
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









def caseinfo():


    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    results = []

    try:
        driver.get(BASE_URL)

        for year in YEARS:
            for registry in REGISTRIES:
                print(f"\n🔍 Searching Year={year}, Registry={registry}")



                try:
                    Select(wait.until(EC.presence_of_element_located((By.ID, "ddlYear")))).select_by_value(year)
                    Select(wait.until(EC.presence_of_element_located((By.ID, "ddlRegistry")))).select_by_value(registry)
                except:
                    print(f"Could not select Year={year}, Registry={registry}")
                    continue




                try:
                    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSearch")))
                    search_btn.click()
                    time.sleep(2)
                except:
                    print("Search button not clickable")
                    continue




                while True:
                    try:
                        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='gvCases']/tbody/tr")))
                    except:
                        print("No results for this combo")
                        break

                    

                    for i in range(1, len(rows)):


                        try:


                            rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='gvCases']/tbody/tr")))
                            row = rows[i]

                            cols = row.find_elements(By.TAG_NAME, "td")
                            if not cols:
                                continue

                            case_no = cols[0].text.strip()
                            case_title = cols[1].text.strip()
                            case_status = cols[2].text.strip()

                            detail_link = row.find_element(By.XPATH, ".//a[contains(@id,'gvCases_lnkView')]")
                            driver.execute_script("arguments[0].click();", detail_link)
                            time.sleep(2)




                            case_info = {
                                "CaseTitle": driver.find_element(By.ID, "spCaseTitle").text.strip(),
                                "CaseNo": driver.find_element(By.ID, "spCaseNo").text.strip(),
                                "Status": driver.find_element(By.ID, "spCaseStatus").text.strip(),
                                "InstitutionDate": driver.find_element(By.ID, "spInstDate").text.strip(),
                                "DisposalDate": driver.find_element(By.ID, "spDispDate").text.strip(),
                                "Judges": "",
                                "Memo": None,
                                "Judgment": None,
                                "MemoSize": "0 KB",
                                "JudgmentSize": "0 KB",
                                "Year": year,
                                "Registry": registry,
                            }




                            try:
                                hist_table = driver.find_element(By.ID, "gvJResults")
                                rows_hist = hist_table.find_elements(By.TAG_NAME, "tr")
                                judge_texts = []
                                for hr in rows_hist[1:]:
                                    tds = hr.find_elements(By.TAG_NAME, "td")
                                    if len(tds) > 1:
                                        judge_texts.append(tds[1].text.strip())
                                case_info["Judges"] = "; ".join(judge_texts)
                            except:
                                pass








                            try:
                                memo_div = driver.find_element(By.ID, "divMemo")
                                memo_link = memo_div.find_element(By.TAG_NAME, "a").get_attribute("href")
                                fname = f"memo_{safe_filename(case_no)}.pdf"
                                out_path = MEMO_DIR / fname
                                size = download_file(memo_link, out_path)
                                case_info["Memo"] = f"memopdfs/{fname}"
                                case_info["MemoSize"] = size
                            except:
                                pass





                            try:
                                hist_table = driver.find_element(By.ID, "gvJResults")
                                links = hist_table.find_elements(By.TAG_NAME, "a")
                                for link in links:
                                    href = link.get_attribute("href")
                                    if href and href.endswith(".pdf"):
                                        fname = f"judgement_{safe_filename(case_no)}.pdf"
                                        out_path = JUDGMENT_DIR / fname
                                        size = download_file(href, out_path)
                                        case_info["Judgment"] = f"judgementpdfs/{fname}"
                                        case_info["JudgmentSize"] = size
                                        break
                            except:
                                pass




                            results.append(case_info)

                            driver.back()
                            time.sleep(2)





                        except Exception as e:
                            print(f"Could not process row {i} in Year={year}, Registry={registry} → {e}")
                            continue





                    try:
                        next_btn = driver.find_element(By.LINK_TEXT, "Next")
                        driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(2)
                    except:
                        break



    finally:
        driver.quit()

    return results







if __name__ == "__main__":

    cases = caseinfo()
    payload = {"CaseInfo": cases}


    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(cases)} case info records → {OUTPUT_JSON}")
