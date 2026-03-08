# ============================================================
# STUDENT PERFORMANCE & ENGAGEMENT ANALYSIS
# Author: Keerthi RK | Data Analyst
# Tools: Python (Pandas, Matplotlib, Seaborn)
# Context: Mirrors real-world EdTech / Test Prep analytics
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Style ────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor':   '#161b22',
    'axes.edgecolor':   '#30363d',
    'axes.labelcolor':  '#c9d1d9',
    'xtick.color':      '#8b949e',
    'ytick.color':      '#8b949e',
    'text.color':       '#c9d1d9',
    'grid.color':       '#21262d',
    'grid.linestyle':   '--',
    'font.family':      'DejaVu Sans',
})
BLUE   = '#38bdf8'
ORANGE = '#f97316'
GREEN  = '#4ade80'
PURPLE = '#a78bfa'
RED    = '#f87171'
YELLOW = '#fbbf24'

# ── Load Data ────────────────────────────────────────────────
df = pd.read_csv('project2/exams.csv')

# Feature Engineering
df['avg_score']       = df[['math score','reading score','writing score']].mean(axis=1).round(1)
df['completed_prep']  = (df['test preparation course'] == 'completed').astype(int)
df['pass_math']       = (df['math score'] >= 50).astype(int)
df['pass_reading']    = (df['reading score'] >= 50).astype(int)
df['pass_writing']    = (df['writing score'] >= 50).astype(int)
df['pass_all']        = ((df['pass_math']==1) & (df['pass_reading']==1) & (df['pass_writing']==1)).astype(int)

# Performance segments
def segment(score):
    if score >= 80: return 'High (80+)'
    elif score >= 60: return 'Medium (60-79)'
    elif score >= 40: return 'At Risk (40-59)'
    else: return 'Critical (<40)'

df['performance_segment'] = df['avg_score'].apply(segment)

print(f"Dataset: {len(df):,} students")
print(f"Completed test prep: {df['completed_prep'].sum()} ({df['completed_prep'].mean()*100:.1f}%)")
print(f"Pass all subjects: {df['pass_all'].sum()} ({df['pass_all'].mean()*100:.1f}%)")

# ════════════════════════════════════════════════════════════
# FIGURE 1 — EXECUTIVE DASHBOARD
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Student Performance & Engagement — Executive Dashboard',
             fontsize=20, fontweight='bold', color='white', y=0.98)

# ── Chart 1: Test Prep Completion (Donut) ────────────────────
ax1 = axes[0, 0]
prep_counts = df['test preparation course'].value_counts()
colors = [GREEN, RED]
wedges, texts, autotexts = ax1.pie(
    prep_counts, labels=None, autopct='%1.1f%%',
    colors=colors, startangle=90,
    wedgeprops=dict(width=0.55, edgecolor='#0d1117', linewidth=2),
    pctdistance=0.75
)
for at in autotexts:
    at.set_color('white'); at.set_fontsize(13); at.set_fontweight('bold')
ax1.set_title('Test Prep Course Completion', fontsize=13, fontweight='bold', color='white', pad=15)
ax1.legend(['Completed', 'Not Completed'], loc='lower center',
           bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=False, labelcolor='white', fontsize=11)
ax1.text(0, 0, f"33.5%\nCompleted", ha='center', va='center',
         fontsize=12, fontweight='bold', color=GREEN)

# ── Chart 2: Avg Score by Test Prep ──────────────────────────
ax2 = axes[0, 1]
prep_scores = df.groupby('test preparation course')[['math score','reading score','writing score']].mean()
x = np.arange(3)
width = 0.35
subjects = ['Math', 'Reading', 'Writing']
b1 = ax2.bar(x - width/2, prep_scores.loc['completed'],   width, label='Completed Prep', color=GREEN,  edgecolor='#0d1117', alpha=0.85)
b2 = ax2.bar(x + width/2, prep_scores.loc['none'],        width, label='No Prep',        color=RED,    edgecolor='#0d1117', alpha=0.85)
ax2.set_title('Score by Test Prep — Completed vs Not', fontsize=13, fontweight='bold', color='white', pad=15)
ax2.set_xticks(x); ax2.set_xticklabels(subjects)
ax2.set_ylabel('Average Score', fontsize=10)
ax2.set_ylim(0, 80)
ax2.legend(frameon=False, labelcolor='white', fontsize=10)
ax2.grid(axis='y', alpha=0.3)
for bar in b1:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{bar.get_height():.0f}', ha='center', fontsize=9, color='white', fontweight='bold')
for bar in b2:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{bar.get_height():.0f}', ha='center', fontsize=9, color='white', fontweight='bold')

# ── Chart 3: Performance Segments ────────────────────────────
ax3 = axes[1, 0]
seg_order  = ['High (80+)', 'Medium (60-79)', 'At Risk (40-59)', 'Critical (<40)']
seg_colors = [GREEN, BLUE, ORANGE, RED]
seg_counts = df['performance_segment'].value_counts().reindex(seg_order, fill_value=0)
bars3 = ax3.bar(seg_counts.index, seg_counts.values, color=seg_colors, edgecolor='#0d1117', width=0.5)
ax3.set_title('Student Performance Segments', fontsize=13, fontweight='bold', color='white', pad=15)
ax3.set_ylabel('Number of Students', fontsize=10)
ax3.set_xticklabels(seg_order, fontsize=9)
ax3.grid(axis='y', alpha=0.3)
for bar in bars3:
    pct = bar.get_height()/len(df)*100
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3,
             f'{bar.get_height()}\n({pct:.1f}%)', ha='center', fontsize=9, color='white', fontweight='bold')

# ── Chart 4: Score Distribution by Subject ───────────────────
ax4 = axes[1, 1]
ax4.hist(df['math score'],    bins=20, alpha=0.6, color=BLUE,   label='Math',    edgecolor='#0d1117')
ax4.hist(df['reading score'], bins=20, alpha=0.6, color=GREEN,  label='Reading', edgecolor='#0d1117')
ax4.hist(df['writing score'], bins=20, alpha=0.6, color=ORANGE, label='Writing', edgecolor='#0d1117')
ax4.set_title('Score Distribution by Subject', fontsize=13, fontweight='bold', color='white', pad=15)
ax4.set_xlabel('Score', fontsize=10)
ax4.set_ylabel('Number of Students', fontsize=10)
ax4.legend(frameon=False, labelcolor='white', fontsize=10)
ax4.axvline(50, color=RED, linestyle='--', alpha=0.7, linewidth=1.5)
ax4.text(51, 55, 'Pass\nLine', color=RED, fontsize=9)
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('project2/dashboard_1_student_executive.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("✅ Chart 1 saved!")

# ════════════════════════════════════════════════════════════
# FIGURE 2 — DROP-OFF & ENGAGEMENT ANALYSIS
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Student Drop-off, Risk & Engagement Analysis',
             fontsize=18, fontweight='bold', color='white', y=1.01)

# ── Chart 5: Engagement Funnel ───────────────────────────────
ax5 = axes[0]
funnel_stages = ['Enrolled\nStudents', 'Attempted\nAll Subjects', 'Passed\nAll Subjects', 'High\nPerformers']
funnel_values = [
    len(df),
    len(df),  # all attempted
    df['pass_all'].sum(),
    len(df[df['avg_score'] >= 80])
]
colors_f = [BLUE, PURPLE, GREEN, YELLOW]
bars5 = ax5.barh(funnel_stages[::-1], funnel_values[::-1], color=colors_f, edgecolor='#0d1117', height=0.5)
ax5.set_title('Student Engagement Funnel', fontsize=12, fontweight='bold', color='white', pad=10)
ax5.set_xlabel('Number of Students', fontsize=10)
ax5.grid(axis='x', alpha=0.3)
for bar, val in zip(bars5, funnel_values[::-1]):
    pct = val/len(df)*100
    ax5.text(bar.get_width()+5, bar.get_y()+bar.get_height()/2,
             f'{val:,} ({pct:.0f}%)', va='center', fontsize=10, color='white', fontweight='bold')

# ── Chart 6: At-Risk by Parental Education ───────────────────
ax6 = axes[1]
edu_risk = df.groupby('parental level of education').apply(
    lambda x: (x['avg_score'] < 50).sum() / len(x) * 100
).sort_values(ascending=True)
colors6 = [GREEN if v < 15 else ORANGE if v < 25 else RED for v in edu_risk.values]
bars6 = ax6.barh(edu_risk.index, edu_risk.values, color=colors6, edgecolor='#0d1117', height=0.5)
ax6.set_title('At-Risk Students by\nParental Education', fontsize=12, fontweight='bold', color='white', pad=10)
ax6.set_xlabel('At-Risk Rate (%)', fontsize=10)
ax6.grid(axis='x', alpha=0.3)
for bar, val in zip(bars6, edu_risk.values):
    ax6.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
             f'{val:.1f}%', va='center', fontsize=9, color='white')

# ── Chart 7: Impact of Lunch (Socioeconomic) ─────────────────
ax7 = axes[2]
lunch_scores = df.groupby('lunch')[['math score','reading score','writing score']].mean()
x = np.arange(3)
width = 0.35
b1 = ax7.bar(x - width/2, lunch_scores.loc['standard'],     width, label='Standard Lunch',      color=GREEN,  edgecolor='#0d1117', alpha=0.85)
b2 = ax7.bar(x + width/2, lunch_scores.loc['free/reduced'], width, label='Free/Reduced Lunch',  color=ORANGE, edgecolor='#0d1117', alpha=0.85)
ax7.set_title('Score by Socioeconomic Factor\n(Lunch Type)', fontsize=12, fontweight='bold', color='white', pad=10)
ax7.set_xticks(x); ax7.set_xticklabels(['Math', 'Reading', 'Writing'])
ax7.set_ylabel('Average Score', fontsize=10)
ax7.set_ylim(0, 80)
ax7.legend(frameon=False, labelcolor='white', fontsize=10)
ax7.grid(axis='y', alpha=0.3)
for bar in b1:
    ax7.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{bar.get_height():.0f}', ha='center', fontsize=9, color='white', fontweight='bold')
for bar in b2:
    ax7.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{bar.get_height():.0f}', ha='center', fontsize=9, color='white', fontweight='bold')

plt.tight_layout()
plt.savefig('project2/dashboard_2_dropoff.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("✅ Chart 2 saved!")

# ════════════════════════════════════════════════════════════
# SQL QUERIES
# ════════════════════════════════════════════════════════════
sql = """-- ============================================================
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
"""
with open('project2/student_analysis.sql', 'w') as f:
    f.write(sql)
print("✅ SQL saved!")

# ════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("KEY INSIGHTS")
print("="*60)
prep = df.groupby('test preparation course')['avg_score'].mean()
print(f"\n1. Test prep completion rate: {df['completed_prep'].mean()*100:.1f}%")
print(f"2. Avg score WITH prep:    {prep['completed']:.1f}")
print(f"   Avg score WITHOUT prep: {prep['none']:.1f}")
print(f"   Improvement: +{prep['completed']-prep['none']:.1f} points")
print(f"\n3. Pass all subjects: {df['pass_all'].mean()*100:.1f}%")
print(f"4. At-risk students (<50 avg): {(df['avg_score']<50).sum()} ({(df['avg_score']<50).mean()*100:.1f}%)")
print(f"5. High performers (80+): {(df['avg_score']>=80).sum()} ({(df['avg_score']>=80).mean()*100:.1f}%)")
print("="*60)
print("\n✅ ALL DONE! Project 2 ready for GitHub!")
