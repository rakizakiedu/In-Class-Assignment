from pathlib import Path
from bs4 import BeautifulSoup as bs
import csv

listings = Path("listings/")
job_listings = [
]

for listing in listings.iterdir():
    if listing.is_file():
        with listing.open(encoding="utf-8") as html_file:
            content = html_file.read()
            soup = bs(content, 'html.parser')

            skill_list = soup.find("ul", "skills")
            company_name = soup.find("div", "company").string
            job_title = soup.find("h1").string
            job_skills = []

            for skill in skill_list.children:
                skill_string = skill.string.strip()
                if len(skill_string) > 0:
                    job_skills.append(skill_string)

            job_listings.append(
                (
                    company_name,
                    job_title,
                    ";".join(job_skills)
                )
            )

with open("jobs.csv", "wt") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(["company_name", "job_title", "job_skills"])
    writer.writerows(job_listings)
