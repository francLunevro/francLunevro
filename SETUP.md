# Set up the GitHub profile

The profile lives in the public repository **francLunevro/francLunevro**. GitHub displays its root README from the default branch after the pull request is merged.

## Verify and edit

Use Python 3.11 or later. Run these commands from the repository root.

```sh
python -m unittest discover -s scripts -v
python scripts/refresh.py --check
```

Edit `README.md` for profile copy and links, or `scripts/render.py` for the SVG artwork and chart layout. Run `python scripts/refresh.py --offline` to regenerate the cards from the checked-in data. The Validate profile workflow runs both verification commands on pull requests.

## Enable project statistics

1. In **Settings → Secrets and variables → Actions → Variables**, add `PUBLIC_PROJECT_REPOSITORY` with the value `owner/repository` for a project you approve for this profile. The project must be public.
2. On the default branch, open **Actions → Refresh profile activity → Run workflow**. The scheduled refresh also runs at **07:37 Amman time** (04:37 UTC) each day.
3. To remove the project statistics, remove the variable and run the workflow again. This restores the empty cards and data table.

The calendar counts commits reachable from the configured project's default branch, grouped by UTC committer date. It shows the current calendar week and the preceding eleven weeks. Language share uses GitHub Linguist source-byte totals. The README links directly to the separate GitHub profile contribution history.

The generator calls GitHub anonymously and checks public visibility before requesting language totals or commit history. An API failure preserves the last published charts. With no repository variable, the generator makes no API calls. The validation workflow only has `contents: read`. The refresh job uses the built-in repository token with `contents: write` to commit changed generated files after the default-branch guard passes. A repository rule that blocks that push also blocks the refresh commit.

[Profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme) · [Pinned checkout release](https://github.com/actions/checkout/releases/tag/v7.0.1)

## Design references

[Avi Vashishta’s animated cards](https://www.avivashishta.com/blog/github-profile-readme-animated-svg-cards) informed the image-embedded CSS and Python generation. [Platane’s animated calendar](https://github.com/Platane/snk) and [DenverCoder1’s profile](https://github.com/DenverCoder1) informed the use of motion to guide attention.
