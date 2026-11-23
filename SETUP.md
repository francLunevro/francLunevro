# Profile maintenance

Run these commands from the repository root using Python 3.11 or later.

```sh
python -m unittest discover -s scripts -v
python scripts/refresh.py --check
```

Edit the profile copy in README.md and the two illustrations in scripts/render.py. Regenerate the illustrations and the optional report with `python scripts/refresh.py --offline`. The wordmark paths were drawn from Noto Serif Display Regular and Italic, so the lettering renders consistently without loading fonts. Both SVGs animate once using their own CSS and show the finished composition when reduced motion is enabled.

## Optional public project report

Configure `PUBLIC_PROJECT_REPOSITORY` under **Settings → Secrets and variables → Actions → Variables** with an `owner/repository` value you approve for public reporting. Run **Refresh profile activity** from the default branch or wait for the daily run at 07:37 Amman time (04:37 UTC). The [activity report](./data/activity-summary.md) displays default-branch commit counts and GitHub Linguist language totals when available. Remove the variable and run the workflow again to clear the project data.

The data fetch is anonymous and verifies the repository is public before retrieving commit or language totals. API failures preserve the last successful report. Validation has read-only repository access. The refresh job can write on the public default branch and only stages the two generated data files.
