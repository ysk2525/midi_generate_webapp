// 【重要】今鳴っているメロディのデータを覚えておくための「箱」を一番外側に用意する
let currentMelodyData = null;
let currentBpm = 120;
let currentChords = [];

document.getElementById('generateBtn').addEventListener('click', async () => {
    await Tone.start();
    
    const bpmValue = document.getElementById('bpm').value;
    const chordsInput = document.getElementById('chords').value;
    const chordProgression = chordsInput.split(',');

    // 新しい曲を生成し始めたら、一度「いいね」ボタンを隠す（誤操作を防ぐためだよ）
    document.getElementById('likeBtn').style.display = 'none';

   try {
        // 【ここだ！】絶対パス（http://...）を消して、相対パス（/api/...）にする
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                bpm: parseInt(bpmValue),
                chord_progression: chordProgression
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            // 【重要】ここで、APIから届いたデータを「箱」に保存しておくんだ！
            currentMelodyData = data.melody;
            currentBpm = parseInt(bpmValue);
            currentChords = chordProgression;

            // 音を鳴らす
            playMelody(currentMelodyData, currentBpm);

            // 無事に音が鳴ったら、隠していた「いいね」ボタンを表示する！
            document.getElementById('likeBtn').style.display = 'inline-block';
        }
    } catch (error) {
        console.error("生成エラーだ:", error);
    }
});

// --- 【新規】いいねボタンが押された時の処理 ---
document.getElementById('likeBtn').addEventListener('click', async () => {
    // 箱が空っぽ（メロディがない）なら何もしない。フェイルセーフだね。
    if (!currentMelodyData) return;

    try {
        // バックエンド（Python）の保存用APIへデータを送る
        const response = await fetch('http://localhost:8000/api/like', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                bpm: currentBpm,
                chord_progression: currentChords,
                melody_data: currentMelodyData // 覚えておいた箱の中身を送る！
            })
        });

        const result = await response.json();

        if (result.status === "success") {
            // 保存に成功したらユーザーに知らせる
            alert("貴重なデータを保存したよ！協力に感謝する。");
            
            // 何度も同じデータを保存させないために、ボタンを再び隠す
            document.getElementById('likeBtn').style.display = 'none';
        }
    } catch (error) {
        console.error("保存エラーだ:", error);
        alert("すまない、データベースへの接続に失敗したようだ。");
    }
});

// (playMelody関数は前回のままで大丈夫だよ)
function playMelody(melodyData, bpm) {
    Tone.Transport.bpm.value = bpm;
    const synth = new Tone.Synth().toDestination();
    Tone.Transport.cancel();
    const part = new Tone.Part((time, value) => {
        synth.triggerAttackRelease(value.note, value.duration, time);
    }, melodyData);
    part.start(0);
    Tone.Transport.start();
}
