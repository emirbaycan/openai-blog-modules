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
import shutil, time, os
from pathlib import Path

def build_and_deploy_static_site(
    out_dir="frontend/out",
    active_dir="/usr/share/nginx/releases/active",
    backup_dir="/usr/share/nginx/releases/backup",
    releases_dir="releases",
    keep_releases=5,
):
    BASE_DIR = Path(__file__).parent.parent.parent.resolve()
    out_dir = (BASE_DIR / out_dir).resolve()
    releases_dir = (BASE_DIR / releases_dir).resolve()
    releases_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    new_release = releases_dir / f"site-{timestamp}"

    def is_dir_ready(p):
        return p.exists() and os.access(p, os.R_OK | os.X_OK) and any(p.iterdir())

    def safe_chmod(path, mode):
        try:
            os.chmod(path, mode)
        except Exception as e:
            print(f"[WARN] chmod failed: {e}")

    try:
        shutil.copytree(out_dir, new_release, dirs_exist_ok=True)
    except Exception as e:
        print(f"[ERROR] Failed to copy new release: {e}")
        return

    active = Path(active_dir)
    backup = Path(backup_dir)

    # LOCK dosyası ile paralel çalışmayı engelle
    lock_file = releases_dir / ".deploy_lock"
    if lock_file.exists():
        print("[ERROR] Deploy already running. Exiting.")
        return
    lock_file.touch()

    try:
        # Hangi dizin canlı?
        if is_dir_ready(active):
            print("[INFO] ACTIVE is live, updating ACTIVE, backup = BACKUP")
            if backup.exists():
                shutil.rmtree(backup)
            try:
                shutil.copytree(active, backup, dirs_exist_ok=True)
            except Exception as e:
                print(f"[ERROR] Backup failed: {e}")
                return

            # Önce içeriği temizle
            for item in active.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"[WARN] Couldn't clean active: {e}")
            try:
                shutil.copytree(new_release, active, dirs_exist_ok=True)
                safe_chmod(active, 0o755)
            except Exception as e:
                print(f"[ERROR] Copy new release to active failed: {e}")
                return

        elif is_dir_ready(backup):
            print("[INFO] BACKUP is live, updating BACKUP, backup = ACTIVE")
            if active.exists():
                shutil.rmtree(active)
            try:
                shutil.copytree(backup, active, dirs_exist_ok=True)
            except Exception as e:
                print(f"[ERROR] Restore active from backup failed: {e}")
                return

            for item in backup.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"[WARN] Couldn't clean backup: {e}")
            try:
                shutil.copytree(new_release, backup, dirs_exist_ok=True)
                safe_chmod(backup, 0o755)
            except Exception as e:
                print(f"[ERROR] Copy new release to backup failed: {e}")
                return

        else:
            print("[INFO] First deploy: active -> new_release")
            shutil.copytree(new_release, active, dirs_exist_ok=True)
            safe_chmod(active, 0o755)

        # Eski release'leri sil (keep_releases)
        all_releases = sorted(releases_dir.glob("site-*"), reverse=True)
        for old_release in all_releases[keep_releases:]:
            print(f"[*] Deleting old release: {old_release}")
            try:
                if old_release.is_symlink():
                    old_release.unlink()
                else:
                    shutil.rmtree(old_release)
            except Exception as e:
                print(f"[WARN] Delete failed for {old_release}: {e}")

        print(f"[*] ACTIVE: {active_dir}")
        print(f"[*] BACKUP: {backup_dir}")
        print("[SUCCESS] Deploy completed.")

    finally:
        # Lock dosyasını sil
        if lock_file.exists():
            lock_file.unlink()





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
