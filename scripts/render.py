"""Render the profile's original SVG artwork without external assets."""

from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

WIDTH = 720
WEEKS = 12
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
INK = "#f1f5ff"
MUTED = "#adbcd4"
CYAN = "#89e6f7"
BLUE = "#7ba9ff"
VIOLET = "#bf9dff"
EDGE = "#2a3c5e"

STYLE = """
text{font-family:Arial,Helvetica,sans-serif}
.mono{font-family:Consolas,'Liberation Mono',monospace;letter-spacing:.045em}
.rise{animation:rise 760ms cubic-bezier(.2,.65,.3,1) both;animation-delay:var(--delay,0ms)}
.sweep{animation:sweep 1700ms 180ms ease-out both}
.trace{stroke-dasharray:100;animation:trace 1600ms 200ms ease-out both}
.reveal{transform-box:fill-box;transform-origin:left center;animation:reveal 850ms 200ms ease-out both}
@keyframes rise{from{opacity:.15;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}
@keyframes sweep{from{opacity:0;transform:translateX(-335px)}35%{opacity:1}to{opacity:0;transform:translateX(610px)}}
@keyframes trace{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
@keyframes reveal{from{opacity:.25;transform:scaleX(.02)}to{opacity:1;transform:scaleX(1)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.sweep{opacity:0}}
"""


def label(x, y, value, size, fill=INK, *, weight=400, mono=False):
    cls = ' class="mono"' if mono else ""
    return (
        f'<text{cls} x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}">{escape(str(value))}</text>'
    )


def group(contents, delay=0):
    return f'<g class="rise" style="--delay:{delay}ms">{contents}</g>'


def tag(x, y, value, color=CYAN):
    return label(x, y, value, 17, color, weight=700, mono=True)


def rect(x, y, width, height, color, radius=0, stroke="none"):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
        f'fill="{color}" stroke="{stroke}"/>'
    )


def frame(height, title, description, body, definitions=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
<defs>
  <linearGradient id="panel" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop stop-color="#10192b"/><stop offset=".62" stop-color="#0a1020"/><stop offset="1" stop-color="#13112b"/>
  </linearGradient>
  <linearGradient id="signal" x1="0%" y1="100%" x2="100%" y2="0%">
    <stop stop-color="#64dcf7"/><stop offset=".54" stop-color="#769bff"/><stop offset="1" stop-color="#bb91ff"/>
  </linearGradient>
  <clipPath id="bounds"><rect x="1" y="1" width="718" height="{height - 2}" rx="23"/></clipPath>
  {definitions}
</defs>
<style>{STYLE}</style>
<rect x="1" y="1" width="718" height="{height - 2}" rx="23" fill="url(#panel)" stroke="{EDGE}"/>
<g clip-path="url(#bounds)">
{body}
</g>
</svg>
"""


def hero():
    definitions = """
    <radialGradient id="field">
      <stop stop-color="#413ac7" stop-opacity=".4"/><stop offset="1" stop-color="#272f81" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 H 0 V 24" fill="none" stroke="#87a6ee" stroke-opacity=".17"/>
    </pattern>
    <linearGradient id="fade"><stop stop-color="white" stop-opacity="0"/><stop offset="1" stop-color="white"/></linearGradient>
    <mask id="grid-fade"><rect x="280" width="440" height="314" fill="url(#fade)"/></mask>
    <linearGradient id="gleam">
      <stop stop-color="white" stop-opacity="0"/><stop offset=".56" stop-color="#d5fbff" stop-opacity=".7"/><stop offset="1" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <mask id="word" maskUnits="userSpaceOnUse" x="33" y="132" width="352" height="88"><text x="34" y="205" font-size="75" font-weight="800" letter-spacing="-3.1" fill="white">Lunevro</text></mask>
    """
    art = """
    <ellipse cx="552" cy="149" rx="243" ry="190" fill="url(#field)"/>
    <rect x="280" width="440" height="314" fill="url(#grid)" mask="url(#grid-fade)"/>
    <g fill="none" stroke-width="1.4">
      <path d="M366 158 543 55l177 103-177 103Z" stroke="#34517f"/>
      <path d="M390 158 543 69l152 89-152 89Z" stroke="#46659c"/>
      <path d="M417 158 543 86l126 72-126 74Z" stroke="#6085be"/>
      <path d="M366 158h354M543 29v260M446 95l194 124M446 219l194-124" stroke="#6281bc" opacity=".37"/>
      <path class="trace" pathLength="100" d="m390 158 153-89 152 89-152 89-153-89" stroke="url(#signal)" opacity=".85"/>
      <path d="m438 158 105-61 104 61-104 62Z" stroke="#7196df" opacity=".6"/>
    </g>
    <path d="m474 141 69-40 70 40-70 40Z" fill="#233a74" stroke="#86b6ff" stroke-width="1.5"/>
    <path d="m474 141 69 40v61l-69-40Z" fill="#14264d" stroke="#5f87d3" stroke-width="1.5"/>
    <path d="m543 181 70-40v61l-70 40Z" fill="#28285d" stroke="#8b82e9" stroke-width="1.5"/>
    <path d="m491 141 52-30 53 30-53 30Z" fill="#192953" stroke="url(#signal)" stroke-width="1.4"/>
    <path d="m513 141 30-17 31 17-31 18Z" fill="#9eafff" fill-opacity=".26" stroke="#a9bcff" stroke-width="1.3"/>
    <path d="m489 169 39 23m-39-13 28 16m-28-6 39 23m32-17 36-22m-36 32 22-13m-22 23 36-22" fill="none" stroke="#7da2ed" stroke-opacity=".55" stroke-width="2" stroke-linecap="round"/>
    <circle cx="390" cy="158" r="3" fill="#81e6f8"/><circle cx="695" cy="158" r="3" fill="#b598ff"/>
    <circle cx="543" cy="69" r="3.5" fill="#c0a6ff"/><circle cx="543" cy="247" r="3.5" fill="#6ddff6"/>
    <path d="M657 46h18v18M657 265h18v-18" fill="none" stroke="#5477b1" stroke-width="1.4"/>
    """
    headline = """
    <text x="34" y="130" fill="#f1f5ff" font-size="75" font-weight="800" letter-spacing="-3.1">Franc</text>
    <text x="34" y="205" fill="url(#signal)" font-size="75" font-weight="800" letter-spacing="-3.1">Lunevro</text>
    <g mask="url(#word)"><rect class="sweep" x="8" y="136" width="215" height="78" fill="url(#gleam)" opacity="0"/></g>
    """
    intro = (
        tag(38, 52, "@FRANCLUNEVRO")
        + group(headline)
        + group(label(38, 253, "Discord bots · backend systems", 24, MUTED), 120)
        + group(label(38, 281, "Web dashboards", 24, MUTED), 180)
        + '<path d="M39 298h70" fill="none" stroke="url(#signal)" stroke-width="2" stroke-linecap="round"/>'
    )
    return frame(314, "Franc Lunevro", "@francLunevro builds Discord bots, backend systems, and web dashboards.", art + intro, definitions)


def stack():
    panels = []
    items = (
        (32, "BACKEND", ("JavaScript", "Node.js · discord.js", "Express · SQLite"), CYAN, "m0 12 11-10 11 10-11 10Z M11 22v8"),
        (369, "WEB & DELIVERY", ("React · Vite", "GitHub Actions", "Docker"), VIOLET, "M1 4h21v15H1Z M6 25h11 M11 19v6"),
    )
    for index, (x, name, tools, accent, icon) in enumerate(items):
        tile = rect(x, 27, 319, 157, "#141e36", 15, EDGE)
        tile += rect(x + 18, 47, 38, 36, "#202e4c", 9)
        tile += f'<path d="{icon}" transform="translate({x + 25} 51)" fill="none" stroke="{accent}" stroke-width="1.55" stroke-linejoin="round"/>'
        tile += tag(x + 68, 69, name, accent)
        for line, tool in enumerate(tools):
            tile += label(x + 20, 110 + 28 * line, tool, 24, INK if line == 0 else MUTED, weight=700 if line == 0 else 400)
        panels.append(group(tile, index * 100))
    return frame(211, "Technical stack", "Backend, web, and delivery tools.", "".join(panels))


def activity(snapshot):
    if snapshot["week_start"] is None:
        body = tag(34, 42, "PUBLIC REPOSITORY ACTIVITY")
        body += label(32, 91, "Public commit calendar", 43, INK, weight=800)
        body += label(34, 133, "Activity charts appear when a public project is configured.", 22, MUTED)
        body += label(34, 166, "View GitHub contribution history →", 22, CYAN, weight=700)
        return frame(191, "Public commit calendar", "Activity charts appear when a public project is configured.", body)

    start = date.fromisoformat(snapshot["week_start"])
    days = snapshot["days"]
    total, active, peak = sum(days.values()), len(days), max(days.values(), default=0)
    labels = tag(34, 42, "PUBLIC REPOSITORY ACTIVITY")
    labels += label(32, 91, "Public commit calendar", 43, INK, weight=800)
    labels += label(34, 124, f"Default branch · {WEEKS} weeks · UTC", 22, MUTED)
    for x, metric, caption in (
        (34, total, "Commits"),
        (256, active, "Active days"),
        (480, peak, "Peak in a day"),
    ):
        labels += label(x, 186, f"{metric:,}", 44, CYAN, weight=800)
        labels += label(x, 214, caption, 23, MUTED)

    palette = ("#253555", "#4269af", "#608df1", "#86adff", "#a7edff")
    graph = label(34, 273, "Sun", 18, MUTED)
    graph += label(34, 322, "Wed", 18, MUTED)
    graph += label(34, 370, "Sat", 18, MUTED)
    last_month = None
    for week in range(WEEKS):
        first = start + timedelta(weeks=week)
        x = 107 + week * 48
        month = MONTHS[first.month - 1]
        if month != last_month:
            graph += label(x, 245, month, 19, MUTED)
            last_month = month
        column = []
        for offset in range(7):
            day = first + timedelta(days=offset)
            count = days.get(day.isoformat(), 0)
            level = sum(count >= threshold for threshold in (1, 2, 4, 8))
            cell = rect(x, 260 + 16 * offset, 38, 12, palette[level], 3)
            accessible = f"{day.isoformat()} · {count} commits"
            cell = cell.replace("/>", f"><title>{accessible}</title></rect>")
            column.append(cell)
        graph += group("".join(column), 35 * week)

    graph += label(34, 416, "No commits", 17, MUTED)
    for level, color in enumerate(palette):
        graph += rect(132 + level * 22, 402, 17, 14, color, 3)
    graph += label(247, 416, "8+ in a day", 17, MUTED)
    graph += label(496, 416, "Contribution history →", 17, CYAN, weight=700)
    return frame(443, "Public commit activity", f"{total} commits across {active} days, with a peak of {peak} commits in one day. The calendar starts {start.isoformat()}.", labels + graph)


def languages(snapshot):
    heading = tag(34, 44, "PUBLIC PROJECT · SOURCE LANGUAGES")
    heading += label(33, 88, "Language breakdown", 40, INK, weight=800)
    if snapshot["week_start"] is None:
        body = label(34, 134, "Source byte totals appear when a public project is configured.", 22, MUTED)
        return frame(165, "Public project source languages", "Source byte totals appear when a public project is configured.", heading + body)
    languages = snapshot["languages"]
    if not languages:
        body = label(34, 134, snapshot["primary_language"] or "Pending", 29, CYAN, weight=700)
        body += label(34, 165, "GitHub has not reported byte totals", 22, MUTED)
        return frame(191, "Public project source languages", "GitHub has not reported source byte totals for this project.", heading + body)

    ranked = sorted(languages.items(), key=lambda pair: (-pair[1], pair[0]))
    if len(ranked) > 4:
        ranked = ranked[:3] + [("Other", sum(size for _, size in ranked[3:]))]
    total = sum(languages.values())
    colors = (BLUE, VIOLET, CYAN, "#94aaca")
    body = label(34, 122, "GitHub Linguist · share of source bytes", 22, MUTED)
    x = 34
    for index, (name, size) in enumerate(ranked):
        y = 191 + 34 * index
        share = 100 * size / total
        display = "<0.1%" if share < .05 else f"{share:.1f}%"
        width = 652 * size / total
        if width >= .06:
            body += f'<g class="reveal">{rect(f"{x:.2f}", 143, f"{width:.2f}", 14, colors[index])}</g>'
        x += width
        body += rect(34, y - 15, 15, 15, colors[index], 4)
        body += label(64, y, name, 23, INK)
        body += label(550, y, display, 23, MUTED, mono=True)
    desc = ", ".join(f"{name} {100 * size / total:.1f} percent" for name, size in ranked)
    return frame(189 + 34 * len(ranked), "Public project source languages", desc, heading + body)


def cards(snapshot):
    images = {
        "hero": hero(),
        "stack": stack(),
        "activity": activity(snapshot),
        "languages": languages(snapshot),
    }
    return {Path("assets") / f"{name}.svg": svg for name, svg in images.items()}


def activity_summary(snapshot):
    if snapshot["week_start"] is None:
        return "# Public project activity\n\nActivity charts appear when a public project is configured.\n"
    start = date.fromisoformat(snapshot["week_start"])
    end = start + timedelta(weeks=WEEKS, days=-1)
    days = snapshot["days"]
    lines = [
        "# Public project activity",
        "",
        f"Default-branch commit window from {start} through {end} (UTC).",
        "",
        f"**{sum(days.values()):,} commits · {len(days)} active days · "
        f"{max(days.values(), default=0):,} commits on the busiest day.**",
        "",
        "## Commits by active day",
        "",
        "| UTC date | Commits |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {day} | {count:,} |" for day, count in sorted(days.items()))
    if not days:
        lines += ["", "No commits in this window."]
    lines += ["", "## Languages by source bytes", ""]
    if snapshot["languages"]:
        lines += ["| Language | Bytes |", "| --- | ---: |"]
        for language, size in sorted(snapshot["languages"].items(), key=lambda item: (-item[1], item[0])):
            safe_language = escape(language).replace("|", "&#124;").replace("\n", " ")
            lines.append(f"| {safe_language} | {size:,} |")
    else:
        lines.append("GitHub has not reported source byte totals for this project.")
    return "\n".join(lines) + "\n"
