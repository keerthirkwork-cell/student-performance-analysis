-- ============================================================
-- STUDENT PERFORMANCE & ENGAGEMENT ANALYSIS — SQL QUERIES
-- Author: Keerthi RK | Data Analyst
-- ============================================================

-- 1. Overall Pass Rate by Subject
SELECT
    ROUND(SUM(CASE WHEN math_score >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)    AS math_pass_rate,
    ROUND(SUM(CASE WHEN reading_score >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS reading_pass_rate,
    ROUND(SUM(CASE WHEN writing_score >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS writing_pass_rate,
    ROUND(AVG((math_score + reading_score + writing_score) / 3.0), 2)                  AS overall_avg_score
FROM students;

-- 2. Impact of Test Prep on Performance
SELECT
    test_preparation_course,
    COUNT(*) AS total_students,
    ROUND(AVG(math_score), 2)    AS avg_math,
    ROUND(AVG(reading_score), 2) AS avg_reading,
    ROUND(AVG(writing_score), 2) AS avg_writing,
    ROUND(AVG((math_score + reading_score + writing_score) / 3.0), 2) AS avg_overall
FROM students
GROUP BY test_preparation_course;

-- 3. Student Performance Segments
SELECT
    CASE
        WHEN (math_score + reading_score + writing_score) / 3.0 >= 80 THEN 'High (80+)'
        WHEN (math_score + reading_score + writing_score) / 3.0 >= 60 THEN 'Medium (60-79)'
        WHEN (math_score + reading_score + writing_score) / 3.0 >= 40 THEN 'At Risk (40-59)'
        ELSE 'Critical (<40)'
    END AS performance_segment,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM students
GROUP BY performance_segment
ORDER BY MIN((math_score + reading_score + writing_score) / 3.0) DESC;

-- 4. At-Risk Students by Parental Education
SELECT
    parental_level_of_education,
    COUNT(*) AS total_students,
    SUM(CASE WHEN (math_score + reading_score + writing_score) / 3.0 < 50 THEN 1 ELSE 0 END) AS at_risk_students,
    ROUND(SUM(CASE WHEN (math_score + reading_score + writing_score) / 3.0 < 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS at_risk_rate_pct
FROM students
GROUP BY parental_level_of_education
ORDER BY at_risk_rate_pct DESC;

-- 5. Student Engagement Funnel
SELECT
    COUNT(*)                                                                           AS total_enrolled,
    SUM(CASE WHEN math_score >= 50 AND reading_score >= 50
             AND writing_score >= 50 THEN 1 ELSE 0 END)                               AS passed_all,
    ROUND(SUM(CASE WHEN math_score >= 50 AND reading_score >= 50
             AND writing_score >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)       AS pass_all_rate,
    SUM(CASE WHEN (math_score+reading_score+writing_score)/3.0 >= 80 THEN 1 ELSE 0 END) AS high_performers,
    ROUND(SUM(CASE WHEN (math_score+reading_score+writing_score)/3.0 >= 80
             THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)                               AS high_performer_rate
FROM students;

-- 6. Gender Performance Comparison
SELECT
    gender,
    ROUND(AVG(math_score), 2)    AS avg_math,
    ROUND(AVG(reading_score), 2) AS avg_reading,
    ROUND(AVG(writing_score), 2) AS avg_writing,
    COUNT(*) AS total_students
FROM students
GROUP BY gender;

-- 7. Top Performing Segments (for targeted programs)
SELECT
    test_preparation_course,
    parental_level_of_education,
    COUNT(*) AS students,
    ROUND(AVG((math_score+reading_score+writing_score)/3.0), 2) AS avg_score,
    SUM(CASE WHEN (math_score+reading_score+writing_score)/3.0 >= 80 THEN 1 ELSE 0 END) AS high_performers
FROM students
GROUP BY test_preparation_course, parental_level_of_education
HAVING COUNT(*) > 20
ORDER BY avg_score DESC;
