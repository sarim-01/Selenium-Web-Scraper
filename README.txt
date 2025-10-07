# Supreme Court of Pakistan – Data Extraction Project
Course: NLP – Assignment 1  
Roll No: 22i-1280  
Group: G4  
Student: Sarim Rasheed  

-------------------------------------------------------
Project Overview
-------------------------------------------------------
This project extracts structured case data from the Supreme Court of Pakistan website.  
Two main sources were used:

1. Case Judgments (SupremeCourt_Judgments.py)  
   - Extracts all judgments (1980–2025).  
   - Saves metadata (case subject, case no, title, judge, dates, citations, tagline).  
   - Downloads PDF files into judgementpdfs/ with naming convention:  
     judgment_<CaseNo>.pdf.  

2. Case Information (SupremeCourt_CaseInfo.py)  
   - Iterates over Year × Registry combinations.  
   - Collects case details, citations, status, judges, and memo files.  
   - Saves petition/appeal memos into memopdfs/ with naming convention:  
     memo_<CaseNo>.pdf.  

Both scripts output JSON files (SupremeCourt_Judgments.json and SupremeCourt_CaseInfo.json) following the required sample structure.  

-------------------------------------------------------
Folder Structure
-------------------------------------------------------
SupremeCourt_22i-1280/  
├── code/  
│   ├── SupremeCourt_Judgments.py  
│   ├── SupremeCourt_CaseInfo.py  
├── data/  
│   ├── SupremeCourt_Judgments.json  
│   ├── SupremeCourt_CaseInfo.json  
├── judgementpdfs/  
│   └── judgment_<CaseNo>.pdf  
├── memopdfs/  
│   └── memo_<CaseNo>.pdf  
├── README.txt  

-------------------------------------------------------
Tools & Libraries
-------------------------------------------------------
- Python 3.13  
- Selenium WebDriver (Chrome)  
- WebDriver Manager (auto-handles ChromeDriver)  
- Requests (for downloading PDFs)  
- JSON (data storage)  
- OS / Pathlib (file handling)  

-------------------------------------------------------
Process Description
-------------------------------------------------------
1. Judgments Scraper  
   - Opens Judgment Search page.  
   - Clicks search to load the complete table.  
   - Iterates all pages using “Next” navigation.  
   - Extracts metadata and downloads PDF files.  

2. Case Info Scraper  
   - Opens Case Information page.  
   - Selects Year (1980–2025) and Registry.  
   - Submits query and parses the case table.  
   - Extracts metadata and downloads memo/judgment files.  

-------------------------------------------------------
Challenges Encountered
-------------------------------------------------------
- StaleElementReferenceException: resolved by re-fetching rows after each page load.  
- 404 Errors on PDFs: some links were broken; handled gracefully.  
- Large Dataset (~3326+ cases): required careful pagination and waiting logic.  
- Optional Tagline: missing in some rows; defaulted to "N/A".  

-------------------------------------------------------
Output
-------------------------------------------------------
- SupremeCourt_Judgments.json: approximately 3326 records of case judgments.  
- SupremeCourt_CaseInfo.json: complete Year × Registry combinations.  
- All PDFs saved in structured folders with preserved file sizes.  

-------------------------------------------------------
Naming Conventions
-------------------------------------------------------
- Judgments: judgementpdfs/judgment_<CaseNo>.pdf  
- Memos: memopdfs/memo_<CaseNo>.pdf  
- JSON: SupremeCourt_<RollNo>.json  

-------------------------------------------------------
Bonus
-------------------------------------------------------
Compared to the provided sample JSONs, the following additional metadata has been extracted:

Judgments JSON:  
- SrNo: Serial number of each record.  
- FileSize: Human-readable PDF size (KB/MB).  
- Tagline: Optional tagline preserved when available.  

Case Info JSON:  
- Detailed Judges list extracted from hearing history.  
- ListType and Location preserved from the hearing history.  
- Consistent structure for memo/judgment files with download links.  

These enhancements provide additional clarity, traceability, and completeness.  

-------------------------------------------------------
Conclusion
-------------------------------------------------------
The project successfully extracts, downloads, and organizes Supreme Court case data.  
Both Judgments and Case Information parts are completed as per assignment requirements, with additional metadata included for bonus marks.  
