import pandas as pd
import os

path = 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'
files = {
    'bangalore_doctors_final.csv': 'doctors',
    'healthcare_rag_dataset.csv': 'rag',
    'hospital_insights_summary.csv': 'hospitals',
    'medical_question_answer_dataset_50000.csv': 'qa',
    'patients.csv': 'patients',
    'services_weekly.csv': 'services',
    'staff.csv': 'staff',
    'staff_schedule.csv': 'schedule'
}

print("=== INSPECTING YOUR DATASETS ===\n")

for file, name in files.items():
    try:
        df = pd.read_csv(os.path.join(path, file))
        print(f'📄 {file} ({name})')
        print(f'   Rows: {len(df)}')
        print(f'   Columns: {list(df.columns)[:10]}')  # Show first 10 columns
        if len(df) > 0:
            print(f'   Sample: {df.iloc[0].to_dict()}')
        print()
    except Exception as e:
        print(f'❌ Error reading {file}: {e}\n')
