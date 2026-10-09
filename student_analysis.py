import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# =====================================

# 1. CONNECT TO MYSQL

# =====================================

db = mysql.connector.connect(
host="localhost",
user="root",
password="sakthi@123",
database="student_result_analysis"
)

print("MySQL connected successfully!")

# =====================================

# 2. FETCH STUDENT RESULTS

# =====================================

query = """
SELECT
students.student_id,
students.student_name,
students.department,
subjects.subject_name,
marks.internal_marks,
marks.external_marks,
marks.internal_marks + marks.external_marks AS total_marks
FROM students
JOIN marks
ON students.student_id = marks.student_id
JOIN subjects
ON marks.subject_id = subjects.subject_id
"""

df = pd.read_sql(query, db)

db.close()

# =====================================

# 3. DISPLAY STUDENT RESULTS

# =====================================

print("\n========== STUDENT RESULTS ==========\n")
print(df.to_string(index=False))

# =====================================

# 4. CALCULATE AVERAGE MARKS

# =====================================

student_avg = (
df.groupby(["student_id", "student_name"])["total_marks"]
.mean()
.sort_values(ascending=False)
)

print("\n========== STUDENT AVERAGE MARKS ==========\n")
print(student_avg)

# =====================================

# 5. PASS / FAIL ANALYSIS

# =====================================

pass_count = (df["total_marks"] >= 50).sum()
fail_count = (df["total_marks"] < 50).sum()

print("\n========== PASS / FAIL ANALYSIS ==========")
print("Passed subject results:", pass_count)
print("Failed subject results:", fail_count)

# =====================================

# 6. DEPARTMENT PERFORMANCE

# =====================================

department_avg = (
df.groupby("department")["total_marks"]
.mean()
.sort_values(ascending=False)
)

print("\n========== DEPARTMENT PERFORMANCE ==========\n")
print(department_avg)

# =====================================

# 7. CREATE DASHBOARD CHARTS

# =====================================

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Chart 1: Student Average Marks

student_avg.plot(kind="bar", ax=axes[0])

axes[0].set_title("Student Average Marks")
axes[0].set_xlabel("Student ID and Name")
axes[0].set_ylabel("Average Marks")
axes[0].tick_params(axis="x", rotation=90)

# Chart 2: Pass / Fail Analysis

axes[1].bar(
["Pass", "Fail"],
[pass_count, fail_count]
)

axes[1].set_title("Pass / Fail Analysis")
axes[1].set_xlabel("Result")
axes[1].set_ylabel("Number of Subject Results")

# Chart 3: Department Performance

department_avg.plot(kind="bar", ax=axes[2])

axes[2].set_title("Department-wise Average Marks")
axes[2].set_xlabel("Department")
axes[2].set_ylabel("Average Marks")
axes[2].tick_params(axis="x", rotation=45)

# Display all charts

plt.tight_layout()
plt.show()

print("\nDashboard completed successfully!")
