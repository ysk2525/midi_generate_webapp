import re

# 基本的な12音階（半音階）
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# 【改善点】コードの品質（quality）とインターバル（半音の距離）を「辞書」としてまとめる
CHORD_INTERVALS = {
    '': [0, 4, 7],           # メジャー (例: C)
    'm': [0, 3, 7],          # マイナー (例: Cm)
    '7': [0, 4, 7, 10],      # ドミナントセブンス (例: C7)
    'm7': [0, 3, 7, 10],     # マイナーセブンス (例: Cm7)
    'M7': [0, 4, 7, 11],     # メジャーセブンス (例: CM7 / Cmaj7)
    'maj7': [0, 4, 7, 11],   # (表記揺れ対応)
    'sus4': [0, 5, 7],       # サスフォー (例: Csus4)
    'dim': [0, 3, 6],        # ディミニッシュ (例: Cdim) - 不安を煽る響き
    'dim7': [0, 3, 6, 9],    # ディミニッシュセブンス (例: Cdim7)
    'm7b5': [0, 3, 6, 10],   # ハーフディミニッシュ (例: Cm7b5) - エモい進行の定番
    'aug': [0, 4, 8],        # オーギュメント (例: Caug) - フワッとした浮遊感
    'add9': [0, 4, 7, 14],   # アドナインス (例: Cadd9) - 爽やかさを足す響き
}

def get_note_index(note_str):
    return NOTES.index(note_str)

def get_chord_tones(chord_string):
    match = re.match(r'^([A-G][#b]?)([^/]*)(?:/([A-G][#b]?))?$', chord_string)
    
    if not match:
        return {"error": "解析できないコード形式だ。"}

    root_note = match.group(1)
    quality = match.group(2)
    bass_note = match.group(3)

    root_idx = get_note_index(root_note)
    
    # 【改善点】辞書からインターバルを取得。見つからない場合はメジャーコードにする
    intervals = CHORD_INTERVALS.get(quality, [0, 4, 7]) 

    # 音名への変換（% 12 のおかげで、add9の「14」も正しく計算できる）
    chord_tones = [NOTES[(root_idx + interval) % 12] for interval in intervals]

    if bass_note:
        if bass_note not in chord_tones:
            chord_tones.append(bass_note)
        return {"root": root_note, "tones": chord_tones, "bass": bass_note}

    return {"root": root_note, "tones": chord_tones, "bass": root_note}

# --- テスト実行 ---
print("Cdimの解析:", get_chord_tones("Cdim"))      
# 出力: {'root': 'C', 'tones': ['C', 'D#', 'F#'], 'bass': 'C'}

print("Eaugの解析:", get_chord_tones("Eaug"))    
# 出力: {'root': 'E', 'tones': ['E', 'G#', 'C'], 'bass': 'E'}

print("Bm7b5の解析:", get_chord_tones("Bm7b5"))    
# 出力: {'root': 'B', 'tones': ['B', 'D', 'F', 'A'], 'bass': 'B'}

print("Cadd9の解析:", get_chord_tones("Cadd9"))    
# 出力: {'root': 'C', 'tones': ['C', 'E', 'G', 'D'], 'bass': 'C'}