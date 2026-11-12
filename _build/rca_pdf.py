"""Build the root-cause-analysis practice PDFs (questions and solutions) from content/rca/rca_questions.yaml.

    python -I -X utf8 _build/rca_pdf.py
Writes interview-preparation/RCA-Practice-Questions.pdf and RCA-Practice-Solutions.pdf.
"""
import sys, datetime
from html import escape
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
import charts

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "interview-preparation"
WORK = ROOT / "_build" / "print"
CSS = (ROOT / "_build" / "assets" / "style.css").as_uri()
DATE = datetime.date.today().strftime("%d %B %Y")
NOTICE = ("Independent practice material. All scenarios are hypothetical; company names only identify the type of product. "
          "Not affiliated with or endorsed by any company named.")
FOOTER = ('<div style="font-size:8px;width:100%;text-align:center;color:#667085;font-family:Segoe UI,Arial">'
          'RCA Interview Practice &nbsp;·&nbsp; page <span class="pageNumber"></span> of <span class="totalPages"></span></div>')

Q = yaml.safe_load((ROOT / "content" / "rca" / "rca_questions.yaml").read_text(encoding="utf-8"))
DIFF = {"Easy": "tone-g", "Medium": "tone-b", "Hard": "tone-v"}


def ul(items):
    return "<ul>" + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def ol(items):
    return "<ol>" + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ol>"


def cover(title, sub):
    return (f'<section class="cover"><div><div class="stripe"></div><h1>{escape(title)}</h1><div class="sub">{escape(sub)}</div></div>'
            f'<div class="meta">{len(Q)} root-cause-analysis scenarios · Easy / Medium / Hard<br>{DATE}<br>{escape(NOTICE)}</div></section>')


def framework():
    steps = charts.stepflow("A repeatable approach to metric-drop questions", [
        ("Clarify the metric", "Exact definition, baseline, size, timing (sudden vs gradual)"),
        ("Check the data", "Logging, pipelines, definition or dashboard changes"),
        ("Segment", "Platform, app version, region, channel, user type, step of the funnel"),
        ("Internal vs external", "Releases, experiments, pricing, outages vs competitors, seasonality, partners"),
        ("Walk the funnel", "Find the exact step where users stop"),
        ("Confirm and fix", "Root cause, immediate fix, metric to watch, prevention"),
    ], "Use it as a checklist, not a script: the best answers prioritise the checks most likely to explain the data first.", per_row=3)
    return f"""<section class="toc-page"><h1>How to use this set</h1>
<p>Each scenario is a classic <b>root-cause-analysis (RCA)</b> interview question: a metric changed and you must find out why. Practise out loud with a partner who plays the interviewer. Your partner should use the <b>Solutions PDF</b>, which lists the facts to reveal only when you ask the right question.</p>
{steps}
<h2>What interviewers look for</h2>
<table><thead><tr><th>Skill</th><th>What good looks like</th></tr></thead><tbody>
<tr><td>Clarifying</td><td>Pins down the metric definition, scope and timing before investigating</td></tr>
<tr><td>Structure</td><td>States a framework up front and returns to it as hypotheses are ruled out</td></tr>
<tr><td>Prioritisation</td><td>Checks the most likely and cheapest-to-verify causes first (data, recent releases, segments)</td></tr>
<tr><td>Data thinking</td><td>Asks for specific cuts: by platform, version, region, channel, funnel step</td></tr>
<tr><td>Conclusion</td><td>Names the root cause, an immediate fix, how to measure recovery and how to prevent recurrence</td></tr>
<tr><td>Communication</td><td>Summarises progress regularly; speaks with confident, statement-style delivery</td></tr>
</tbody></table>
<h2>Self-scoring (1–5 per row)</h2>
<table><thead><tr><th>Clarified metric</th><th>Checked data</th><th>Segmented early</th><th>Found exact step</th><th>Fix + prevention</th><th>Clear summary</th></tr></thead>
<tbody><tr><td>&nbsp;</td><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>
</section>"""


def questions_doc():
    rows = "".join(f'<tr><td>{q["id"]}</td><td>{escape(q["title"])}</td><td>{escape(q["product"])}</td><td>{q["difficulty"]}</td></tr>' for q in Q)
    body = cover("RCA Interview Practice — Questions", "24 root-cause-analysis scenarios for Product Manager interviews")
    body += framework()
    body += f'<section class="toc-page"><h1>Question list</h1><table><thead><tr><th>#</th><th>Scenario</th><th>Product type</th><th>Level</th></tr></thead><tbody>{rows}</tbody></table></section>'
    for q in Q:
        body += f"""<section class="rcaq"><h2>Q{q['id']} · {escape(q['title'])}</h2>
<div class="canvas" style="grid-template-columns:repeat(3,minmax(0,1fr))">
<div class="cv"><h5>Product</h5><p>{escape(q['product'])}</p></div>
<div class="cv"><h5>Metric</h5><p>{escape(q['metric'])}</p></div>
<div class="cv {DIFF[q['difficulty']]}"><h5>Difficulty</h5><p>{q['difficulty']}</p></div></div>
<div class="admonition example"><p class="admonition-title">Interviewer prompt</p><p>{escape(q['prompt'])}</p></div>
<details open class="note"><summary>Hints (use only if stuck)</summary>{ul(q['hints'])}</details>
<div class="notes"><p><b>Your notes</b> — clarifying questions, hypotheses, data you'd request, conclusion:</p>{'<div class="line"></div>' * 8}</div>
</section>"""
    return body


def solutions_doc():
    body = cover("RCA Interview Practice — Solutions", "Model answers, interviewer reveals and common mistakes for all 24 scenarios")
    body += """<section class="toc-page"><h1>How to use the solutions</h1>
<p>If you are the practice interviewer, read the <b>Interviewer reveals</b> before the session and share each fact only when the candidate asks a question that would uncover it. If you are self-studying, attempt the question first, then compare your path with the model path below.</p>
<p>Each model answer shows one strong path to the root cause. Other orders of investigation are fine if they are structured and prioritised. All facts are invented for practice.</p></section>"""
    for q in Q:
        body += f"""<section class="rcaq"><h2>Q{q['id']} · {escape(q['title'])}</h2>
<p class="meta-line"><b>{escape(q['product'])}</b> · Metric: {escape(q['metric'])} · {q['difficulty']}</p>
<div class="admonition example"><p class="admonition-title">Prompt</p><p>{escape(q['prompt'])}</p></div>
<h3>1. Clarifying questions to ask</h3>{ul(q['clarify'])}
<h3>2. Hypothesis buckets</h3>{ul(q['hypotheses'])}
<div class="admonition hypo"><p class="admonition-title">Interviewer reveals (share only when asked)</p>{ul(q['reveals'])}</div>
<h3>3. Model investigation path</h3>{ol(q['path'])}
<div class="admonition tip"><p class="admonition-title">Root cause</p><p>{escape(q['root_cause'])}</p></div>
<div class="canvas" style="grid-template-columns:repeat(3,minmax(0,1fr))">
<div class="cv tone-b"><h5>Fix</h5>{ul(q['fix'])}</div>
<div class="cv tone-g"><h5>Measure recovery</h5>{ul(q['measure'])}</div>
<div class="cv tone-v"><h5>Prevent recurrence</h5>{ul(q['prevention'])}</div></div>
<h3>4. Common mistakes</h3>{ul(q['mistakes'])}
<div class="admonition abstract"><p class="admonition-title">60-second answer</p><p>{escape(q['summary60'])}</p></div>
</section>"""
    return body


EXTRA_CSS = """<style>
.rcaq{break-before:page}.rcaq h2{margin-top:0;border-top:0}
.notes .line{border-bottom:1px solid #D0D5DD;height:26px}
.meta-line{color:#475467;font-size:.9rem}
.canvas{margin:10px 0}
</style>"""


def html(title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title>'
            f'<link rel="stylesheet" href="{CSS}">{EXTRA_CSS}</head><body class="print" data-theme="light"><div class="article">{body}</div></body></html>')


def render(name, title, body):
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    src = WORK / f"{name}.html"
    src.write_text(html(title, body), encoding="utf-8")
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="msedge", headless=True)
        p = b.new_page()
        p.goto(src.as_uri(), wait_until="load")
        p.emulate_media(media="print")
        p.pdf(path=str(OUT / f"{name}.pdf"), format="A4", print_background=True, display_header_footer=True,
              footer_template=FOOTER, header_template="<span></span>", outline=True, tagged=True,
              margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
        b.close()
    return OUT / f"{name}.pdf"


if __name__ == "__main__":
    for name, title, body in (("RCA-Practice-Questions", "RCA Practice — Questions", questions_doc()),
                              ("RCA-Practice-Solutions", "RCA Practice — Solutions", solutions_doc())):
        print(render(name, title, body))
