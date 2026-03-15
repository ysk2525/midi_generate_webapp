import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client

from core.melody_gen import generate_melody_array

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Supabaseの接続設定 ---
# 実際のURLとキーはSupabaseの「Project Settings -> API」から取得する
# セキュリティのため、本来は .env ファイルなどで管理するのが王道だよ
SUPABASE_URL = "君のSupabaseのURL"
SUPABASE_KEY = "君のSupabaseのanon/publicキー"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 生成用の設計図 ---
class MelodyRequest(BaseModel):
    bpm: int
    chord_progression: List[str]

# --- 【新規】いいね保存用の設計図 ---
class LikeRequest(BaseModel):
    bpm: int
    chord_progression: List[str]
    melody_data: list  # JSONBとしてそのまま保存する配列データ

@app.post("/api/generate")
def generate_api(request: MelodyRequest):
    # (前回書いたメロディ生成のコードがそのまま入る)
    real_melody = generate_melody_array(request.chord_progression)
    if not real_melody:
        return {"status": "error", "message": "メロディの生成に失敗した。"}
    return {"status": "success", "melody": real_melody}

# --- 【新規】「いいね」されたメロディを保存するエンドポイント ---
@app.post("/api/like")
def save_liked_melody(request: LikeRequest):
    """
    フロントエンドで「いいね」ボタンが押された時、このAPIが呼ばれる
    """
    try:
        # Supabaseの 'liked_melodies' テーブルにデータを挿入（INSERT）
        data, count = supabase.table("liked_melodies").insert({
            "bpm": request.bpm,
            "chord_progression": ",".join(request.chord_progression), # 配列を文字列にして保存
            "melody_data": request.melody_data,
            "likes": 1
        }).execute()
        
        return {
            "status": "success", 
            "message": "見事だ。この心地よいメロディをデータベースに記憶したよ。"
        }
    except Exception as e:
        print(f"データベースエラー: {e}")
        return {
            "status": "error",
            "message": "保存に失敗したようだ。"
        }