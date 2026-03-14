# UC Student Sync Action

Automate syncing of your academic files from the UCStudent (UC) platform directly into your repository.

## Features
- Fetches all units for the current academic year.
- Recursively navigates buckets and folders.
- Downloads files into a structured directory: `downloads/academic_year/course/unit/bucket/folder/file`.
- Only downloads new files (skips existing ones).
- Ready to use as a GitHub Action.

## Setup for This Repository

1. **GitHub Secrets:**
   Go to **Settings > Secrets and variables > Actions** and add:
   - `UC_USERNAME`: Your UC student email or number.
   - `UC_PASSWORD`: Your UC student password.

2. **Wait for Sync:**
   The action is configured to run automatically every night at midnight. You can also run it manually from the **Actions** tab.

## Use in Other Repositories

You can use this action in any repository to sync files:

```yaml
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: jdsoliveira/ucsrepo-action@main
        with:
          username: ${{ secrets.UC_USERNAME }}
          password: ${{ secrets.UC_PASSWORD }}
          download_dir: 'my_academic_files'
```

## Local Setup

If you want to run it locally:

1. Clone the repo.
2. `pip install -r requirements.txt`.
3. Set environment variables:
   - `UC_USERNAME`
   - `UC_PASSWORD`
   - `DOWNLOAD_DIR` (optional, defaults to `downloads`)
4. Run `python main.py`.

## License
MIT
