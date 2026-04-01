# AI-Powered Cyber Threat Intelligence: From Raw Reports to Adversary Emulation

---

## 📋 Table of Contents

1. [Course Introduction](#1-course-introduction)
2. [Learning Objectives](#2-learning-objectives)
3. [Why AI Agents for Threat Intelligence?](#3-why-ai-agents-for-threat-intelligence)
4. [Understanding AI Agents : Core Concepts](#4-understanding-ai-agents--core-concepts)
5. [The CrewAI Framework : Architecture Deep Dive](#5-the-crewai-framework--architecture-deep-dive)
6. [System Requirements & Prerequisites](#6-system-requirements--prerequisites)
7. [Step-by-Step Environment Setup](#7-step-by-step-environment-setup)
8. [Generating Your API Keys](#8-generating-your-api-keys)
9. [Module 1 : Manual Adversary Research (HAFNIUM)](#9-module-1--manual-adversary-research-hafnium)
10. [Module 2 : TTP Extraction & MITRE ATT\&CK Mapping](#10-module-2--ttp-extraction--mitre-attck-mapping)
11. [Module 3 : Building ATT\&CK Navigator Layers](#11-module-3--building-attck-navigator-layers)
12. [Module 4 : Building Your First AI Agent Pipeline](#12-module-4--building-your-first-ai-agent-pipeline)
13. [Module 5 : Multi-Agent Crew with Local PDF Reports](#13-module-5--multi-agent-crew-with-local-pdf-reports)
14. [Module 6 : Live Intelligence Gathering with Web Search](#14-module-6--live-intelligence-gathering-with-web-search)
15. [Validation & Critical Thinking : Spotting AI Hallucinations](#15-validation--critical-thinking--spotting-ai-hallucinations)
16. [Challenges & Extension Tasks](#16-challenges--extension-tasks)
17. [What Comes Next](#17-what-comes-next)
18. [Quick Reference & Cheatsheet](#18-quick-reference--cheatsheet)

---

## 1. Course Introduction

Threat intelligence is the backbone of effective adversary emulation. Yet the traditional workflow, reading through long reports, manually identifying TTPs, cross-referencing MITRE ATT&CK, is painfully slow. A single analyst might spend an entire day building an adversary profile that a well-designed AI pipeline can produce in under a minute.

This course bridges both worlds. You will:

- **Build by hand first.** Research HAFNIUM (the Chinese state-sponsored group behind ProxyLogon) the traditional way, reading real reports, extracting TTPs manually, creating an ATT&CK Navigator layer. This gives you the analytical foundation to evaluate AI output.
- **Then automate it.** Design a multi-agent AI pipeline using CrewAI that reads the same reports and produces a structured adversary profile automatically.
- **Then go live.** Extend your pipeline to pull fresh intelligence directly from the internet using an AI-integrated web search agent.

By the end, you'll have a production-ready workflow that can be applied to any threat group, not just HAFNIUM.


---

## 2. Learning Objectives

After completing this course, students will be able to:

| # | Objective |
|---|-----------|
| 1 | Explain the role of threat intelligence in adversary emulation planning |
| 2 | Conduct structured adversary research using open-source reports |
| 3 | Extract and classify TTPs from narrative threat reports |
| 4 | Map TTPs to MITRE ATT&CK using the correct framework taxonomy |
| 5 | Create ATT&CK Navigator visualization layers |
| 6 | Define and explain core AI agent concepts: Agent, Task, Crew, Tool, Flow |
| 7 | Justify the use of multi-agent architectures over single-prompt LLM approaches |
| 8 | Set up a Python environment with CrewAI and configure LLM API keys |
| 9 | Build a multi-agent pipeline that analyzes PDF threat reports autonomously |
| 10 | Integrate live web search into an AI intelligence gathering workflow |
| 11 | Critically evaluate AI-generated threat profiles for hallucinations and errors |

---

## 3. Why AI Agents for Threat Intelligence?

### The Problem with Traditional CTI Workflows

Threat intelligence production has a throughput problem. Consider what a human analyst must do to profile a single threat actor:

```
Read 3–8 reports (often 20–80 pages each)
        ↓
Identify relevant indicators and TTPs
        ↓
Cross-reference MITRE ATT&CK (hundreds of techniques)
        ↓
Resolve ambiguous mappings manually
        ↓
Structure findings into a profile
        ↓
Review for completeness and accuracy
```

This process can take **6–8 hours per threat actor**. For a team tracking 20 active threat groups, that's weeks of research before a single emulation plan exists.

### Why Not Just Use ChatGPT?

Pasting a report into a general-purpose chat interface has real limitations:

| Limitation | Impact |
|------------|--------|
| **No structured workflow** | Output format changes between sessions |
| **Context window overflow** | Large reports degrade output quality |
| **No tool integration** | Can't read local files, search the web, or write structured outputs |
| **No pipeline continuity** | Each session starts from scratch |
| **Hard to validate** | No audit trail of what the model "read" vs. assumed |

### Why AI Agents?

AI agents solve these problems with three key properties:

**1. Role Specialization**  
Instead of one model doing everything, you assign distinct roles: one agent reads reports, another maps TTPs, another writes the final profile. Each agent is optimized for a narrow task.

**2. Tool Use**  
Agents can use real tools, file readers, web search APIs, code interpreters. They don't just think; they act.

**3. Orchestration & Memory**  
Multi-agent frameworks like CrewAI manage task sequencing, pass outputs between agents, and maintain shared state across a pipeline, something a chat interface can't do.

```
Traditional Approach:    Human → reads report → maps TTPs → writes profile
                         Time: 6-8 hours per actor

AI Agent Approach:       Pipeline → reads reports → maps TTPs → writes profile
                         Time: ~5 minutes per actor
                         Human role: set direction + validate output
```

### The Right Mental Model

AI agents are not a replacement for human expertise, they are a **force multiplier**. Your job shifts from doing the research to:
- Designing the pipeline
- Curating the inputs
- Validating the output
- Acting on the findings

---

## 4. Understanding AI Agents — Core Concepts

Before writing any code, you need a clear mental model of how AI agents work. The following concepts apply across frameworks, not just CrewAI.

### What is an AI Agent?

An AI agent is an autonomous system that perceives inputs, reasons about them, and takes actions to accomplish a goal. Unlike a standard LLM prompt (which produces a single response), an agent can:

- Use tools (search the web, read files, run code)
- Make decisions based on intermediate results
- Retry failed actions
- Break large goals into subtasks

```
Traditional LLM:     Input → Model → Output
                     (one shot, no feedback)

AI Agent:            Input → Model → Action → Result → Model → Action → Result → Output
                     (iterative, tool-augmented reasoning)
```

### The ReAct Pattern

Most agent frameworks use the **ReAct** pattern (Reasoning + Acting):

```
1. THOUGHT:  "I need to read the HAFNIUM report to extract TTPs"
2. ACTION:   Call the PDF reader tool with filename
3. RESULT:   "Report content: ..."
4. THOUGHT:  "I see references to T1190 and T1059. Let me map these."
5. ACTION:   Return structured TTP list
```

The model alternates between reasoning and acting until it completes the task.

### Agentic vs. Non-Agentic LLM Usage

| Property | Non-Agentic (Chat) | Agentic |
|----------|-------------------|---------|
| Tool use | Manual (you copy-paste) | Automatic |
| Memory | None between sessions | Shared state |
| Workflow | Linear | Parallel/sequential orchestration |
| Error handling | User must retry | Agent retries automatically |
| Output format | Free-form | Structured, schema-enforced |
| Scalability | One at a time | Parallel agents |

### Key Terminology

| Term | Definition |
|------|------------|
| **Agent** | An AI worker with a role, goal, and backstory. Has access to tools. |
| **Task** | A specific assignment: a description + expected output format. |
| **Crew** | A coordinated team of agents working through a set of tasks. |
| **Tool** | A capability (file reader, web search, code runner) an agent can invoke. |
| **Flow** | An orchestration layer managing state and sequencing between multiple crews. |
| **LLM Backend** | The language model powering the agent (GPT-4o, Claude, Gemini, etc.) |
| **Hallucination** | When an agent confidently produces false information. Must be validated. |

---

## 5. The CrewAI Framework — Architecture Deep Dive

### What is CrewAI?

[CrewAI](https://github.com/crewAIInc/crewAI) is an open-source Python framework for building multi-agent AI pipelines. It provides:

- A structured way to define agents and their roles
- Task orchestration with sequential or parallel execution
- Built-in tool ecosystem (file readers, web search, code execution)
- A `Flow` abstraction for multi-phase, stateful pipelines
- Support for 20+ LLM providers through LiteLLM

### Why CrewAI for CTI?

| Requirement | CrewAI Solution |
|-------------|----------------|
| Process multiple reports in parallel | `asyncio`-powered parallel Crews |
| Pass results between pipeline phases | `Flow` shared state (`self.state`) |
| Read PDF files | `PDFSearchTool` |
| Search the web for fresh intel | `TavilySearchTool` |
| Work with multiple LLM providers | LiteLLM backend integration |
| Open-source, auditable | Full source on GitHub |

### Pipeline Architecture

The pipeline you will build in this course has three phases:

```
┌─────────────────────────────────────────────────────────────────┐
│                        ThreatIntelFlow                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PHASE 1 — @start()  ·  discover_files()                │   │
│  │  Discovery Crew identifies PDF reports in the workspace  │   │
│  │  → Writes file paths to shared state                     │   │
│  └───────────────────────────┬─────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PHASE 2 — @listen()  ·  read_pdfs_parallel()           │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐            │   │
│  │  │  Crew 1   │  │  Crew 2   │  │  Crew 3   │            │   │
│  │  │  PDF #1   │  │  PDF #2   │  │  PDF #3   │            │   │
│  │  │ (MSFT)    │  │ (Mandiant)│  │ (Volexity)│            │   │
│  │  └───────────┘  └───────────┘  └───────────┘            │   │
│  │  → Each Crew extracts TTPs from one report               │   │
│  │  → Writes all summaries to shared state                  │   │
│  └───────────────────────────┬─────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PHASE 3 — @listen()  ·  analyze_and_map()              │   │
│  │  Analyst → ATT&CK Mapper → Report Writer                 │   │
│  │  → Produces hafnium_threat_profile.md                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Shared State — How Data Flows

```
┌──────────────────────────────────────────────────────┐
│             SHARED STATE  (self.state)                │
│                                                      │
│  pdf_paths:           [list of PDF file paths]        │
│  pdf_summaries:       [TTP summary per report]        │
│  combined_summaries:  "all summaries as one string"  │
│  final_report:        "completed threat profile"     │
└──────────────────────────────────────────────────────┘
         ↑                    ↑                  ↑
    Phase 1 writes       Phase 2 writes     Phase 3 reads
    file paths           all summaries      combined data
                                            & writes report
```

### Why Multiple Crews Instead of One?

This is the question every student asks. Two technical reasons:

**Context Window Overflow:** LLMs have token limits. Three research reports may total 30,000–60,000 tokens. Feeding all of them into a single agent context pushes the model to its limits — or beyond — where output quality degrades significantly.

**Attention Dilution:** Even within token limits, attention quality drops as context grows. A model analyzing one focused document produces sharper extractions than the same model processing three documents simultaneously. Parallel crews with isolated contexts solve both problems.

---

## 6. System Requirements & Prerequisites

### Hardware & OS

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Ubuntu 22.04, macOS 12+, Windows WSL2 | Ubuntu 22.04 LTS |
| RAM | 4 GB | 8 GB+ |
| Disk | 2 GB free | 5 GB free |
| Python | 3.10 | 3.11 or 3.12 |
| Network | Required | Stable broadband |

> 💡 **Windows Users:** Use WSL2 with Ubuntu 22.04. Native Windows Python environments may have path issues with some CrewAI dependencies.

### Knowledge Prerequisites

Students should be comfortable with:
- Basic Linux/terminal commands
- Python syntax fundamentals (functions, classes, `import`)
- General understanding of cybersecurity terminology
- Familiarity with MITRE ATT&CK at a conceptual level

### Accounts You Will Need

| Service | Purpose | Free Tier? |
|---------|---------|------------|
| OpenAI / Anthropic / Groq | LLM backend for agents | Groq & Google: Yes |
| Tavily | Web search for Exercise 6 | Yes (1,000 calls/month) |
| GitHub | Hosting your Navigator layers | Yes |

---

## 7. Step-by-Step Environment Setup

### Step 1 — Verify Python Version

```bash
python3 --version
```

**Expected output:**
```
Python 3.10.x  (or higher)
```

If Python 3.10+ is not installed:

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3.11 python3.11-pip -y
```

**macOS (with Homebrew):**
```bash
brew install python@3.11
```

**Windows WSL2:**
```bash
sudo apt update && sudo apt install python3.11 python3-pip -y
```

---

### Step 2 — Verify Internet Connectivity

```bash
ping -c 4 sans.org
```

You should see response times. If not, resolve your network configuration before proceeding — the pipeline needs access to LLM APIs and optionally web search.

---

### Step 3 — Create a Virtual Environment (Recommended)

Using a virtual environment isolates your project dependencies and prevents conflicts with system packages:

```bash
# Create the virtual environment
python3 -m venv ~/workshop/venv

# Activate it
source ~/workshop/venv/bin/activate

# Confirm you're using the venv Python
which python3
# Should show: /home/<your-user>/workshop/venv/bin/python3
```

> ⚠️ **Always activate your venv before working on this project.** If you close your terminal, re-run `source ~/workshop/venv/bin/activate`.

---

### Step 4 — Install Python Dependencies

With your virtual environment active:

```bash
pip install --upgrade pip
pip install 'crewai[tools]' pypdf tavily-python
```

**What each package does:**

| Package | Purpose |
|---------|---------|
| `crewai[tools]` | Core multi-agent framework + built-in tools (PDF reader, web search, etc.) |
| `pypdf` | PDF parsing library used by CrewAI's PDF tools |
| `tavily-python` | Tavily web search SDK for live intelligence gathering |

---

### Step 5 — Set Up Working Directories

```bash
mkdir -p ~/workshop/threat-intel     # Store PDF reports here
mkdir -p ~/workshop/threatintel-crew # Store your Python scripts here
cd ~/workshop
```

---

### Step 6 — Gather the HAFNIUM Reports (PDF Format)

You will analyze three real public reports on the HAFNIUM threat group.

Open each URL in your browser and save the page as PDF (`File → Print → Save as PDF`):

| Report | URL | Save As |
|--------|-----|---------|
| Microsoft HAFNIUM Report | https://www.microsoft.com/security/blog/2021/03/02/hafnium-targeting-exchange-servers/ | `Microsoft-HAFNIUM-report.pdf` |
| Mandiant Exchange Zero-Days | https://www.mandiant.com/resources/detection-response-to-exploitation-of-microsoft-exchange-zero-day-vulnerabilities | `Mandiant-Microsoft-Exchange-Zero-Days.pdf` |
| Volexity Operation Exchange Marauder | https://www.volexity.com/blog/2021/03/02/active-exploitation-of-microsoft-exchange-zero-day-vulnerabilities/ | `Volexity-Operation-Exchange-Marauder.pdf` |

Move them to your working directory:

```bash
mv ~/Downloads/Microsoft-HAFNIUM-report.pdf ~/workshop/threat-intel/
mv ~/Downloads/Mandiant-Microsoft-Exchange-Zero-Days.pdf ~/workshop/threat-intel/
mv ~/Downloads/Volexity-Operation-Exchange-Marauder.pdf ~/workshop/threat-intel/

# Verify they landed correctly
ls -lh ~/workshop/threat-intel/
```

---

### Step 7 — Verify Everything Works

```bash
python3 -c "import crewai; import pypdf; print('✅ All imports successful')"
```

**Expected output:**
```
✅ All imports successful
```

If you see an error, check the Troubleshooting section below.

---

### Troubleshooting

<details>
<summary>❌ <code>pip install</code> fails with permission error</summary>

```bash
# Option A: Use the --user flag
pip install --user 'crewai[tools]' pypdf tavily-python

# Option B: Use a virtual environment (recommended)
python3 -m venv ~/workshop/venv
source ~/workshop/venv/bin/activate
pip install 'crewai[tools]' pypdf tavily-python
```
</details>

<details>
<summary>❌ ModuleNotFoundError: No module named 'crewai'</summary>

Python path mismatch. Try:

```bash
pip3 install 'crewai[tools]' pypdf tavily-python
python3 -c "import crewai; print('OK')"
```

Or ensure you've activated your virtual environment:
```bash
source ~/workshop/venv/bin/activate
```
</details>

<details>
<summary>❌ SSL or network errors during pip install</summary>

```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org 'crewai[tools]' pypdf tavily-python
```
</details>

<details>
<summary>❌ crewai version conflicts</summary>

```bash
pip install 'crewai[tools]==0.28.8'
```
Check the [CrewAI releases](https://github.com/crewAIInc/crewAI/releases) for the current stable version.
</details>

---

## 8. Generating Your API Keys

You need one LLM provider. Pick the one that fits your situation.

### Option A — OpenAI API Key (GPT-4o)

1. Go to [https://platform.openai.com](https://platform.openai.com)
2. Create an account or sign in
3. Navigate to **API Keys** in the left sidebar
4. Click **"Create new secret key"**
5. Name it (e.g., `cti-workshop`) and copy the key — **you cannot view it again**
6. Add billing information (small costs apply per token used)

```bash
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> 💰 **Cost estimate:** This workshop uses ~50,000–100,000 tokens. At GPT-4o pricing, expect under $1 USD for the full workshop.

---

### Option B — Anthropic API Key (Claude)

1. Go to [https://console.anthropic.com](https://console.anthropic.com)
2. Create an account and verify your email
3. Navigate to **API Keys** → **Create Key**
4. Copy the key immediately

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

### Option C — Groq API Key (Free Tier Available)

Groq offers a **free tier** with fast inference — a great option for students:

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up with a Google or GitHub account
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key

```bash
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> 🆓 **Free tier:** Groq's free tier supports ~14,400 requests/day on Llama 3.3 70B — more than enough for this workshop.

---

### Option D — Google Gemini API Key (Free Tier Available)

1. Go to [https://aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create API key in new project"**
4. Copy the key

```bash
export GOOGLE_API_KEY="AIzaSy-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

### Option E — Ollama (Fully Local, No Key Required)

If you need a completely offline solution:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download a model
ollama pull llama3.2

# Verify it works
ollama run llama3.2 "Hello"
```

No API key needed. CrewAI detects Ollama automatically.

---

### Setting the Tavily API Key (Exercise 6)

Exercise 6 uses Tavily for live web search. Get your free key:

1. Go to [https://tavily.com](https://tavily.com)
2. Sign up and navigate to the dashboard
3. Copy your API key from **"API Key"** section

```bash
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

### Making API Keys Persistent

Environment variables set with `export` disappear when you close your terminal. To make them permanent:

```bash
# Add to your shell profile
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
echo 'export TAVILY_API_KEY="your-key-here"' >> ~/.bashrc

# Reload
source ~/.bashrc
```

For `zsh` (macOS default):
```bash
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

> 🔐 **Security Note:** Never commit API keys to a GitHub repository. Add `.env` files to your `.gitignore`. Consider using `python-dotenv` for local key management in production workflows.

---

## 9. Module 1 — Manual Adversary Research (HAFNIUM)

**Duration:** ~25 minutes  
**Goal:** Build a baseline adversary profile for HAFNIUM by hand

### Background: Who is HAFNIUM?

HAFNIUM is a Chinese state-sponsored threat actor attributed to China's civilian intelligence agency (MSS). They are best known for exploiting four zero-day vulnerabilities in Microsoft Exchange Server in early 2021 (CVE-2021-26855, 26857, 26858, 27065) — collectively dubbed **ProxyLogon**.

Sectors targeted include: defense contractors, law firms, NGOs, infectious disease researchers, higher education institutions.

### Exercise 1.1 — Research the Adversary

Using your browser, research HAFNIUM using the three reports downloaded during setup plus MITRE ATT&CK. Fill in the following profile template:

```
ADVERSARY PROFILE TEMPLATE
===========================

Threat Group Name:       HAFNIUM
Also Known As:           [List aliases]
Origin/Attribution:      [Country, sponsoring organization]
Motivation:              [Financial? Espionage? Disruption?]
Active Since:            [Estimated timeframe]
Primary Targets:         [Industry sectors / countries]
Key Infrastructure:      [VPS providers, C2 mechanisms]
Notable Operations:      [Named operations or campaigns]

ATT&CK Group Page:       https://attack.mitre.org/groups/G0125/
```

**Reference Resources:**
- [MITRE ATT&CK — HAFNIUM (G0125)](https://attack.mitre.org/groups/G0125/)
- [Microsoft HAFNIUM Blog Post](https://www.microsoft.com/security/blog/2021/03/02/hafnium-targeting-exchange-servers/)
- [CISA Advisory AA21-062A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-062a)

> ✅ **Checkpoint:** Before moving on, confirm you can answer: What was HAFNIUM's primary initial access vector? What was their objective after gaining access?

---

## 10. Module 2 — TTP Extraction & MITRE ATT&CK Mapping

**Duration:** ~25 minutes  
**Goal:** Extract TTPs from real reports and map them to ATT&CK

### What is a TTP?

**Tactics, Techniques, and Procedures (TTPs)** describe *how* a threat actor operates:

| Level | Description | ATT&CK Example |
|-------|-------------|----------------|
| **Tactic** | The adversary's high-level goal | `Initial Access` |
| **Technique** | The method used to achieve the goal | `T1190 — Exploit Public-Facing Application` |
| **Sub-technique** | A more specific variation | `T1059.001 — PowerShell` |
| **Procedure** | The exact implementation | "HAFNIUM used the China Chopper webshell deployed to `C:\inetpub\wwwroot\`" |

### Exercise 2.1 — Read and Extract

Open the **Microsoft HAFNIUM report** and complete the extraction table:

```
TTP EXTRACTION TABLE
====================

| Behavior Observed in Report | ATT&CK Tactic | ATT&CK Technique ID | Technique Name |
|-----------------------------|---------------|---------------------|----------------|
| Exploited CVE-2021-26855    | Initial Access | T1190              | Exploit Public-Facing Application |
| Used China Chopper webshell | Persistence    |                    |                |
| LSASS memory dumping        |                |                    |                |
| 7-Zip for data staging      |                |                    |                |
| WINRM for lateral movement  |                |                    |                |
| Exfiltration to MEGA        |                |                    |                |
```

**ATT&CK Lookup Resource:** [https://attack.mitre.org/techniques/enterprise/](https://attack.mitre.org/techniques/enterprise/)

### Exercise 2.2 — Cross-Report Validation

Repeat the extraction for the **Mandiant** and **Volexity** reports. Note any TTPs that appear across all three reports — these are the highest-confidence behaviors to include in an emulation plan.

```
CROSS-REPORT TTP CONFIDENCE TABLE
==================================

| ATT&CK ID | Technique Name | MSFT | Mandiant | Volexity | Confidence |
|-----------|----------------|------|----------|----------|------------|
| T1190     | Exploit Public-Facing App | ✓ | ✓ | ✓ | HIGH |
| T1505.003 | Web Shell      | ✓    | ✓        | ✓        | HIGH       |
| ...       | ...            |      |          |          |            |
```

> 📌 **Instructor Debrief:** After this exercise, compare student extractions. Common errors include: technique-procedure confusion (writing procedures as techniques), incorrect tactic classification, and misidentifying sub-techniques. Use these errors to motivate AI-assisted extraction.

---

## 11. Module 3 — Building ATT&CK Navigator Layers

**Duration:** ~20 minutes  
**Goal:** Visualize HAFNIUM's TTP coverage using ATT&CK Navigator

### What is ATT&CK Navigator?

[ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) is a web-based tool for annotating and visualizing the MITRE ATT&CK matrix. Red teams use it to show adversary coverage; blue teams use it to map defensive gaps.

### Exercise 3.1 — Create Your Layer

1. Go to [https://mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/)
2. Click **"Create New Layer"** → **"Enterprise ATT&CK"**
3. In the search bar, type each technique ID you extracted
4. Right-click techniques → **"Select Techniques"**
5. In the **"Technique Controls"** panel, change the color to red (`#ff0000`)
6. Add a comment to each technique with your source report

### Exercise 3.2 — Export Your Layer

1. Click the **download icon** (top right toolbar)
2. Select **"Download Layer"** (JSON format)
3. Save as `hafnium-layer.json`

### Exercise 3.3 — Compare Against the AI Output

Later in Module 5, the AI will produce its own ATT&CK layer. You will compare:
- Which techniques did both you and the AI find?
- What did the AI find that you missed?
- What did the AI get wrong?

This comparison is the core learning outcome of the course.

---

## 12. Module 4 — Building Your First AI Agent Pipeline

**Duration:** ~20 minutes  
**Goal:** Understand CrewAI's building blocks and verify your installation

### CrewAI Building Blocks in Practice

```python
from crewai import Agent, Task, Crew, LLM

# 1. Define the LLM backend
llm = LLM(model="openai/gpt-4o")
# or: LLM(model="anthropic/claude-sonnet-4-5")
# or: LLM(model="groq/llama-3.3-70b-versatile")
# or: LLM(model="ollama/llama3.2")

# 2. Define an Agent
analyst = Agent(
    role="CTI Analyst",
    goal="Extract all TTPs from a threat report and map them to MITRE ATT&CK",
    backstory="""You are a senior threat intelligence analyst at a cybersecurity firm.
                 You specialize in adversary profiling and ATT&CK mapping.""",
    llm=llm,
    verbose=True
)

# 3. Define a Task
extraction_task = Task(
    description="Read the provided report text and extract all TTPs as a structured list with ATT&CK IDs.",
    expected_output="A JSON-formatted list of TTPs with technique ID, name, tactic, and evidence.",
    agent=analyst
)

# 4. Assemble the Crew
crew = Crew(
    agents=[analyst],
    tasks=[extraction_task],
    verbose=True
)

# 5. Run it
result = crew.kickoff()
print(result)
```

### Exercise 4.1 — Verify Your Installation

Create the following file:

```bash
cd ~/workshop/threatintel-crew
nano test_crewai.py
```

Paste this code:

```python
import os
from crewai import Agent, Task, Crew, LLM

def get_llm():
    """Auto-detect LLM provider from environment variables."""
    if os.getenv("LITELLM_API_BASE"):
        return LLM(
            model=os.getenv("MODEL_NAME", "openai/gpt-4o"),
            base_url=os.getenv("LITELLM_API_BASE"),
            api_key=os.getenv("LITELLM_API_KEY")
        )
    elif os.getenv("ANTHROPIC_API_KEY"):
        return LLM(model="anthropic/claude-sonnet-4-5-20250929")
    elif os.getenv("GROQ_API_KEY"):
        return LLM(model="groq/llama-3.3-70b-versatile")
    elif os.getenv("OPENAI_API_KEY"):
        return LLM(model="openai/gpt-4o")
    else:
        return LLM(model="ollama/llama3.2")

llm = get_llm()

agent = Agent(
    role="Test Agent",
    goal="Verify that CrewAI is properly installed and configured",
    backstory="You are a verification agent checking that the system works correctly.",
    llm=llm,
    verbose=True
)

task = Task(
    description="Respond with exactly: 'CrewAI is working correctly. LLM connection established.'",
    expected_output="A confirmation message",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)
result = crew.kickoff()
print(f"\n✅ Result: {result}")
```

Run it:

```bash
python3 test_crewai.py
```

**Expected output:**
```
[Agent: Test Agent] Task output: CrewAI is working correctly. LLM connection established.

✅ Result: CrewAI is working correctly. LLM connection established.
```

> ❌ **Authentication error?** Run `echo $OPENAI_API_KEY` (or your provider's variable) to check it's set. If empty, re-run your `export` command and try again.

---

## 13. Module 5 — Multi-Agent Crew with Local PDF Reports

**Duration:** ~30 minutes  
**Goal:** Build the full 3-phase pipeline that reads PDFs and produces an adversary profile

### The Full Pipeline Code

Create the main script:

```bash
nano ~/workshop/threatintel-crew/threatintel_flow.py
```

```python
#!/usr/bin/env python3
"""
Threat Intelligence Multi-Agent Pipeline
=========================================
Reads HAFNIUM PDF reports and produces a structured ATT&CK-mapped profile.

Architecture:
  Phase 1: Discover PDF files in the threat-intel directory
  Phase 2: Process each PDF with an isolated crew (parallel)
  Phase 3: Synthesize all summaries into a final adversary profile
"""

import os
import asyncio
from pathlib import Path
from crewai import Agent, Task, Crew, LLM
from crewai.flow.flow import Flow, listen, start
from crewai_tools import PDFSearchTool
from pydantic import BaseModel


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

THREAT_INTEL_DIR = Path.home() / "workshop" / "threat-intel"
OUTPUT_FILE = Path.home() / "workshop" / "hafnium_threat_profile.md"


def get_llm():
    """Auto-detect LLM provider from environment variables."""
    if os.getenv("LITELLM_API_BASE"):
        return LLM(
            model=os.getenv("MODEL_NAME", "openai/gpt-4o"),
            base_url=os.getenv("LITELLM_API_BASE"),
            api_key=os.getenv("LITELLM_API_KEY")
        )
    elif os.getenv("ANTHROPIC_API_KEY"):
        return LLM(model="anthropic/claude-sonnet-4-5-20250929")
    elif os.getenv("GROQ_API_KEY"):
        return LLM(model="groq/llama-3.3-70b-versatile")
    elif os.getenv("OPENAI_API_KEY"):
        return LLM(model="openai/gpt-4o")
    else:
        return LLM(model="ollama/llama3.2")


# ─────────────────────────────────────────────
# SHARED STATE SCHEMA
# ─────────────────────────────────────────────

class ThreatIntelState(BaseModel):
    pdf_paths: list[str] = []
    pdf_summaries: list[str] = []
    combined_summaries: str = ""
    final_report: str = ""


# ─────────────────────────────────────────────
# AGENT FACTORY FUNCTIONS
# ─────────────────────────────────────────────

def make_discovery_agent(llm):
    return Agent(
        role="Intelligence File Discoverer",
        goal="Locate all PDF threat reports in the specified directory",
        backstory="""You are a CTI operations specialist responsible for 
                     cataloguing intelligence reports for analysis.""",
        llm=llm,
        verbose=True
    )

def make_pdf_analyst(llm, pdf_path: str):
    return Agent(
        role="Threat Report Analyst",
        goal=f"Extract all TTPs and key indicators from the report: {pdf_path}",
        backstory="""You are an expert threat intelligence analyst with deep knowledge 
                     of MITRE ATT&CK. You read reports and extract structured TTPs.""",
        tools=[PDFSearchTool(pdf=pdf_path)],
        llm=llm,
        verbose=True
    )

def make_attack_mapper(llm):
    return Agent(
        role="MITRE ATT&CK Mapper",
        goal="Map extracted behaviors to precise ATT&CK technique IDs",
        backstory="""You are an ATT&CK subject matter expert. You receive raw TTP 
                     descriptions and return validated technique IDs with tactic context.""",
        llm=llm,
        verbose=True
    )

def make_report_writer(llm):
    return Agent(
        role="Threat Profile Author",
        goal="Produce a structured, emulation-ready adversary profile in Markdown",
        backstory="""You write threat intelligence reports used by Red Teams to plan 
                     adversary emulation exercises. Your output must be precise, 
                     structured, and ready for operational use.""",
        llm=llm,
        verbose=True
    )


# ─────────────────────────────────────────────
# CREW BUILDER FOR A SINGLE PDF
# ─────────────────────────────────────────────

def build_pdf_crew(pdf_path: str, llm) -> Crew:
    analyst = make_pdf_analyst(llm, pdf_path)
    
    extract_task = Task(
        description=f"""Read the PDF at {pdf_path}. Extract:
        1. All attacker behaviors and actions
        2. Tools, malware, and scripts used
        3. Indicators of compromise (IoCs)
        4. Infrastructure details
        5. Target sectors and context
        
        For each behavior, map it to a MITRE ATT&CK technique if possible.
        Include the ATT&CK ID (e.g., T1190), technique name, and tactic.""",
        expected_output="""A structured summary with:
        - Threat group context (1-2 sentences)
        - TTP list: each item with [ATT&CK ID] Technique Name — Tactic — Evidence quote
        - Tools and malware observed
        - IoCs (hashes, IPs, domains if present)""",
        agent=analyst
    )
    
    return Crew(agents=[analyst], tasks=[extract_task], verbose=True)


# ─────────────────────────────────────────────
# PHASE 3: SYNTHESIS CREW
# ─────────────────────────────────────────────

def build_synthesis_crew(combined_summaries: str, llm) -> Crew:
    mapper = make_attack_mapper(llm)
    writer = make_report_writer(llm)
    
    map_task = Task(
        description=f"""Review these combined TTP summaries from multiple reports:
        
{combined_summaries}

Deduplicate and validate all ATT&CK mappings. Remove any incorrect technique IDs.
Produce a consolidated, deduplicated TTP list with confidence levels (HIGH/MEDIUM/LOW)
based on how many sources reported each behavior.""",
        expected_output="A deduplicated, validated TTP table with ATT&CK IDs, names, tactics, and confidence levels.",
        agent=mapper
    )
    
    write_task = Task(
        description="""Using the validated TTP table, write a complete adversary profile 
in Markdown format suitable for Red Team use. Include:
1. Executive Summary
2. Attribution and Background
3. Target Sectors
4. Attack Lifecycle (kill chain narrative)
5. Complete TTP Table (ATT&CK ID | Technique | Tactic | Confidence | Evidence)
6. Tools & Malware
7. Indicators of Compromise
8. Emulation Planning Notes (what to prioritize)
9. Detection Opportunities (brief)
10. References""",
        expected_output="A complete Markdown adversary profile ready for operational use.",
        agent=writer
    )
    
    return Crew(agents=[mapper, writer], tasks=[map_task, write_task], verbose=True)


# ─────────────────────────────────────────────
# MAIN FLOW ORCHESTRATION
# ─────────────────────────────────────────────

class ThreatIntelFlow(Flow[ThreatIntelState]):

    def __init__(self):
        super().__init__()
        self.llm = get_llm()

    @start()
    def discover_files(self):
        """Phase 1: Find all PDF files in the threat-intel directory."""
        print("\n🔍 Phase 1: Discovering PDF reports...")
        
        pdf_files = list(THREAT_INTEL_DIR.glob("*.pdf"))
        
        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF files found in {THREAT_INTEL_DIR}. "
                "Please complete the setup steps in Module 7."
            )
        
        self.state.pdf_paths = [str(p) for p in pdf_files]
        print(f"✅ Found {len(self.state.pdf_paths)} reports: {[p.name for p in pdf_files]}")

    @listen(discover_files)
    async def read_pdfs_parallel(self):
        """Phase 2: Process each PDF with an isolated crew (parallel execution)."""
        print(f"\n📄 Phase 2: Processing {len(self.state.pdf_paths)} PDFs in parallel...")
        
        async def process_pdf(pdf_path: str) -> str:
            crew = build_pdf_crew(pdf_path, self.llm)
            result = crew.kickoff()
            return str(result)
        
        tasks = [process_pdf(path) for path in self.state.pdf_paths]
        summaries = await asyncio.gather(*tasks)
        
        self.state.pdf_summaries = list(summaries)
        self.state.combined_summaries = "\n\n---\n\n".join(
            [f"## Report {i+1}: {Path(path).name}\n\n{summary}"
             for i, (path, summary) in enumerate(zip(self.state.pdf_paths, summaries))]
        )
        
        print(f"✅ Phase 2 complete. Processed {len(summaries)} reports.")

    @listen(read_pdfs_parallel)
    def analyze_and_map(self):
        """Phase 3: Synthesize all summaries into a final threat profile."""
        print("\n🧠 Phase 3: Synthesizing threat profile...")
        
        crew = build_synthesis_crew(self.state.combined_summaries, self.llm)
        result = crew.kickoff()
        
        self.state.final_report = str(result)
        
        # Save to file
        OUTPUT_FILE.write_text(self.state.final_report, encoding="utf-8")
        print(f"\n✅ Threat profile saved to: {OUTPUT_FILE}")
        print("\n" + "="*60)
        print(self.state.final_report[:2000] + "...")
        print("="*60)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    flow = ThreatIntelFlow()
    flow.kickoff()
```

### Running the Pipeline

```bash
cd ~/workshop/threatintel-crew
python3 threatintel_flow.py
```

**Watch for these outputs:**
```
🔍 Phase 1: Discovering PDF reports...
✅ Found 3 reports: ['Microsoft-HAFNIUM-report.pdf', ...]

📄 Phase 2: Processing 3 PDFs in parallel...
[multiple agent reasoning outputs...]

🧠 Phase 3: Synthesizing threat profile...
✅ Threat profile saved to: /home/<user>/workshop/hafnium_threat_profile.md
```

### Viewing the Output

```bash
cat ~/workshop/hafnium_threat_profile.md
```

---

## 14. Module 6 — Live Intelligence Gathering with Web Search

**Duration:** ~25 minutes  
**Prerequisites:** Tavily API key set as `TAVILY_API_KEY`

### Why Web Search Changes Everything

The PDF pipeline from Module 5 is powerful but limited to what's in your downloaded reports. The web search variant can:
- Pull the latest threat reporting published *today*
- Find new IoCs or infrastructure patterns
- Cross-reference attribution from multiple sources in real time

### The Web Search Crew

Create:

```bash
nano ~/workshop/threatintel-crew/threatintel_web.py
```

```python
#!/usr/bin/env python3
"""
Live Threat Intelligence Gathering via Web Search
==================================================
Uses Tavily search to pull real-time intelligence about a threat actor.
Requires: TAVILY_API_KEY environment variable
"""

import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import TavilySearchTool


def get_llm():
    if os.getenv("ANTHROPIC_API_KEY"):
        return LLM(model="anthropic/claude-sonnet-4-5-20250929")
    elif os.getenv("GROQ_API_KEY"):
        return LLM(model="groq/llama-3.3-70b-versatile")
    elif os.getenv("OPENAI_API_KEY"):
        return LLM(model="openai/gpt-4o")
    else:
        return LLM(model="ollama/llama3.2")


THREAT_ACTOR = "HAFNIUM"  # Change this to profile a different actor
llm = get_llm()
search_tool = TavilySearchTool()

# ─── AGENTS ───────────────────────────────────────────────────

intelligence_gatherer = Agent(
    role="Open-Source Intelligence (OSINT) Specialist",
    goal=f"Gather comprehensive threat intelligence about {THREAT_ACTOR} from public sources",
    backstory="""You specialize in open-source intelligence collection. You know where 
                 to find high-quality threat research: vendor blogs, CISA advisories, 
                 academic papers, and security conference presentations.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

ttp_analyst = Agent(
    role="TTP Extraction Specialist",
    goal=f"Extract and validate TTPs for {THREAT_ACTOR} from gathered intelligence",
    backstory="""You are an expert at parsing narrative threat intelligence and 
                 extracting precise ATT&CK mappings. You validate every technique ID 
                 against the official MITRE ATT&CK framework.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

profile_writer = Agent(
    role="Intelligence Report Writer",
    goal=f"Produce an emulation-ready threat profile for {THREAT_ACTOR}",
    backstory="""You write actionable threat intelligence reports for Red Teams. 
                 Your profiles are used directly in emulation planning.""",
    llm=llm,
    verbose=True
)

# ─── TASKS ────────────────────────────────────────────────────

gather_task = Task(
    description=f"""Search the web for recent threat intelligence on {THREAT_ACTOR}.
    
    Use the following search queries:
    1. "{THREAT_ACTOR} threat actor TTPs"
    2. "{THREAT_ACTOR} MITRE ATT&CK techniques"
    3. "{THREAT_ACTOR} malware tools infrastructure"
    4. "{THREAT_ACTOR} exchange server exploitation"
    5. "ProxyLogon HAFNIUM 2021 indicators"
    
    Collect raw intelligence from multiple sources. Prioritize vendor reports, 
    CISA advisories, and reputable security research.""",
    expected_output="""Raw intelligence collection: for each source found, include
    - Source name and URL
    - Key TTPs mentioned
    - Tools and malware
    - Any IoCs (IPs, hashes, domains)
    - Target sectors""",
    agent=intelligence_gatherer
)

extract_task = Task(
    description=f"""Using the gathered intelligence, extract and validate all TTPs for {THREAT_ACTOR}.
    
    For each TTP:
    1. Verify the ATT&CK technique ID is valid (format: T1XXX or T1XXX.XXX)
    2. Confirm the tactic category
    3. Note which sources corroborate it
    4. Rate confidence: HIGH (3+ sources), MEDIUM (2 sources), LOW (1 source)""",
    expected_output="A validated TTP table with ATT&CK IDs, names, tactics, confidence, and sources.",
    agent=ttp_analyst
)

write_task = Task(
    description=f"""Write a complete adversary profile for {THREAT_ACTOR} in Markdown.
    
    Include all standard sections: Executive Summary, Attribution, Target Sectors,
    Attack Lifecycle, Full TTP Table, Tools & Malware, IoCs, Emulation Notes, 
    Detection Opportunities, and References.""",
    expected_output="A complete, structured Markdown adversary profile.",
    agent=profile_writer
)

# ─── CREW ─────────────────────────────────────────────────────

crew = Crew(
    agents=[intelligence_gatherer, ttp_analyst, profile_writer],
    tasks=[gather_task, extract_task, write_task],
    verbose=True
)

if __name__ == "__main__":
    print(f"\n🌐 Starting live intelligence gathering for {THREAT_ACTOR}...\n")
    result = crew.kickoff()
    
    output_path = f"/home/{os.getenv('USER', 'user')}/workshop/{THREAT_ACTOR.lower()}_live_profile.md"
    with open(output_path, "w") as f:
        f.write(str(result))
    
    print(f"\n✅ Live profile saved to: {output_path}")
```

### Running the Web Search Pipeline

```bash
cd ~/workshop/threatintel-crew
python3 threatintel_web.py
```

### Discussion: PDF vs. Web Search

| Factor | PDF Pipeline | Web Search Pipeline |
|--------|-------------|---------------------|
| Data freshness | Reports from 2021 | Current (today) |
| Source control | You curate reports | AI chooses sources |
| Reproducibility | Identical every run | Varies with web content |
| Cost | Lower (fewer tokens) | Higher (many search calls) |
| Offline capability | Yes (after download) | No |
| Best for | Deep analysis of known reports | Initial reconnaissance, recent actors |

> 💡 **Best Practice:** Use both. Run the PDF pipeline on curated high-quality reports, then use the web search pipeline to check for new developments and IoCs. Compare and reconcile the outputs.

---

## 15. Validation & Critical Thinking — Spotting AI Hallucinations

This is the most important module in the course. AI-generated threat profiles can be wrong in ways that are hard to spot without domain expertise.

### Common AI Failure Modes in CTI

| Failure Type | Example | Impact |
|-------------|---------|--------|
| **Wrong ATT&CK ID** | Says T1055 (Process Injection) but describes T1190 (Exploit Public-Facing App) | Wrong emulation target |
| **Made-up tool names** | Invents a fictional malware family attributed to the threat actor | Wasted research |
| **Attribution drift** | Conflates behaviors from multiple threat actors | Wrong emulation profile |
| **Stale TTPs** | Reports TTPs the group stopped using years ago | Outdated emulation |
| **Missing sub-techniques** | Maps to parent technique (T1059) when sub-technique is documented (T1059.001) | Less precise emulation |
| **Confidence inflation** | Reports LOW-confidence observations as HIGH-confidence | Overcommitted emulation plan |

### Validation Checklist

For every AI-generated adversary profile, verify:

```
□ Each ATT&CK ID format is correct (T1XXX or T1XXX.XXX)
□ Each technique ID is verified against attack.mitre.org
□ Tool names are real and correctly attributed (search Google)
□ IoC formats are valid (IPs are valid, hashes are correct length)
□ Source reports actually say what the AI claims they say
□ Attribution matches the official ATT&CK group page
□ No fictional sub-techniques (check the parent technique page)
```

### Exercise 15.1 — Find the Errors

The following is an intentionally flawed AI output. Find at least 3 errors:

```markdown
## HAFNIUM TTP Table (FIND THE ERRORS)

| ATT&CK ID | Technique | Tactic | Evidence |
|-----------|-----------|--------|---------|
| T1190     | Exploit Public-Facing Application | Initial Access | CVE-2021-26855 |
| T1055.003 | Process Injection: Thread Execution Hijacking | Defense Evasion | Used to avoid AV detection |
| T1059.003 | Command and Scripting Interpreter: Windows Command Shell | Execution | cmd.exe usage |
| T1087     | Account Discovery | Discovery | Ran net user /domain |
| T1048.002 | Exfiltration Over Asymmetric Encrypted Non-C2 Protocol | Exfiltration | Exfiltrated via MEGA |
| T1021.006 | Remote Services: Windows Remote Management | Lateral Movement | Used WINRM |
| T1003.001 | OS Credential Dumping: LSASS Memory | Credential Access | Used ProcDump |
| T1567.002 | Exfiltration Over Web Service: Exfiltration to Code Repository | Exfiltration | Used GitHub to exfiltrate |
```

> *(Answer key available in the instructor guide. Errors include a tactic mismatch, a technique that doesn't match HAFNIUM's documented behavior, and a sub-technique attribution error.)*

---

## 16. Challenges & Extension Tasks

For students who complete the core exercises early:

### Challenge 1 — New Threat Actor (Hard)
Profile a different threat group using the same pipeline. Suggested actors: APT29 (Cozy Bear), Lazarus Group, APT41. Compare the profile quality to publicly available ATT&CK group pages.

### Challenge 2 — Custom Agent Roles (Medium)
Add a fourth agent to the synthesis crew: a **Detection Engineer** who, for each high-confidence TTP, suggests a Sigma rule or SIEM query. Consider what data sources the detection would require.

### Challenge 3 — Multi-Format Output (Medium)
Modify the Report Writer agent to produce output in two formats simultaneously: a Markdown narrative report AND a JSON-formatted ATT&CK Navigator layer file.

### Challenge 4 — Scheduled Intelligence Feed (Hard)
Wrap the web search pipeline in a cron job or scheduled task that runs weekly, appends new findings to a running intelligence file, and only reports on TTPs that are new since the last run.

### Challenge 5 — Hallucination Detection Agent (Hard)
Add a **Validation Agent** that takes the final report and verifies each ATT&CK technique ID against the live MITRE ATT&CK STIX data feed. Flag any IDs that don't exist or don't match the described behavior.

---

## 17. What Comes Next

This course covered the **intelligence consumption phase** of adversary emulation. The full lifecycle:

```
Phase 1: Intelligence Collection & Analysis     ← This course
         ↓
Phase 2: Emulation Plan Development
         (Translate TTPs to red team actions)
         ↓
Phase 3: Infrastructure Preparation
         (C2 setup, tool development, staging)
         ↓
Phase 4: Operation Execution
         (Phased execution with operator logs)
         ↓
Phase 5: Reporting & Purple Team Review
         (Compare actions to detections)
```

### Recommended Next Steps

| Resource | Focus |
|----------|-------|
| [SANS SEC565](https://www.sans.org/cyber-security-courses/red-team-operations-adversary-emulation/) | Full adversary emulation lifecycle (6 days) |
| [MITRE CALDERA](https://caldera.mitre.org/) | Automated adversary emulation platform |
| [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) | Technique-level emulation tests |
| [CrewAI Documentation](https://docs.crewai.com) | Framework reference |
| [MITRE ATT&CK](https://attack.mitre.org) | Framework reference |
| [CISA Advisories](https://www.cisa.gov/news-events/cybersecurity-advisories) | High-quality free threat reports |

---

## 18. Quick Reference & Cheatsheet

### Environment Setup (Quick Start)

```bash
# Create environment
python3 -m venv ~/workshop/venv && source ~/workshop/venv/bin/activate
pip install 'crewai[tools]' pypdf tavily-python

# Set API keys (replace with your provider)
export OPENAI_API_KEY="sk-..."
export TAVILY_API_KEY="tvly-..."

# Create directories
mkdir -p ~/workshop/threat-intel ~/workshop/threatintel-crew
```

### LLM Model Strings for CrewAI

```python
LLM(model="openai/gpt-4o")                        # OpenAI
LLM(model="anthropic/claude-sonnet-4-5-20250929") # Anthropic
LLM(model="groq/llama-3.3-70b-versatile")         # Groq (free tier)
LLM(model="google/gemini-2.0-flash")              # Google
LLM(model="ollama/llama3.2")                      # Local Ollama
```

### CrewAI Building Blocks Summary

```python
from crewai import Agent, Task, Crew, LLM
from crewai.flow.flow import Flow, listen, start
from crewai_tools import PDFSearchTool, TavilySearchTool

# Agent = specialist with role, goal, backstory, tools
# Task  = assignment with description, expected_output, agent
# Crew  = team of agents with list of tasks
# Flow  = orchestrator managing state between multiple crews
```

### ATT&CK Technique ID Format

```
T1XXX           ← Technique (e.g., T1059 — Command and Scripting Interpreter)
T1XXX.XXX       ← Sub-technique (e.g., T1059.001 — PowerShell)
```

### Key HAFNIUM ATT&CK Techniques (Reference)

| ID | Technique | Tactic |
|----|-----------|--------|
| T1190 | Exploit Public-Facing Application | Initial Access |
| T1505.003 | Server Software Component: Web Shell | Persistence |
| T1003.001 | OS Credential Dumping: LSASS Memory | Credential Access |
| T1059.001 | Command and Scripting Interpreter: PowerShell | Execution |
| T1021.006 | Remote Services: Windows Remote Management | Lateral Movement |
| T1560.001 | Archive Collected Data: Archive via Utility | Collection |
| T1048.002 | Exfiltration Over Asymmetric Encrypted Non-C2 Protocol | Exfiltration |

---

## 📎 Appendix: File Structure Reference

```
~/workshop/
├── venv/                          # Python virtual environment
├── threat-intel/                  # PDF reports for analysis
│   ├── Microsoft-HAFNIUM-report.pdf
│   ├── Mandiant-Microsoft-Exchange-Zero-Days.pdf
│   └── Volexity-Operation-Exchange-Marauder.pdf
├── threatintel-crew/              # Python scripts
│   ├── test_crewai.py             # Installation verification
│   ├── threatintel_flow.py        # Full PDF pipeline (Module 5)
│   └── threatintel_web.py         # Web search pipeline (Module 6)
├── hafnium_threat_profile.md      # Output: PDF pipeline result
└── hafnium_live_profile.md        # Output: Web search result
```

---

*Course developed for Cyber Threat Intelligence (CTI) instruction. All threat actor references are drawn from publicly available, vendor-published research. Intended for authorized educational and defensive security purposes only.*

---

> 🔗 **Course Repository:** Fork this file and track your progress. Each module's output files can be committed to your own repo as evidence of completion.
