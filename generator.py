import csv
import json
import urllib.request

JOBS_CSV = "jobs.csv"
SKILLS_TXT = "skills.txt"

def loadJobs(filepath):
    jobs = []
    
    with open(filepath, 'r') as file:
        reader = csv.DictReader(f)
        for line in reader:
            jobs.append(line)
    
    return jobs

def loadSkills(filepath):
    skills = []

    with open(filepath, 'r') as file:
        for line in file:
            skills.append(line.strip())
    
    return skills

def generateResumeContent(job, skills):
    """Call the Anthropic API to generate ATS-friendly resume bullets."""
    skills_str = ", ".join(skills)

    prompt = f"""You are an expert resume writer specializing in ATS-optimized resumes.

Generate 3 strong ATS-friendly resume bullets for the following job using the format:
  Action verb + task + impact

Rules:
- Start each bullet with a strong, varied action verb (e.g. Implemented, Designed, Automated, Led, Optimized)
- Include quantifiable impact where possible (e.g. 50,000+ records, 30% faster, 3-person team)
- Naturally incorporate relevant skills from the candidate's skill set where they fit
- Keep each bullet to 1-2 lines
- Do NOT use filler phrases like "responsible for" or "helped with"

Job Title: {job.get('job_title', job.get('title', 'Unknown'))}
Company: {job.get('company', job.get('company_name', 'Unknown'))}
Required Skills: {job.get('required_skills', job.get('skills', ''))}

Candidate's Skills: {skills_str}

Respond ONLY with a JSON object in this exact format (no markdown, no extra text):
{{
  "bullets": [
    "First bullet here.",
    "Second bullet here.",
    "Third bullet here."
  ]
}}"""

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))

    raw_text = "".join(
        block.get("text", "")
        for block in data.get("content", [])
        if block.get("type") == "text"
    )

    # Strip markdown fences if present
    clean = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    parsed = json.loads(clean)
    return parsed["bullets"]


def main():
    jobs = loadJobs(JOBS_CSV)
    skills = loadSkills(SKILLS_TXT)

    try:
        bullets = generateResumeContent(jobs, skills)
        for bullet in bullets:
            print(f" • {bullet}")
    except Exception as e:
        print(f" Error: {e}")