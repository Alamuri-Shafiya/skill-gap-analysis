# AI-Based Skill Gap and Training Recommendation System

## 📌 Project Overview

The AI-Based Skill Gap and Training Recommendation System is a data-driven application designed to identify the gap between the skills possessed by candidates and the skills currently required for CSE-related job roles.

The system analyzes candidate skill information and compares it with skills demanded in the job market. Based on this comparison, it identifies matching skills, missing skills, calculates the overall skill match percentage, and recommends suitable training programs to help candidates improve their employability.

This project aims to support students, job seekers, training institutes, and organizations by providing useful insights into current industry skill requirements.

## 🎯 Problem Statement

Students and job seekers often face difficulties in understanding which skills are required for specific job roles. At the same time, training institutes and organizations may find it difficult to identify skill gaps and evaluate whether available training programs are aligned with current industry requirements.

Our system addresses this problem by combining candidate data with job-market skill information to provide automated skill-gap analysis and training recommendations.

## 💡 Proposed Solution

The proposed system performs the following steps:

1. Collects candidate and job-market data.
2. Cleans and preprocesses the collected data.
3. Focuses on major CSE-related job roles.
4. Extracts commonly required skills from job postings.
5. Compares candidate skills with job-role requirements.
6. Identifies matching and missing skills.
7. Calculates the candidate's skill match percentage.
8. Recommends suitable training based on missing skills.
9. Displays the results through an interactive web application.

## ✨ Key Features

- 👤 Candidate profile analysis
- 💼 CSE job-role analysis
- 🔍 Skill matching
- ⚠️ Skill-gap identification
- 📊 Skill match percentage calculation
- 📚 Training recommendations
- 📈 Job-market skill analysis
- 🌐 Interactive Streamlit web application

## 👨‍💻 Job Roles Covered

The current system focuses on four major CSE-related roles:

- Software Engineer
- Data Scientist
- AI Researcher
- Cybersecurity Analyst

## 🛠️ Technologies Used

- **Python** – Main programming language
- **Pandas** – Data preprocessing and analysis
- **NumPy** – Numerical operations
- **Scikit-learn** – Machine learning and data analysis
- **Streamlit** – Web application development
- **Microsoft Power BI** – Data visualization and dashboard analysis
- **Excel / CSV** – Dataset storage and processing

## 📂 Datasets Used

### 1. AI Resume Screening Dataset

This dataset contains candidate-related information such as skills, education, certifications, job role, projects, and other resume attributes.

It is used for candidate skill analysis and resume-related processing.

### 2. Indian Job Market Dataset

This dataset contains job-market information including job titles, skills, companies, locations, job descriptions, and salary-related information.

The dataset is filtered to focus on CSE and IT-related job roles and is used to identify the skills demanded by the industry.

## 🔄 System Workflow

```text
Candidate Data
      ↓
Data Preprocessing
      ↓
Candidate Skill Extraction
      ↓
Job Market Data
      ↓
CSE Job Filtering
      ↓
Skill Demand Analysis
      ↓
Skill Gap Analysis
      ↓
Skill Match Percentage
      ↓
Training Recommendation
      ↓
Streamlit Web Application
