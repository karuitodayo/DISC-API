import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Embedの枠の色(10進数のカラーコード)。例: 緑=3066993, 青=3447003, 赤=15158332
COLOR_INFO = 3447003


def build_embed(title: str, description: str, color: int = COLOR_INFO) -> dict:
    return {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def send_embed(embed: dict) -> None:
    if not WEBHOOK_URL:
        raise RuntimeError(".envにWEBHOOK_URLが設定されていません")

    response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})

    if response.status_code == 204:
        print("通知を送信しました")
    else:
        print(f"送信に失敗しました: status={response.status_code}, body={response.text}")


if __name__ == "__main__":
    # 実行例: python notify.py "作業が完了しました"
    text = sys.argv[1] if len(sys.argv) > 1 else "プログラムが正常に動作しています"
    embed = build_embed(title="通知", description=text)
    send_embed(embed)
