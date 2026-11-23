"""Render the profile illustrations and the public-project report."""

from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ART = Path(__file__).resolve().parents[1] / "assets"
WEEKS = 12


def svg(height, title, description, body, css):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" viewBox="0 0 760 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
<style>
{css}
@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; }}
}}
</style>
{body}
</svg>
"""


def hero():
    css = """
.label { font: 24px Arial, Helvetica, sans-serif; }
.rule { stroke-dasharray: 100; animation: rule 900ms 160ms cubic-bezier(.22,.7,.26,1) both; }
@keyframes rule { from { stroke-dashoffset: 100; } to { stroke-dashoffset: 0; } }
""".strip()
    wordmark = (ART / "wordmark.path").read_text(encoding="utf-8").strip().splitlines()
    body = f"""<path fill="#142934" d="M0 0H760V181H0z"/>
<text class="label" x="33" y="43" fill="#bad0cb">@francLunevro</text>
<g fill="#f3f2e9">
  <path d="{wordmark[0]}" transform="translate(29 130) scale(.073 -.073)"/>
  <path d="{wordmark[1]}" transform="translate(244 130) scale(.073 -.073)"/>
</g>
<path fill="none" stroke="#64828a" d="M34 151.5H725"/>
<path class="rule" pathLength="100" fill="none" stroke="#db9a73" stroke-width="2.5" d="M34 151.5H213"/>"""
    return svg(181, "Franc Lunevro", "GitHub profile of Franc Lunevro, @francLunevro.", body, css)


def ticket():
    css = """
.serif { font-family: Georgia, 'Times New Roman', serif; }
.sans { font-family: Arial, Helvetica, sans-serif; }
.route { transform-origin: 220px 245px; animation: trace 700ms 320ms ease-out both; }
.slip { animation: file 980ms 850ms cubic-bezier(.25,.65,.35,1) both; }
.stamp { transform-origin: 599px 293px; animation: ink 260ms 1660ms ease-out both; }
@keyframes trace {
  from { transform: scaleX(0); } to { transform: scaleX(1); }
}
@keyframes file {
  0% { transform: translate(-360px, 22px) rotate(-8deg); opacity: 0; }
  20% { opacity: 1; }
  53% { transform: translate(-147px, -57px) rotate(-5deg); }
  80% { transform: translate(-26px, -28px) rotate(-2deg); }
  100% { transform: none; }
}
@keyframes ink {
  from { opacity: 0; transform: scale(1.15); }
  to { opacity: 1; transform: scale(1); }
}
""".strip()
    body = """
<defs>
  <pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse">
    <path d="M-1 7 7-1M6 8l2-2" stroke="#5b716f" stroke-opacity=".43" stroke-width=".9"/>
  </pattern>
  <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">
    <path d="M2 2h.15" stroke="#7b9492" stroke-width="1.25" stroke-linecap="round"/>
  </pattern>
  <clipPath id="trail-edge">
    <rect class="route" x="216" y="147" width="279" height="119"/>
  </clipPath>
</defs>
<path fill="#e8eee7" d="M0 0H760V400H0z"/>
<path fill="none" stroke="#73918c" d="M32 84.5H728M32 345.5H728"/>
<text class="serif" x="31" y="58" fill="#19333b" font-size="37">The record stays.</text>

<!-- Open ticket with paper edges, handwritten message marks and a perforated counterfoil. -->
<g transform="rotate(-6 134 225)" stroke="#294750" stroke-linecap="round" stroke-linejoin="round">
  <path d="m58 140 154 2 2 167-155 4-2-89 10-9-10-9Z" fill="#a5bbb1" stroke="none"/>
  <path d="m54 135 155 2 2 167-155 4-2-89c12-1 13-16 0-18Z" fill="#f6f4e9" stroke-width="2"/>
  <path d="m60 143 139 1m-137 153 135-3" fill="none" stroke="#9aaea5" stroke-width="1"/>
  <path d="M70 261c38 .5 78-.8 123-2" stroke-dasharray="2 5" fill="none"/>
  <path d="M72 162v28l25 .5v-4l9 5-1-28Z" fill="#d7e3db" stroke-width="1.4"/>
  <path d="m78 173 18 .4m-18 6 14 .1" fill="none" stroke-width="1.1"/>
  <path d="M117 169c22-1 44-1 72 0m-69 9c19-1 35-.7 57-.4m-59 10c26-1 42-.7 66-.6m-113 22c36-1 79-1 119-.1m-118 11c30-.8 62-.8 92-.6m-89 13c42-1 66-.9 99-.4m-101 10 70-.7" fill="none" stroke="#55716f" stroke-width="1.6"/>
  <path d="M73 274v12m4-12v12m3-12-.2 12m7-12v12m4-12v12m4-12v12m6-12v12m2-12v12m5-12v12m5-12v12m6-12v12m3-12v12m6-12v12" fill="none" stroke-width="1.15"/>
</g>

<!-- The dashed route maps the movement from the ticket to the archive. -->
<g fill="none" stroke="#48716e" stroke-linecap="round" clip-path="url(#trail-edge)">
  <path d="M222 239c63-50 128-82 211-42" stroke-width="2" stroke-dasharray="2 7"/>
  <path d="m424 187 11 11-15 3" stroke-width="1.6"/>
</g>

<!-- A folder with a thumb notch. The foreground lip covers the moving transcript. -->
<g stroke="#294750" stroke-linejoin="round">
  <path d="m463 150 196 7 43 21-6 141-239-9Z" fill="#a6bcb4" stroke="none"/>
  <path d="m456 155 13-19 68 3 13 19 138 7-8 148-230-10Z" fill="#aec3b9" stroke-width="2"/>
  <path d="m466 154 67 3 13 16 132 5m-214 6-4 106 210 10" fill="none" stroke="#5e817c" stroke-width="1.15"/>
  <path d="m459 175 224 10-3 87-225-9Z" fill="url(#hatch)" stroke="none"/>
</g>
<g class="slip">
  <g transform="rotate(8 576 188)" stroke="#294750" stroke-linecap="round" stroke-linejoin="round">
    <path d="M513 123h116l22 22v118H513Z" fill="#f7f4e8" stroke-width="2"/>
    <path d="M629 123v21l22 1Z" fill="#dbe5dd" stroke-width="1.5"/>
    <path d="M527 148h71m-71 12h91m-91 13h75m-75 12h102m-102 12h87m-87 12h73m-73 12h96" fill="none" stroke="#537471" stroke-width="1.65"/>
    <path d="M527 138h26" stroke="#a7462b" stroke-width="2"/>
  </g>
</g>
<g stroke="#294750" stroke-linecap="round" stroke-linejoin="round">
  <path d="m447 217 55 2c6 18 26 19 33 2l156 7-12 89-238-12Z" fill="#d5e3d9" stroke-width="2"/>
  <path d="m450 294 224 11m-222-73-4 57m231-53-7 57" fill="none" stroke="#6e8f88" stroke-width="1"/>
  <path d="m462 241 72 3-4 34-72-3Z" fill="url(#dots)" stroke="none"/>
</g>
<g class="stamp" fill="#8c3526">
  <g transform="rotate(5 603 276)">
    <path d="m551 257 105 1-1 36-105-1Z" fill="none" stroke="#8c3526" stroke-width="2"/>
    <path d="m555 261 97 .7-.7 27.6-97-.5Z" fill="none" stroke="#8c3526" stroke-width=".7"/>
    <text class="sans" x="604" y="283" text-anchor="middle" font-size="19" font-weight="700" letter-spacing="1.7">SAVED</text>
  </g>
</g>

<text class="sans" x="37" y="377" fill="#244751" font-size="26">Support ticket</text>
<text class="sans" x="724" y="377" text-anchor="end" fill="#244751" font-size="26">Ticket transcript</text>
""".strip()
    return svg(
        400, "The record stays",
        "A support ticket on the left becomes a written transcript filed in an archive on the right.",
        body, css,
    )


def artwork():
    return {Path("assets/hero.svg"): hero(), Path("assets/ticket.svg"): ticket()}


def activity_summary(snapshot):
    heading = [
        "# GitHub activity", "",
        "[Contribution history](https://github.com/francLunevro#contribution-activity) · "
        "[Public repositories](https://github.com/francLunevro?tab=repositories)", "",
    ]
    if snapshot["week_start"] is None:
        return "\n".join(heading)

    start = date.fromisoformat(snapshot["week_start"])
    end = start + timedelta(weeks=WEEKS, days=-1)
    days = snapshot["days"]
    lines = heading + [
        "## Public project commits", "",
        f"Default-branch commit window from {start} through {end} (UTC).", "",
    ]
    if days:
        lines += [
            f"**{sum(days.values()):,} commits across {len(days)} active days.**", "",
            "| UTC date | Commits |", "| --- | ---: |",
        ]
        lines.extend(f"| {day} | {count:,} |" for day, count in sorted(days.items()))
    else:
        lines.append("No commits in this window.")
    if snapshot["languages"]:
        lines += ["", "## Languages by source bytes", "", "| Language | Bytes |", "| --- | ---: |"]
        for language, size in sorted(snapshot["languages"].items(), key=lambda item: (-item[1], item[0])):
            safe_language = escape(language).replace("|", "&#124;").replace("\n", " ")
            lines.append(f"| {safe_language} | {size:,} |")
    return "\n".join(lines) + "\n"
