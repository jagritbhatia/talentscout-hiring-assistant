import os
import pandas as pd

EXCEL_FILE = "interview_summary.xlsx"

def save_interview_to_excel(candidate_info: dict, answers: list):
    # Load existing or empty
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame()

    row = {
        "Full Name": candidate_info.get("name", ""),
        "Email": candidate_info.get("email", ""),
        "Phone": candidate_info.get("phone", ""),
        "Experience": candidate_info.get("experience", ""),
        "Position": candidate_info.get("position", ""),
        "Location": candidate_info.get("location", ""),
        "Tech Stack": ", ".join(candidate_info.get("tech_stack", [])),
    }

    # Add questions and answers columns dynamically
    for i, ans in enumerate(answers, start=1):
        row[f"Question {i}"] = ans["question"]
        row[f"Answer {i}"] = ans["answer"]

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
