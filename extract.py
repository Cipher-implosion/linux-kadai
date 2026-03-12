import os
import sys
import configparser

# config読み込み
config = configparser.ConfigParser()
config.read("config.ini")

LOG_DIR = config["LOG"]["directory"]


def extract_logs(target_date, keyword=None, output=None):

    files = []
    for root, dirs, fs in os.walk(LOG_DIR):
        for f in fs:
            files.append(os.path.join(root, f))

    total = len(files)
    print(f"対象ログファイル数: {total}")

    result = []

    for i, file in enumerate(files, start=1):

        print(f"[{i}/{total}] 読み込み中: {file}")

        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:

                    if target_date not in line:
                        continue

                    if keyword and keyword not in line:
                        continue

                    record = f"{os.path.basename(file)} : {line}"
                    result.append(record)

        except Exception as e:
            print(f"読み込み失敗: {file} {e}")

    if output:
        with open(output, "w", encoding="utf-8") as out:
            out.writelines(result)
        print(f"\n出力完了: {output}")

    else:
        for r in result:
            print(r, end="")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage:")
        print("python log_extract.py 日付 [キーワード] [出力ファイル]")
        print("例: python log_extract.py 2026-03-11 ERROR result.log")
        sys.exit()

    date = sys.argv[1]

    keyword = None
    output = None

    if len(sys.argv) >= 3:
        keyword = sys.argv[2]

    if len(sys.argv) >= 4:
        output = sys.argv[3]

    extract_logs(date, keyword, output)