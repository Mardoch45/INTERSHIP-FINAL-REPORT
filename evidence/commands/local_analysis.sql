-- Query a local demonstration database, not the hospital server.
SELECT full_name, job_title, department, monthly_salary_zar FROM staff ORDER BY id;
SELECT shareholder_name, share_percent, shares_held, share_class FROM shareholders ORDER BY id;
SELECT COUNT(*) AS employee_count, SUM(monthly_salary_zar) AS monthly_total_zar FROM staff;
SELECT SUM(share_percent) AS total_percent, SUM(shares_held) AS total_shares FROM shareholders;
