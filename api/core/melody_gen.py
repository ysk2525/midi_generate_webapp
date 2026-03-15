import random
from .chord_parser import get_chord_tones  # ちゃんとインポートしておくよ

def generate_melody_array(chord_progression):
    melody_track = []
    
    for measure_idx, chord_str in enumerate(chord_progression):
        chord_data = get_chord_tones(chord_str)
        safe_notes = chord_data.get('tones', [])
        
        if not safe_notes:
            continue

        for step in range(16):
            # 【修正点】Tone.js用のフォーマット (Bars:Beats:Sixteenths) を計算する
            # measure_idx: 小節 (0始まり)
            # step // 4  : 拍 (0〜3) ※16分音符を4つで割ると現在の拍になる
            # step % 4   : 16分音符 (0〜3)
            tone_position = f"{measure_idx}:{step // 4}:{step % 4}"
            
            # 強拍（0, 4, 8, 12ステップ目）
            if step % 4 == 0:
                note = random.choice(safe_notes)
                melody_track.append({
                    "note": note,
                    "position": tone_position, 
                    "duration": "8n"
                })
            
            # 弱拍（意外性の演出）
            else:
                surprise_factor = random.random()
                if surprise_factor < 0.15:
                    note = random.choice(safe_notes)
                    melody_track.append({
                        "note": note,
                        "position": tone_position,
                        "duration": "16n"
                    })

    return melody_track

# --- テスト用のダミー関数（単体で動かすため） ---
def get_chord_tones(chord):
    # 本来は chord_parser の結果を使うが、ここではテスト用に簡略化
    mapping = {"C": {"tones": ["C4", "E4", "G4"]}, "G": {"tones": ["G3", "B3", "D4"]}}
    return mapping.get(chord, {"tones": ["C4"]})

# 実行してみる
progression = ["C", "G"]
result = generate_melody_array(progression)
for note_info in result:
    print(note_info)