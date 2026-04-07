# 🛡️ Threat Intelligence Lab Exercise

## 🎯 Objective

In this exercise, you will conduct a **full threat intelligence workflow** on a real-world APT (Advanced Persistent Threat) group. You will collect open-source intelligence (OSINT) reports, analyze them using automated scripts, extract Indicators of Compromise (IOCs), and document your findings in a structured threat event on MISP unsing AI.

---

## 📋 Prerequisites

Before starting, make sure the following are available on your system:

- Access to the working directory: `~/workshop/threat-intel/`
- Python scripts available:
  - `threatintel_flow.py`
  - `threatintel_flow_IOC.py`
- Access to your lab's **MISP instance** (credentials provided by instructor)
- Tools: `wget` or `curl`, `python3.10` or `python3.11`

---

## 🔎 Step 1 — Choose Your APT Group

Using **Google Dork**, select one APT group from the list below (or choose your own with instructor approval):

| APT Group | Also Known As |
|-----------|---------------|
|APT28 | Fancy Bear |
|APT29 | Cozy Bear |
|APT41 | Double Dragon/Wicked Panda |
|APT38 | Lazarus Group/Hidden Cobra |
|APT44 | Sandworm  |
|APT1 | Comment Crew |
|APT10 | MenuPass/Stone Panda |
|APT33 | Elfin/Curious Serpens |
|APT34 | OilRig/Helix Kitten |
|Turla | Snake/Venomous Bear |
|APT43 | Kimsuky |
|APT37 | ScarCruft/Reaper |
|APT34 | MuddyWater/Neighbor |
|Gamaredon | Primitive Bear |
|APT40 | Bronze Mohawk/TEMP.Periscope |

> **⚠️ Note:** Each student must choose a **different** APT group. Confirm your choice with your instructor.

---

## 🔍 Step 2 — Search for PDF Reports (Google Dork)

Use the following **Google Dork query** in your browser, replacing the threat actor names with those matching your chosen APT group:

```
"APT28" OR "Fancy Bear" ("threat intelligence" OR "report" OR "analysis" OR "IOC") filetype:pdf
```

**How to adapt the query:**

- Replace `"APT28"` with your group's official designation (e.g., `"APT29"`)
- Replace `"Fancy Bear"` with the group's alias (e.g., `"Cozy Bear"`)
- Keep the rest of the query unchanged

**Goal:** Identify **3 to 5 relevant PDF reports** from trusted sources such as:
- Mandiant / FireEye
- CrowdStrike
- MITRE ATT&CK
- CISA / US-CERT
- Recorded Future
- Unit 42 (Palo Alto Networks)

> 📌 Save the direct download URLs of the PDFs you select, you will need them in the next step.

---

## 📁 Step 3 — Prepare the Working Directory

Open a terminal and execute the following commands to clean and prepare your working directory:

```bash
# Navigate to the working directory
cd ~/workshop/threat-intel/

# Remove all existing files
rm -f *.pdf

# Verify the directory is empty
ls -la
```

Then **download your selected PDF reports** into this directory:

```bash
# Example — replace the URL with each of your PDF links
wget -O report1.pdf "https://example.com/path/to/report.pdf"
wget -O report2.pdf "https://example.com/path/to/second-report.pdf"
# Repeat for each report...
```

> 💡 Tip: Name your files descriptively (e.g., `mandiant_apt28_2023.pdf`) for easier reference.

Verify your downloads:

```bash
ls -lh ~/workshop/threat-intel/
```

---

## ⚙️ Step 4 — Run the Threat Intelligence Analysis Script

Execute `threatintel_flow.py` from the working directory:

```bash
cd ~/workshop/threat-intel/
python3 threatintel_flow.py
```

This script will:
- Parse all PDF reports in the current directory
- Extract key intelligence (TTPs, threat actors, targeted sectors, timeline)
- Generate a structured **threat intelligence report**

**Expected output:** A report file (`hafnium_threat_profile.md`) will be created in `~/workshop/`.

> 📌 **Deliverable #1:** This generated report must be submitted to **Google Classroom**.

---

## 🧩 Step 6 — Extract IOCs

Run the IOC extraction script on the same PDF files:

```bash
cd ~/workshop/threat-intel/
python3 threatintel_flow_IOC.py
```

This script will extract the following types of IOCs from the reports:

| IOC Type | Examples |
|----------|----------|
| IP Addresses | `192.168.1.1`, `45.33.32.156` |
| Domain Names | `malicious-domain.com` |
| File Hashes | MD5, SHA1, SHA256 |
| URLs | `http://evil.example.com/payload` |
| Email Addresses | `attacker@domain.ru` |
| CVE References | `CVE-2021-44228` |

**Expected output:** An IOC list file (`hafnium_ioc.md`) in the working directory.

Review the extracted IOCs before proceeding:

```bash
cat ~/workshop/hafnium_ioc.md
```

---

## 🗂️ Step 7 — Create a MISP Event

Log in to your lab's **MISP instance** and follow these steps:

### 7.1 — Create a New Event

1. Go to **Event Actions** → **Add Event**
2. Fill in the fields as follows:

| Field | Value |
|-------|-------|
| **Event name** | `YourName_APT##_AI` (e.g., `JohnDoe_APT28_AI`) |
| **Distribution** | `This community only` |
| **Threat Level** | `High` |
| **Analysis** | `Completed` |
| **Date** | Today's date |

3. Click **"Add"** to create the event.
4. Follow the instruction on "TP3_MISP_Lab.docx" / MODULE 4 - Lab Exercises -> Exercise 1

> 📌 **Deliverable #2:** A screenshot or export of your completed MISP event must be submitted to **Google Classroom**.

---

## ✅ Summary of Deliverables

| # | Deliverable | Submission Method |
|---|-------------|-------------------|
| 1 | Generated threat intelligence report (`threatintel_flow.py` output) | Google Classroom |
| 2 | MISP event `YourName_APT##_AI` with all IOCs populated | Screenshot / MISP export on Google Classroom |



---

## 💡 Tips & Reminders

- Use **trusted sources only** for your PDF reports (avoid random blogs or unverified sites).
- In MISP, always double-check the **attribute type** — using the wrong type (e.g., `ip-src` instead of `ip-dst`) affects detection rules.

---
