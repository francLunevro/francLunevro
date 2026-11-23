"""Fetch verified public project data and rebuild the README cards."""

import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

import render

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path("data/public-activity.json")


class RefreshError(Exception):
    """GitHub data could not be refreshed safely."""


class NoRedirect(HTTPRedirectHandler):
    """Keep requests on the intended public API endpoint."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def get_json(path, params=None):
    query = f"?{urlencode(params)}" if params else ""
    request = Request(
        f"https://api.github.com{path}{query}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "francLunevro-profile-readme",
        },
    )
    opener = build_opener(NoRedirect())
    for attempt in range(3):
        try:
            with opener.open(request, timeout=15) as response:
                return json.load(response), response.headers.get("Link", "")
        except HTTPError as error:
            if error.code not in {500, 502, 503, 504}:
                raise RefreshError(f"GitHub returned HTTP {error.code}.") from None
        except (URLError, TimeoutError, OSError):
            pass
        except (ValueError, UnicodeError):
            raise RefreshError("GitHub returned unreadable JSON.") from None
        if attempt < 2:
            time.sleep(2 ** attempt)
    raise RefreshError("GitHub API did not respond successfully after three tries.")


def collect_snapshot(today, repository_name):
    if not repository_name:
        return {"week_start": None, "days": {}, "languages": {}, "primary_language": None}
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+", repository_name):
        raise RefreshError("Set PUBLIC_PROJECT_REPOSITORY to an approved public owner/repository.")
    if repository_name.rsplit("/", 1)[1] in {".", ".."}:
        raise RefreshError("The approved repository name is invalid.")
    project = f"/repos/{repository_name}"

    # Start on Sunday so the calendar stays put for a full week.
    sunday = today - timedelta(days=(today.weekday() + 1) % 7)
    start = sunday - timedelta(weeks=render.WEEKS - 1)
    repository, _ = get_json(project)
    if (
        repository["visibility"] != "public"
        or repository["private"] is not False
        or repository["full_name"].casefold() != repository_name.casefold()
    ):
        raise RefreshError("The approved project is unavailable as a public repository.")
    languages, _ = get_json(f"{project}/languages")
    if not isinstance(languages, dict) or any(
        not name.strip() or type(size) is not int or size <= 0
        for name, size in languages.items()
    ):
        raise RefreshError("GitHub returned invalid language totals.")

    days = Counter()
    seen = set()
    branch = repository["default_branch"]
    branch_info, _ = get_json(f"{project}/commits", {"sha": branch, "per_page": 1})
    if not isinstance(branch_info, list) or not branch_info:
        raise RefreshError("The public default branch has no commits.")
    tip = branch_info[0]["sha"]
    before_window = f"{(start - timedelta(days=1)).isoformat()}T23:59:59Z"
    # Pin pagination to an immutable commit so a push cannot shift pages mid-refresh.
    for page in range(1, 41):
        commits, links = get_json(
            f"{project}/commits",
            {"sha": tip, "since": before_window, "per_page": 100, "page": page},
        )
        if not isinstance(commits, list):
            raise RefreshError("GitHub returned unexpected commit data.")
        for entry in commits:
            timestamp = datetime.fromisoformat(entry["commit"]["committer"]["date"])
            day = timestamp.astimezone(timezone.utc).date()
            sha = entry["sha"]
            if start <= day <= today and sha not in seen:
                days[day.isoformat()] += 1
                seen.add(sha)
        if not re.search(r'rel="next"', links):
            break
    else:
        raise RefreshError("Commit pagination exceeded its safety limit.")

    return {
        "week_start": start.isoformat(),
        "days": dict(sorted(days.items())),
        "languages": dict(sorted(languages.items())),
        "primary_language": repository["language"],
    }


def build_files(snapshot):
    encoded = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    return {
        SNAPSHOT: encoded,
        Path("data/activity-summary.md"): render.activity_summary(snapshot),
        **render.cards(snapshot),
    }


def write_files(files, output):
    changed = []
    for relative, contents in files.items():
        path = output / relative
        data = contents.encode("utf-8")
        if path.exists() and path.read_bytes() == data:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = NamedTemporaryFile(dir=path.parent, delete=False)
        staged = Path(temporary.name)
        try:
            with temporary:
                temporary.write(data)
            staged.replace(path)
        finally:
            staged.unlink(missing_ok=True)
        changed.append(relative)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true", help="Refresh from GitHub's public REST API.")
    mode.add_argument("--offline", action="store_true", help="Render the checked-in public snapshot.")
    mode.add_argument("--check", action="store_true", help="Verify the checked-in cards without writing.")
    parser.add_argument("--output", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        if args.live:
            snapshot = collect_snapshot(
                datetime.now(timezone.utc).date(), os.environ.get("PUBLIC_PROJECT_REPOSITORY", "").strip()
            )
        else:
            snapshot = json.loads((ROOT / SNAPSHOT).read_text(encoding="utf-8"))
        files = build_files(snapshot)
        if args.check:
            for relative, contents in files.items():
                path = args.output / relative
                if not path.is_file() or path.read_bytes() != contents.encode("utf-8"):
                    raise RefreshError(f"{relative} differs from the generated version.")
            print("Generated files match the public snapshot.")
        else:
            print(f"Updated {len(write_files(files, args.output))} files.")
    except (RefreshError, OSError, KeyError, TypeError, ValueError) as error:
        # API responses and headers are intentionally excluded from the logs.
        reason = str(error) if isinstance(error, RefreshError) else "Invalid data or a local file error."
        print(f"Profile refresh failed: {reason}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
