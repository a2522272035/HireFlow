import subprocess
import sys

PSQL = r"D:\APP\PostgreSQL\17\bin\psql.exe"

def run(cmd, db="postgres"):
    import os
    env = os.environ.copy()
    # Try password
    env["PGPASSWORD"] = "a591192183"
    r = subprocess.run([PSQL, "-U", "postgres", "-d", db, "-c", cmd],
                       capture_output=True, text=True, env=env)
    if r.returncode == 0:
        if r.stdout.strip():
            print(f"  {r.stdout.strip()}")
        return True
    # Try second password
    env["PGPASSWORD"] = "Aa591192183."
    r = subprocess.run([PSQL, "-U", "postgres", "-d", db, "-c", cmd],
                       capture_output=True, text=True, env=env)
    if r.returncode == 0:
        if r.stdout.strip():
            print(f"  {r.stdout.strip()}")
        return True
    if r.stderr.strip():
        print(f"  ERROR: {r.stderr.strip()[:200]}")
    return False

print("=== HireFlow Database Setup ===")

# 1. Create database
print("\n[1] Creating database 'hireflow'...")
run("SELECT datname FROM pg_database WHERE datname='hireflow';")
run("CREATE DATABASE hireflow;")

# 2. Create role
print("\n[2] Creating role 'hireflow'...")
run("CREATE ROLE hireflow WITH LOGIN PASSWORD 'hireflow_dev';")
run("GRANT ALL PRIVILEGES ON DATABASE hireflow TO hireflow;")

# 3. Create tables in hireflow database
print("\n[3] Creating tables...")
run(r"""
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'interviewer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    parsed_data JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS resume_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID REFERENCES resumes(id) ON DELETE CASCADE,
    skill VARCHAR(255) NOT NULL,
    proficiency VARCHAR(50),
    years_of_experience INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS resume_experiences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID REFERENCES resumes(id) ON DELETE CASCADE,
    company VARCHAR(255),
    position VARCHAR(255),
    start_date DATE,
    end_date DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS interviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID REFERENCES resumes(id),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS interview_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID REFERENCES interviews(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    audio_file VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS policy_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS evaluation_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID REFERENCES interviews(id),
    resume_id UUID REFERENCES resumes(id),
    user_id UUID REFERENCES users(id),
    overall_score DECIMAL(5,2),
    summary TEXT,
    strengths TEXT,
    weaknesses TEXT,
    recommendation VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_interviews_resume_id ON interviews(resume_id);
CREATE INDEX IF NOT EXISTS idx_evaluation_reports_interview_id ON evaluation_reports(interview_id);
""", "hireflow")

# 4. Grant all on schema
print("\n[4] Granting permissions...")
run("GRANT ALL ON SCHEMA public TO hireflow;", "hireflow")
run("GRANT ALL ON ALL TABLES IN SCHEMA public TO hireflow;", "hireflow")
run("GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO hireflow;", "hireflow")

print("\n=== Setup Complete ===")
