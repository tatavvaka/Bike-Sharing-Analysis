"""Audit berkas, catat URL deployment, dan buat ZIP submission Bike Sharing.

Jalankan dari proyek: python scripts/finalize_submission.py prepare
Setelah commit:      python scripts/finalize_submission.py zip
Hanya memakai pustaka standar Python. Pemeriksaan URL mencakup formatnya;
akses publik dan perilaku dashboard harus diperiksa di browser.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'notebook.ipynb', 'README.md', 'requirements.txt',
    'data/day.csv', 'data/hour.csv', 'dashboard/dashboard.py',
    'dashboard/analysis.py', '.streamlit/config.toml',
)
ROOT_FILES = ('notebook.ipynb', 'README.md', 'requirements.txt', 'url.txt', '.gitignore')
INCLUDED_DIRS = ('data', 'dashboard', 'docs', 'outputs', 'tests', 'scripts')
EXTENSIONS = {'.csv', '.txt', '.md', '.py', '.json', '.png', '.jpg', '.jpeg', '.svg'}
EXCLUDED_PARTS = {'.git', '.venv', 'venv', '__pycache__', '.ipynb_checkpoints', 'dist'}


class CheckError(Exception):
    pass


def source_text(cell):
    value = cell.get('source', '')
    return ''.join(value) if isinstance(value, list) else value


def validate_url(value):
    value = value.strip()
    parsed = urlsplit(value)
    host = parsed.hostname or ''
    valid_host = re.fullmatch(r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.streamlit\.app', host)
    if (parsed.scheme != 'https' or not valid_host or parsed.netloc != host
            or parsed.path not in ('', '/')):
        raise CheckError('Gunakan URL aplikasi HTTPS pada domain .streamlit.app. '
                         'Salin dari aplikasi yang sudah terbuka, bukan dari GitHub atau localhost.')
    return f'https://{host}/'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root, require_url=False):
    missing = [name for name in REQUIRED if not (root / name).is_file()]
    if missing:
        raise CheckError('Berkas belum ditemukan: ' + ', '.join(missing))
    notebook = json.loads((root / 'notebook.ipynb').read_text(encoding='utf-8-sig'))
    cells = notebook.get('cells', [])
    code = [c for c in cells if c.get('cell_type') == 'code' and source_text(c).strip()]
    if not code:
        raise CheckError('Notebook tidak memiliki sel kode.')
    if any(c.get('execution_count') is None for c in code):
        raise CheckError('Ada sel kode yang belum dijalankan. Run all, simpan, lalu gunakan notebook terbaru.')
    errors = sum(o.get('output_type') == 'error' for c in code for o in c.get('outputs', []))
    if errors:
        raise CheckError(f'Notebook menyimpan {errors} output error. Perbaiki dan jalankan ulang.')
    images = sum(any(k in o.get('data', {}) for k in ('image/png', 'image/svg+xml', 'image/jpeg'))
                 for c in code for o in c.get('outputs', []))
    if images < 2:
        raise CheckError('Diperlukan minimal dua grafik tersimpan dalam output notebook.')
    markdown = '\n'.join(source_text(c) for c in cells if c.get('cell_type') == 'markdown')
    sections = ['Menentukan Pertanyaan Bisnis', 'Gathering Data', 'Assessing Data',
                'Cleaning Data', 'Exploratory Data Analysis', 'Visualization',
                'Analisis Lanjutan', 'Conclusion', 'Recommendation']
    absent = [s for s in sections if s.casefold() not in markdown.casefold()]
    if absent:
        raise CheckError('Periksa bagian notebook: ' + ', '.join(absent))
    first = source_text(cells[0])
    for field in ('Nama', 'Email', 'ID Dicoding'):
        match = re.search(r'\*\*' + re.escape(field) + r':\*\*\s*([^\n]+)', first, re.I)
        if not match or not match.group(1).strip() or '[' in match.group(1):
            raise CheckError(f'Lengkapi identitas {field} pada awal notebook.')
    stats = {}
    for filename, expected_rows in [('day.csv', 731), ('hour.csv', 17379)]:
        path = root / 'data' / filename
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            required = {'dteday', 'cnt', 'casual', 'registered', 'workingday', 'hum'}
            if filename == 'hour.csv':
                required.add('hr')
            if not required.issubset(reader.fieldnames or []):
                raise CheckError(f'Kolom {filename} tidak sesuai dataset proyek.')
            rows = list(reader)
        if len(rows) != expected_rows:
            raise CheckError(f'{filename}: ditemukan {len(rows)} baris; sumber proyek berisi {expected_rows}. '
                             'Gunakan CSV sumber pada folder data; simpan hasil cleaning di data/processed.')
        total = 0
        for row in rows:
            count = int(row['cnt'])
            if count < 0 or count != int(row['casual']) + int(row['registered']):
                raise CheckError(f'Jumlah penyewaan tidak konsisten pada {filename}.')
            total += count
        stats[filename] = {'rows': len(rows), 'total_rentals': total, 'sha256': sha256(path)}
    if stats['day.csv']['total_rentals'] != stats['hour.csv']['total_rentals']:
        raise CheckError('Total penyewaan pada CSV harian dan per jam berbeda.')
    for path in (root / 'dashboard').rglob('*.py'):
        if '__pycache__' not in path.parts:
            compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    requirements = (root / 'requirements.txt').read_text(encoding='utf-8-sig').lower()
    for name in ('streamlit', 'pandas', 'numpy', 'matplotlib'):
        if not re.search(r'^' + name + r'\b', requirements, re.M):
            raise CheckError(f'{name} belum tercantum dalam requirements.txt.')
    readme = (root / 'README.md').read_text(encoding='utf-8-sig')
    if 'streamlit run dashboard/dashboard.py' not in readme:
        raise CheckError('README perlu mencantumkan perintah menjalankan dashboard/dashboard.py.')
    url = None
    if require_url:
        if not (root / 'url.txt').is_file():
            raise CheckError('url.txt belum tersedia. Jalankan perintah prepare setelah deployment.')
        url = validate_url((root / 'url.txt').read_text(encoding='utf-8-sig'))
    return {'code_cells': len(code), 'saved_figures': images, 'saved_errors': errors,
            'data': stats, 'url': url, 'notebook_sha256': sha256(root / 'notebook.ipynb')}


def replace_block(text, key, body):
    begin, end = f'<!-- {key}:BEGIN -->', f'<!-- {key}:END -->'
    block = f'{begin}\n{body.strip()}\n{end}'
    if begin in text and end in text:
        before, rest = text.split(begin, 1)
        _, after = rest.split(end, 1)
        return before + block + after
    return text.rstrip() + '\n\n' + block + '\n'


def prepare(root, url):
    audit(root)
    url = validate_url(url)
    now = datetime.now(timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M WIB')
    (root / 'url.txt').write_text(url + '\n', encoding='utf-8')
    readme_path = root / 'README.md'
    readme = readme_path.read_text(encoding='utf-8-sig')
    old_status = ('**Status:** analisis tahap 1–6 telah terisi. Dashboard tahap 7 tersedia dan lulus 11 tes otomatis.\n'
                  'Pemeriksaan browser pada Windows dicatat pada checklist pengujian. Deployment dan audit submission\n'
                  'akhir dilanjutkan pada tahap 8.')
    new_status = ('**Status:** analisis dan dashboard tersedia. URL aplikasi dicatat pada bagian Dashboard online.\n'
                  'Bukti pemeriksaan akhir dicatat pada docs/checklist_final.md dan docs/audit_otomatis.md.')
    readme = readme.replace(old_status, new_status)
    readme = readme.replace('- Deployment dan URL publik: tahap 8, belum dicantumkan sebagai hasil selesai.',
                            '- URL aplikasi: lihat bagian Dashboard online dan url.txt.')
    readme = replace_block(readme, 'DEPLOYMENT_TAHAP8', f'''## Dashboard online

[Buka dashboard Bike Sharing]({url})

Repository: https://github.com/tatavvaka/Bike-Sharing-Analysis.
Entrypoint: `dashboard/dashboard.py`. Gunakan Python 3.12 di Advanced settings saat deployment.
Aplikasi membaca `data/day.csv` dan `data/hour.csv`; modul `dashboard/analysis.py` ikut diperlukan.

URL dicatat pada {now}. Pemeriksaan akses publik, filter, grafik, dan unduhan dilakukan
melalui browser dan dicatat pada [checklist akhir](docs/checklist_final.md).
Hasil pemeriksaan berkas: [audit otomatis](docs/audit_otomatis.md).

Sesudah dokumentasi di-commit, buat ZIP dengan:

```bat
.venv\\Scripts\\python.exe scripts/finalize_submission.py zip
```

Hasil: `dist/Submission_Bike_Sharing_Tata_Ivanka.zip`.
ZIP memuat dataset, notebook beserta output, kode dashboard, requirements, README,
URL aplikasi, serta dokumentasi proyek. Paket tahap 7/8 adalah bahan kerja dan tidak
digunakan sebagai pengganti ZIP submission ini.''')
    readme_path.write_text(readme, encoding='utf-8')
    # Ubah hanya paragraf status yang diketahui pada sel Markdown terakhir.
    nb_path = root / 'notebook.ipynb'
    nb = json.loads(nb_path.read_text(encoding='utf-8-sig'))
    old = ('**Status:** Tahap 1–6 telah terisi dan dijalankan pada versi ini. Pembuatan dashboard Streamlit, '
           'pengujian lokal, deployment, dan audit submission akhir menjadi tahap berikutnya.')
    for cell in reversed(nb['cells']):
        if cell.get('cell_type') == 'markdown':
            src = source_text(cell)
            if old in src:
                updated = src.replace(old, '**Status:** Analisis tahap 1–6 telah terisi dan dijalankan. '
                    'Dashboard tersedia pada folder dashboard; URL aplikasi dicatat dalam url.txt. '
                    'Dokumentasi pemeriksaan akhir tersedia pada docs/checklist_final.md dan docs/audit_otomatis.md.')
                cell['source'] = updated.splitlines(keepends=True) if isinstance(cell['source'], list) else updated
                nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
            break
    docs = root / 'docs'; docs.mkdir(exist_ok=True)
    progress_path = docs / 'progress.md'
    progress = progress_path.read_text(encoding='utf-8-sig') if progress_path.exists() else '# Catatan progres proyek\n'
    progress = replace_block(progress, 'TAHAP8', f'''## Tahap 8 — deployment dan persiapan submission

- Pencatatan: {now}.
- URL yang dicatat pemilik: {url}
- Perubahan: README, url.txt, status penutup notebook, pemeriksaan berkas, dan alat pengemasan ZIP.
- Hasil pemeriksaan otomatis berkas: lihat audit_otomatis.md.
- Hasil pemeriksaan manual browser: lihat checklist_final.md; isi sesuai hasil nyata.
- Kendala dan penyelesaian: dicatat oleh pemilik pada checklist_final.md bila ada.
- Pesan commit tahap ini: `docs: finalize deployment and submission`.
- Tindak lanjut: commit/push berkas, buat ZIP, periksa isi ZIP, lalu unggah ke Dicoding.

Catatan ini mencatat persiapan berkas. Riwayat commit/push dan penerimaan submission
dibuktikan melalui GitHub serta status pengiriman pada Dicoding.''')
    progress_path.write_text(progress, encoding='utf-8')
    report = audit(root, require_url=True)
    lines = [f'# Audit otomatis berkas — {now}', '',
             'Pemeriksaan ini membaca struktur berkas, output tersimpan, sintaks kode, dan CSV sumber.',
             'Kode notebook/dashboard tidak dijalankan oleh skrip ini. Akses URL tidak diuji melalui jaringan.', '',
             f"- Sel kode berisi kode dan memiliki execution_count: {report['code_cells']}.",
             f"- Grafik tersimpan dalam notebook: {report['saved_figures']}.",
             f"- Output error tersimpan: {report['saved_errors']}.",
             '- Identitas, judul bagian analisis, requirements, dan petunjuk menjalankan dashboard ditemukan.',
             '- Sintaks berkas Python pada dashboard berhasil diperiksa.',
             f'- URL berformat valid: {url}', '', '## CSV sumber', '',
             '| File | Baris | Total penyewaan |', '|---|---:|---:|']
    for name, data in report['data'].items():
        lines.append(f"| {name} | {data['rows']} | {data['total_rentals']} |")
    lines += ['', 'Kedua tabel merepresentasikan aktivitas yang sama pada tingkat agregasi berbeda; totalnya tidak dijumlahkan.',
              '', '## Pemeriksaan manual', '',
              'Gunakan checklist_final.md untuk memeriksa kesesuaian insight, akses publik, interaksi dashboard,',
              'riwayat GitHub, serta isi ZIP. Hasil otomatis ini bukan penilaian reviewer.',
              '', '## Identitas berkas yang diperiksa', '',
              f"- SHA-256 notebook: `{report['notebook_sha256']}`."]
    for name, data in report['data'].items():
        lines.append(f"- SHA-256 {name}: `{data['sha256']}`.")
    (docs / 'audit_otomatis.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return report


def package_files(root):
    paths = [root / name for name in ROOT_FILES if (root / name).is_file()]
    paths.append(root / '.streamlit/config.toml')
    for directory in INCLUDED_DIRS:
        for path in (root / directory).rglob('*'):
            relative = path.relative_to(root)
            if (path.is_file() and not path.is_symlink() and path.suffix.lower() in EXTENSIONS
                    and not any(part in EXCLUDED_PARTS for part in relative.parts)
                    and not path.name.startswith('.') and path.name.lower() != 'secrets.toml'):
                paths.append(path)
    return sorted(set(paths))


def make_zip(root):
    audit(root, require_url=True)
    if not (root / 'docs/audit_otomatis.md').is_file():
        raise CheckError('Jalankan prepare terlebih dahulu agar dokumentasi akhir tersedia.')
    files = package_files(root)
    dist = root / 'dist'; dist.mkdir(exist_ok=True)
    target = dist / 'Submission_Bike_Sharing_Tata_Ivanka.zip'
    temporary = target.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, 'submission/' + path.relative_to(root).as_posix())
    with zipfile.ZipFile(temporary) as archive:
        if archive.testzip() is not None:
            raise CheckError('Validasi integritas ZIP gagal.')
        if any('submission/' + name not in archive.namelist() for name in (*REQUIRED, 'url.txt')):
            raise CheckError('ZIP belum memuat seluruh berkas wajib.')
    temporary.replace(target)
    return target, len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['audit', 'prepare', 'zip'], nargs='?', default='audit')
    parser.add_argument('--url', help='URL publik Streamlit; jika tidak diisi, diminta ketika prepare.')
    args = parser.parse_args()
    try:
        if args.mode == 'audit':
            report = audit(ROOT)
            print(f"Audit struktur lulus: {report['code_cells']} sel kode, {report['saved_figures']} grafik, 0 output error.")
        elif args.mode == 'prepare':
            url = args.url or input('Tempel URL aplikasi https://....streamlit.app/ yang sudah kamu periksa: ')
            prepare(ROOT, url)
            print('Selesai: url.txt, README.md, status notebook, docs/progress.md, dan docs/audit_otomatis.md diperbarui.')
            print('Isi docs/checklist_final.md sesuai hasil nyata, kemudian commit/push pembaruan tahap 8.')
        else:
            path, count = make_zip(ROOT)
            print(f'ZIP berhasil dibuat: {path}')
            print(f'{count} berkas dikemas. Periksa checklist dan unggah ZIP ini ke Dicoding.')
    except (CheckError, OSError, ValueError, KeyError, SyntaxError) as exc:
        print(f'PERLU DIPERBAIKI: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
