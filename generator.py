import csv
import json

JOBS_CSV = "jobs.csv"
SKILLS_TXT = "skills.txt"

def loadJobs(filepath):
    jobs = []
    
    with open('filepath', 'r') as file:
        reader = csv.DictReader(f)
        for line in reader:
            jobs.append(line)
    
    return jobs

def loadSkills(filepath):
    skills = []

    with open('skills.txt', 'r') as file:
        for line in file:
            skills.append(line.strip())
    
    return skills

def main():
    print("hello")