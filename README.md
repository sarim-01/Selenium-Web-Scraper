# Web Scraper Using Natural Language Processing

## Overview
This project is a Python-based web scraper built with **Selenium** and **Requests** to extract **case judgments** and **case information** from the official website of the Supreme Court of Pakistan.  
The scrapers collect structured metadata, download related PDF files, and save the results into JSON format.  

Two modules are included:  
- `SupremeCourt_Judgments.py` – Extracts judgments (1980–2025).  
- `SupremeCourt_CaseInfo.py` – Extracts case information by Year × Registry combinations.  

Outputs include:  
- `SupremeCourt_Judgments.json`  
- `SupremeCourt_CaseInfo.json`  
- PDF files saved into `judgementpdfs/` and `memopdfs/`.

---

## Tools Used
- **Python 3.x**  
- **Selenium WebDriver** – browser automation for scraping  
- **WebDriver Manager** – manages ChromeDriver automatically  
- **Requests** – file download handling  
- **JSON** – structured data storage  
- **OS / Pathlib** – file and directory management  

---

## Steps Followed
1. **Judgment Scraper**
   - Navigated to the [Judgment Search page](https://www.supremecourt.gov.pk/judgement-search/).
   - Triggered the search to load all judgments.
   - Iterated through all result pages using the “Next” navigation.
   - Extracted metadata fields:
     - Case Subject, Case No, Case Title, Author Judge, Upload Date, Judgment Date, Citations, SCCitations, Tagline (if available).
   - Downloaded judgment PDFs into `judgementpdfs/` and saved metadata in `SupremeCourt_Judgments.json`.

2. **Case Information Scraper**
   - Navigated to the [Case Information page](https://scp.gov.pk/OnlineCaseInformation.aspx).
   - Selected **Year (1980–2025)** and **Registry** combinations.
   - Parsed the results table and followed “View Details” links for each case.
   - Extracted metadata fields:
     - Case Title, Case No, Status, Institution Date, Disposal Date, Advocates, Judges (from history), Fixation Dates, List Type, Location.
   - Downloaded petition/appeal memos into `memopdfs/` and any linked judgments into `judgementpdfs/`.
   - Saved metadata in `SupremeCourt_CaseInfo.json`.

---

## Issues Faced
- **StaleElementReferenceException**  
  Occurred when navigating pages; resolved by re-fetching elements after each page load.  

- **404 Errors on PDFs**  
  Some links returned missing files; handled gracefully by skipping and logging the error.  

- **Large Dataset (~3326+ cases)**  
  Required handling of pagination and longer execution times; mitigated with waits and structured loops.  

- **Optional Fields Missing**  
  Some records lacked taglines or advocates; defaulted to `"N/A"` for consistency.  

---

## Outputs
- `SupremeCourt_Judgments.json` – approximately 3,300 judgment records with PDFs.  
- `SupremeCourt_CaseInfo.json` – complete Year × Registry dataset with case metadata and documents.  
- Folders:
  - `judgementpdfs/` – judgment files  
  - `memopdfs/` – memo files  

---

## License
This project is licensed under the **MIT License**.  
