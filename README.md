# Selenium-Web-Scraper
Overview

This project implements an automated web scraper using Python and Selenium to extract case information and judgments from the Supreme Court of Pakistan.

The scraper collects structured metadata, downloads related PDF files, and organizes the outputs into dedicated folders. It is designed to handle multiple years and registries, ensuring comprehensive data coverage.

Features

Extraction of:

Case Title, Case Number, Case Subject

Author Judge, Status, Institution/Disposal Dates

Citations, SCCitations, and Taglines (if available)

Hearing history and fixation dates (where applicable)

Automated download of:

Petition/Appeal Memos → memopdfs/

Judgments/Orders → judgementpdfs/

Files renamed into structured formats:

memo_<CaseNo>.pdf

judgment_<CaseNo>.pdf

Preservation of file sizes for reference.

JSON outputs:

SupremeCourt_Judgments.json

SupremeCourt_CaseInfo.json

Modular code: separate scripts for Judgments and Case Information scraping.

Folder Structure

Designed for reproducibility and easy extension.

Folder Structure
