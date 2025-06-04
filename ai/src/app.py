import os
import psycopg2
from src.agents.blogpostcreator import BlogPostCreator
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")


def ping_search_engines(sitemap_url):
    engines = [
        f"https://www.google.com/ping?sitemap={sitemap_url}",
        f"https://www.bing.com/ping?sitemap={sitemap_url}",
        f"https://webmaster.yandex.com/ping?sitemap={sitemap_url}",
    ]
    for url in engines:
        try:
            resp = requests.get(url, timeout=5)
            print(f"[*] Pinged: {url} - Status: {resp.status_code}")
        except Exception as e:
            print(f"[!] Ping error: {url} - {e}")


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", 5432),
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
    )


def fetch_title_by_id(title_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title FROM blog_creation_queue_blogcreationqueue
                WHERE id = %s
            """,
                (title_id,),
            )
            row = cur.fetchone()
    conn.close()
    return row  # (id, title)


def mark_title_as_processed(title_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE blog_creation_queue_blogcreationqueue
                SET processed = TRUE, processed_at = NOW()
                WHERE id = %s
            """,
                (title_id,),
            )
    conn.close()


import shutil
from pathlib import Path
import os
import time


def set_read_only(path):
    os.makedirs(path, exist_ok=True)  # Dizin yoksa oluştur!
    os.chmod(path, 0o755)  # Önce root izin!
    for root, dirs, files in os.walk(path):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), 0o755)
        for momo in files:
            os.chmod(os.path.join(root, momo), 0o644)


def set_no_read(path):
    os.makedirs(path, exist_ok=True)  # Dizin yoksa oluştur!
    os.chmod(path, 0o333)  # Önce root izin!
    for root, dirs, files in os.walk(path):
        for momo in dirs:
            os.chmod(os.path.join(root, momo), 0o333)
        for momo in files:
            os.chmod(os.path.join(root, momo), 0o222)


def is_ready(p):
    return p.exists() and any(p.iterdir())


import shutil
from pathlib import Path
import os


def log_dir_contents(path):
    print(f"[LOG] Directory contents of {path}:")
    if not os.path.exists(path):
        print("  [WARN] Path does not exist!")
        return
    for entry in os.scandir(path):
        typ = "DIR" if entry.is_dir() else "FILE"
        print(
            f"  [{typ}] {entry.name} - owner: {entry.stat().st_uid}, mode: {oct(entry.stat().st_mode)}"
        )


def build_and_deploy_static_site(
    out_dir="frontend/out",
    active_dir="/usr/share/nginx/releases/active",
    backup_dir="/usr/share/nginx/releases/backup",
):
    BASE_DIR = Path(__file__).parent.parent.resolve()
    out_dir = (BASE_DIR / out_dir).resolve()
    print(f"[INFO] Out dir: {out_dir}")

    log_dir_contents(str(out_dir))

    (BASE_DIR / "releases").mkdir(parents=True, exist_ok=True)
    active = Path(active_dir)
    backup = Path(backup_dir)
    lock_file = BASE_DIR / "releases" / ".deploy_lock"
    if lock_file.exists():
        print("[ERROR] Deploy already running. Exiting.")
        return
    lock_file.touch()

    try:
        if not is_ready(active):
            if active.exists():
                print(f"[INFO] Removing existing ACTIVE: {active}")
                shutil.rmtree(active)
            print(f"[INFO] Copying {out_dir} -> {active}")
            shutil.copytree(out_dir, active)
            set_read_only(active)
            set_no_read(backup)
            if backup.exists():
                print(f"[INFO] Cleaning and locking BACKUP: {backup}")
                shutil.rmtree(backup)
            print(f"[INFO] Wrote to ACTIVE ({active}), set read, backup is no-read.")
        elif not is_ready(backup):
            if backup.exists():
                print(f"[INFO] Removing existing BACKUP: {backup}")
                shutil.rmtree(backup)
            print(f"[INFO] Copying {out_dir} -> {backup}")
            shutil.copytree(out_dir, backup)
            set_read_only(backup)
            set_no_read(active)
            if active.exists():
                print(f"[INFO] Cleaning and locking ACTIVE: {active}")
                shutil.rmtree(active)
            print(f"[INFO] Wrote to BACKUP ({backup}), set read, active is no-read.")
        else:
            print("[ERROR] Both active and backup are filled. Clean up manually!")
            return

        print("[SUCCESS] Deploy completed.")

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        print("[FAIL] Deploy failed.")

    finally:
        if lock_file.exists():
            lock_file.unlink()
        print("[INFO] Lock file released.")


def process_title(title_id, web_references=3):
    row = fetch_title_by_id(title_id)
    if not row:
        print(f"[!] No title found with id={title_id}")
        return

    _, title = row
    print(f"[*] Generating for: {title} (id={title_id})")
    creator = BlogPostCreator(title, web_references)
    try:
        filepath = creator.create_blog_post()
        if not filepath or isinstance(filepath, Exception):
            print(f"[!] Failed to generate for: {title} -- {filepath}")
            return
        print(f"[*] Saved: {filepath}")
        mark_title_as_processed(title_id)
        build_and_deploy_static_site()

        try:
            sitemap_url = "https://blog.emirbaycan.com.tr/sitemap.xml"
            ping_search_engines(sitemap_url)
            print("[*] Search engines notified.")
        except Exception as e:
            print(f"[!] error: {e}")

    except Exception as e:
        print(f"[!] Exception for {title}: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python app.py <title_id>")
        sys.exit(1)
    title_id = int(sys.argv[1])
    process_title(title_id)
