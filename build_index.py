#!/usr/bin/env python3
"""Build index.html listing all reproduction reports."""

import os
import re
import glob

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Discover reports by scanning for reproduction_report.qmd files
def extract_report_metadata(qmd_path):
    """Extract title, subtitle, and verdict from a .qmd file."""
    with open(qmd_path, "r") as f:
        content = f.read()

    title_match = re.search(r'^title:\s*"(.+)"', content, re.MULTILINE)
    subtitle_match = re.search(r'^subtitle:\s*"(.+)"', content, re.MULTILINE)
    verdict_match = re.search(r'\*\*Verdict\*\*:\s*(.+)', content)

    title = title_match.group(1) if title_match else "Unknown"
    subtitle = subtitle_match.group(1) if subtitle_match else ""
    verdict = verdict_match.group(1).strip() if verdict_match else "IN PROGRESS"

    return {"title": title, "subtitle": subtitle, "verdict": verdict}


def verdict_badge(verdict):
    """Return an HTML badge for the verdict."""
    v = verdict.upper()
    if "NOT REPRODUCED" in v and "PARTIALLY" not in v:
        cls = "badge-red"
    elif "PARTIALLY" in v:
        cls = "badge-orange"
    elif "QUALITATIVELY" in v and "SUBSTANTIAL" in v.upper():
        cls = "badge-yellow"
    elif "QUALITATIVELY" in v:
        cls = "badge-blue"
    elif "COMPUTATIONALLY" in v:
        cls = "badge-green"
    else:
        cls = "badge-gray"
    return f'<span class="badge {cls}">{verdict}</span>'


def build_index():
    qmd_files = sorted(glob.glob(os.path.join(REPO_ROOT, "*/reproduction_report.qmd")))

    reports = []
    for qmd in qmd_files:
        folder = os.path.basename(os.path.dirname(qmd))
        html_path = os.path.join(os.path.dirname(qmd), "reproduction_report.html")
        has_html = os.path.exists(html_path)
        meta = extract_report_metadata(qmd)
        reports.append({
            "folder": folder,
            "has_html": has_html,
            **meta,
        })

    # Also check for folders with claim_result_mapping.md but no .qmd (in-progress)
    mapping_files = glob.glob(os.path.join(REPO_ROOT, "*/claim_result_mapping.md"))
    existing_folders = {r["folder"] for r in reports}
    for mf in mapping_files:
        folder = os.path.basename(os.path.dirname(mf))
        if folder not in existing_folders:
            reports.append({
                "folder": folder,
                "has_html": False,
                "title": f"Reproduction: {folder.upper()}",
                "subtitle": "",
                "verdict": "IN PROGRESS",
            })

    reports.sort(key=lambda r: r["folder"])

    rows = ""
    for r in reports:
        if r["has_html"]:
            link = f'<a href="{r["folder"]}/reproduction_report.html">{r["title"]}</a>'
        else:
            link = f'{r["title"]}'
        rows += f"""        <tr>
          <td>{link}</td>
          <td>{r["subtitle"]}</td>
          <td>{verdict_badge(r["verdict"])}</td>
        </tr>\n"""

    total = len(reports)
    complete = sum(1 for r in reports if r["has_html"])

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Reproduction Reports</title>
  <style>
    :root {{
      --bg: #ffffff;
      --fg: #1a1a2e;
      --muted: #6b7280;
      --border: #e5e7eb;
      --card-bg: #f9fafb;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--fg);
      line-height: 1.6;
      padding: 2rem 1rem;
      max-width: 960px;
      margin: 0 auto;
    }}
    h1 {{ font-size: 1.75rem; margin-bottom: 0.25rem; }}
    .subtitle {{ color: var(--muted); margin-bottom: 1.5rem; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--card-bg);
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border);
    }}
    th, td {{
      text-align: left;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border);
    }}
    th {{
      background: var(--fg);
      color: var(--bg);
      font-weight: 600;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: #f3f4f6; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .badge {{
      display: inline-block;
      padding: 0.2em 0.6em;
      border-radius: 4px;
      font-size: 0.8rem;
      font-weight: 600;
      white-space: nowrap;
    }}
    .badge-green {{ background: #d1fae5; color: #065f46; }}
    .badge-blue {{ background: #dbeafe; color: #1e40af; }}
    .badge-yellow {{ background: #fef3c7; color: #92400e; }}
    .badge-orange {{ background: #ffedd5; color: #9a3412; }}
    .badge-red {{ background: #fee2e2; color: #991b1b; }}
    .badge-gray {{ background: #e5e7eb; color: #374151; }}
    .banner {{
      background: #fef3c7;
      border: 2px solid #f59e0b;
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin-bottom: 1.5rem;
      font-size: 0.95rem;
      line-height: 1.5;
      color: #78350f;
    }}
    footer {{
      margin-top: 2rem;
      color: var(--muted);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <h1>AI Reproduction Reports</h1>
  <p class="subtitle">{complete} of {total} reproductions complete</p>
  <div class="banner">
    <strong>Exploratory AI Capability Study</strong><br>
    These reports were generated autonomously by an AI agent as part of an exploratory study into the capabilities of agentic AI for computational reproduction.
    <strong>They are not independent assessments of the original papers.</strong>
    The AI agent may have made errors in data processing, analytical decisions, or interpretation.
    Any discrepancies reported here may reflect limitations of the AI reproduction process rather than issues with the original research.
  </div>
  <table>
    <thead>
      <tr>
        <th>Report</th>
        <th>Paper</th>
        <th>Verdict</th>
      </tr>
    </thead>
    <tbody>
{rows}    </tbody>
  </table>
  <footer>
    Generated automatically by CI.
  </footer>
</body>
</html>
"""

    out_path = os.path.join(REPO_ROOT, "index.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Wrote {out_path} with {len(reports)} reports")


if __name__ == "__main__":
    build_index()
