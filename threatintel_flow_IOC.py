import pysqlite3, sys
sys.modules['sqlite3'] = pysqlite3
"""
Threat Intelligence IOC Extraction Pipeline
=============================================
Reads APT PDF reports and produces a structured IOC list ready to import into MISP.
Architecture:
  Phase 1: Discover PDF files in the threat-intel directory
  Phase 2: Extract IOCs from each PDF with an isolated crew (parallel)
  Phase 3: Deduplicate and format all IOCs into a MISP-ready report
"""
import os
import asyncio
from pathlib import Path
from crewai import Agent, Task, Crew, LLM
from crewai.flow.flow import Flow, listen, start
from crewai_tools import PDFSearchTool
from pydantic import BaseModel

# ---------------------------------------------
# CONFIGURATION
# ---------------------------------------------
THREAT_INTEL_DIR = Path.home() / "workshop" / "threat-intel"
OUTPUT_FILE = Path.home() / "workshop" / "ioc_misp_report.md"


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


# ---------------------------------------------
# SHARED STATE SCHEMA
# ---------------------------------------------
class IOCExtractionState(BaseModel):
    pdf_paths: list[str] = []
    pdf_ioc_extracts: list[str] = []
    combined_iocs: str = ""
    final_report: str = ""


# ---------------------------------------------
# AGENT FACTORY FUNCTIONS
# ---------------------------------------------
def make_discovery_agent(llm):
    return Agent(
        role="Intelligence File Discoverer",
        goal="Locate all PDF threat reports in the specified directory",
        backstory="""You are a CTI operations specialist responsible for 
                     cataloguing threat intelligence reports before IOC extraction.""",
        llm=llm,
        verbose=True
    )


def make_ioc_extractor(llm, pdf_path: str):
    return Agent(
        role="IOC Extraction Specialist",
        goal=f"Extract every Indicator of Compromise present in the report: {pdf_path}",
        backstory="""You are a threat intelligence analyst specialized in extracting 
                     actionable Indicators of Compromise (IOCs) from threat reports. 
                     You are meticulous, structured, and familiar with MISP attribute 
                     types and categories.""",
        tools=[PDFSearchTool(pdf=pdf_path)],
        llm=llm,
        verbose=True
    )


def make_ioc_deduplicator(llm):
    return Agent(
        role="IOC Deduplication and Validation Analyst",
        goal="Deduplicate, validate, and consolidate all extracted IOCs across multiple reports",
        backstory="""You are a senior CTI analyst who reviews raw IOC dumps from multiple 
                     sources. You remove duplicates, fix formatting errors, and assign the 
                     correct MISP attribute type and category to each IOC so it can be 
                     imported directly into a MISP event without manual correction.""",
        llm=llm,
        verbose=True
    )


def make_misp_formatter(llm):
    return Agent(
        role="MISP Report Formatter",
        goal="Produce a clean, structured Markdown report of all IOCs ready for MISP import",
        backstory="""You produce threat intelligence reports consumed by SOC analysts 
                     who import IOCs into MISP. Your output must use exact MISP attribute 
                     types, be clearly organized by IOC category, and include a summary 
                     table that can be copy-pasted or parsed for bulk import.""",
        llm=llm,
        verbose=True
    )


# ---------------------------------------------
# CREW BUILDER FOR A SINGLE PDF
# ---------------------------------------------
def build_pdf_crew(pdf_path: str, llm) -> Crew:
    extractor = make_ioc_extractor(llm, pdf_path)

    extract_task = Task(
        description=f"""Read the PDF report at {pdf_path} and extract every Indicator 
        of Compromise (IOC) present in the document.

        Extract ALL of the following IOC types if present:
        1. IP Addresses (IPv4 and IPv6) stinguish src vs dst where context allows
        2. Domain Names and subdomains
        3. URLs and URI paths
        4. File hashes 5, SHA1, SHA256, SHA512
        5. File names and file paths associated with malware or tools
        6. Email addresses (attacker infrastructure or phishing senders)
        7. CVE identifiers (e.g. CVE-2021-26855)
        8. Registry keys associated with persistence
        9. Mutex names
        10. User-Agent strings
        11. SSL/TLS certificate fingerprints or serial numbers
        12. ASN or hosting provider details linked to attacker infrastructure

        For each IOC provide:
        - The raw IOC value (defanged if needed, e.g. 192[.]168[.]1[.]1)
        - IOC type (e.g. ip-dst, domain, md5, sha256, url, email-src, filename, regkey...)
        - MISP category (e.g. Network activity, Payload delivery, External analysis...)
        - Brief context: why this IOC appears in the report (1 sentence)
        - Source report name (filename only)""",

        expected_output="""A structured list of IOCs extracted from this report, formatted as:

        | IOC Value | Type | MISP Category | Context | Source |
        |-----------|------|---------------|---------|--------|
        | 185.220.x.x | ip-dst | Network activity | C2 server observed in campaign | report.pdf |
        | evil[.]domain[.]ru | domain | Network activity | Phishing infrastructure | report.pdf |
        | d41d8cd98f00b204e9800998ecf8427e | md5 | Payload delivery | Hash of dropper binary | report.pdf |
        ...

        Include ALL IOCs foundo not summarize or truncate.""",
        agent=extractor
    )

    return Crew(agents=[extractor], tasks=[extract_task], verbose=True)


# ---------------------------------------------
# PHASE 3: DEDUPLICATION AND MISP FORMATTING
# ---------------------------------------------
def build_synthesis_crew(combined_iocs: str, llm) -> Crew:
    deduplicator = make_ioc_deduplicator(llm)
    formatter = make_misp_formatter(llm)

    dedup_task = Task(
        description=f"""Review the following raw IOC extracts from multiple threat reports:

{combined_iocs}

Perform the following operations:
1. Remove exact duplicates (same value appearing in multiple reports)
2. Normalize IOC valuese-fang defanged IOCs for the final table 
   (e.g. 192[.]168[.]1[.]1 ? 192.168.1.1) so MISP can parse them correctly
3. Validate each IOC type against the official MISP taxonomy:
   - Network: ip-src, ip-dst, domain, hostname, url, uri
   - Files: md5, sha1, sha256, sha512, filename, filepath
   - Email: email-src, email-dst, email-subject
   - Registry: regkey, regkey|value
   - Other: vulnerability (for CVEs), mutex, user-agent, x509-fingerprint-sha1
4. Assign the most precise MISP category for each:
   - Network activity, Payload delivery, Artifacts dropped,
     External analysis, Persistence mechanism, Attribution
5. Flag high-confidence IOCs (appeared in 2+ source reports) with ?

Output a clean, deduplicated master IOC table.""",

        expected_output="""A deduplicated, validated master IOC table:

        | IOC Value | MISP Type | MISP Category | Confidence | Sources |
        |-----------|-----------|---------------|------------|---------|
        | 185.220.101.45 | ip-dst | Network activity | ? HIGH | report1.pdf, report2.pdf |
        | evil.domain.ru | domain | Network activity | MEDIUM | report1.pdf |
        ...

        Total count by type listed at the bottom.""",
        agent=deduplicator
    )

    format_task = Task(
        description="""Using the validated, deduplicated IOC master table, produce a 
complete MISP-ready Markdown report with the following structure:

1. **Report Header**
   - APT Group name
   - Date of extraction
   - Number of source reports analyzed
   - Total IOC count by type

2. **IOC Summary Table** (full deduplicated list, sorted by MISP category then type)

3. **IOCs by Category**ne subsection per MISP category:
   - Network activity (IPs, domains, URLs)
   - Payload delivery (hashes, filenames)
   - Artifacts dropped (registry keys, mutexes, paths)
   - External analysis (CVEs, certificates)
   - Attribution (email addresses, ASNs)

4. **High-Confidence IOCs** (? flagged items only) r priority import

5. **MISP Import Instructions**
   - How to create the MISP event (naming convention: YourName_APT##_AI)
   - Recommended attribute settings (IDS flag, to_ids, distribution)
   - Suggested MISP tags (tlp:white, misp-galaxy:threat-actor, etc.)

6. **Source Reports Reference List**""",

        expected_output="""A complete, well-structured Markdown document ready to guide 
a SOC analyst through importing all IOCs into MISP. All IOC values must be 
correctly formatted (not defanged) for direct copy-paste into MISP attributes.""",
        agent=formatter
    )

    return Crew(
        agents=[deduplicator, formatter],
        tasks=[dedup_task, format_task],
        verbose=True
    )


# ---------------------------------------------
# MAIN FLOW ORCHESTRATION
# ---------------------------------------------
class IOCExtractionFlow(Flow[IOCExtractionState]):
    def __init__(self):
        super().__init__()
        self.llm = get_llm()

    @start()
    def discover_files(self):
        """Phase 1: Find all PDF files in the threat-intel directory."""
        print("\n?? Phase 1: Discovering PDF reports...")

        pdf_files = list(THREAT_INTEL_DIR.glob("*.pdf"))

        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF files found in {THREAT_INTEL_DIR}. "
                "Please download APT reports before running this script."
            )

        self.state.pdf_paths = [str(p) for p in pdf_files]
        print(f"? Found {len(self.state.pdf_paths)} reports: {[p.name for p in pdf_files]}")

    @listen(discover_files)
    async def extract_iocs_parallel(self):
        """Phase 2: Extract IOCs from each PDF in parallel."""
        print(f"\n?? Phase 2: Extracting IOCs from {len(self.state.pdf_paths)} PDFs in parallel...")

        async def process_pdf(pdf_path: str) -> str:
            crew = build_pdf_crew(pdf_path, self.llm)
            result = crew.kickoff()
            return str(result)

        tasks = [process_pdf(path) for path in self.state.pdf_paths]
        extracts = await asyncio.gather(*tasks)

        self.state.pdf_ioc_extracts = list(extracts)
        self.state.combined_iocs = "\n\n---\n\n".join(
            [f"## Source Report {i+1}: {Path(path).name}\n\n{extract}"
             for i, (path, extract) in enumerate(zip(self.state.pdf_paths, extracts))]
        )

        print(f"? Phase 2 complete. IOCs extracted from {len(extracts)} reports.")

    @listen(extract_iocs_parallel)
    def deduplicate_and_format(self):
        """Phase 3: Deduplicate IOCs and produce the final MISP-ready report."""
        print("\n?? Phase 3: Deduplicating IOCs and generating MISP report...")

        crew = build_synthesis_crew(self.state.combined_iocs, self.llm)
        result = crew.kickoff()

        self.state.final_report = str(result)

        # Save to file
        OUTPUT_FILE.write_text(self.state.final_report, encoding="utf-8")
        print(f"\n? MISP-ready IOC report saved to: {OUTPUT_FILE}")
        print("\n" + "=" * 60)
        print(self.state.final_report[:2000] + "...")
        print("=" * 60)


# ---------------------------------------------
# ENTRY POINT
# ---------------------------------------------
if __name__ == "__main__":
    flow = IOCExtractionFlow()
    flow.kickoff()
