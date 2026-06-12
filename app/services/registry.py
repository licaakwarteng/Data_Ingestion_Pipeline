# import from s3 into neon postgresql
FILES_TO_IMPORT = [
    {
        "s3_key": "raw/2026-05-28/Candidate_Pipeline.csv",
        "table": "candidate_pipeline"
    },
    {
        "s3_key": "raw/2026-05-28/Employees.csv",
        "table": "employees"
    },
    {
        "s3_key": "raw/2026-05-28/Leave_Requests.csv",
        "table": "leave_requests"
    },
    {
        "s3_key": "raw/2026-05-28/payroll.csv",
        "table": "payroll"
    },
    {
        "s3_key": "raw/2026-05-28/Performance_Reviews.csv",
        "table": "performance_reviews"
    },
    {
        "s3_key": "raw/2026-05-28/Recruitment.csv",
        "table": "recruitment"
    }
]