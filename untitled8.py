import streamlit as st
import random

# 現役メジャーリーガー打者（左右別）
left_batters = [
    "大谷翔平", "フレディ・フリーマン", "コディ・ベリンジャー", "吉田正尚", "ダルトン・バーショー",
    "ブライス・ハーパー", "カイル・シュワーバー", "フアン・ソト", "マット・オルソン", "ラーズ・ヌートバー",
    "ピート・クロウ＝アームストロング", "カイル・タッカー", "クルーズ", "クリスチャン・イエリチ",
    "ヨルダン・アルバレス", "コーリー・シーガー", "ラファエル・ディバース", "ジョシュ・ネイラー", "コービン・キャロル",
    "オジー・アルビーズ", "カルロス・サンタナ", "アンソニー・サンタンダー", "エリー・デラクルーズ", "ジョシュ・ベル",
    "ホルヘ・ポランコ", "ケーテル・マルテ", "アドリー・ラッチマン", "ホセ・ラミレス", "フランシスコ・リンドーア", "カル・ローリー"
]

right_batters = [
    "ムーキー・ベッツ", "ポール・ゴールドシュミット", "ジャンカルロ・スタントン", "アーロン・ジャッジ",
    "ブラディミール・ゲレーロJr.", "ボー・ビシェット", "ウィル・スミス", "ジョージ・スプリンガー",
    "アレックス・ブレグマン", "J.T.リアルミュート", "トレイ・ターナー", "ニック・カステヤノス",
    "ショーン・マーフィー", "オースティン・ライリー", "ロナルド・アクーニャJr.", "マルセル・オズナ",
    "ピート・アロンソ", "スターリング・マルテ", "スペンサー・トーケルソン", "グレイバー・トーレス",
    "ロイス・ルイス", "カルロス・コレア", "ボビー・ウィットJr.", "ノーラン・アレナド",
    "ウィリアム・コントレラス", "ジャスティン・ターナー", "鈴木誠也", "アンドリュー・マカチェン",
    "ジャクソン・チョウリオ", "リース・ホスキンス", "クリスチャン・ウォーカー", "イサーク・パレデス",
    "ホセ・アルテューベ", "ルーカー", "アンソニー・レンドン", "マイク・トラウト", "フリオ・ロドリゲス",
    "ランディ・アロザレーナ", "マーカス・セミエン", "アドリス・ガルシア", "ウィリー・アダメズ",
    "マット・チャプマン", "ユジニオ・スアレス", "ランデル・グリチェク", "ザンダー・ボガーツ",
    "マニー・マチャド", "フェルナンド・タティスJr."
]

ballparks = [
    "ヤンキー・スタジアム", "フェンウェイ・パーク", "ロジャース・センター", "トロピカーナ・フィールド", "カウフマン・スタジアム",
    "ギャランティード・レート・フィールド", "プログレッシブ・フィールド", "コメリカ・パーク", "ターゲット・フィールド", "ミニッツメイド・パーク",
    "エンジェル・スタジアム", "オークランド・コロシアム", "T-モバイル・パーク", "グローブライフ・フィールド", "トゥルイスト・パーク",
    "ローンデポ・パーク", "シチズンズ・バンク・パーク", "ナショナルズ・パーク", "リグレー・フィールド", "グレートアメリカン・ボールパーク",
    "アメリカンファミリー・フィールド", "PNCパーク", "ブッシュ・スタジアム", "チェイス・フィールド", "クアーズ・フィールド",
    "ドジャー・スタジアム", "ペトコ・パーク", "オラクル・パーク", "シティ・フィールド"
]


def get_random_lineup():
    batters = [(name, "左") for name in random.sample(left_batters, 5)] + \
              [(name, "右") for name in random.sample(right_batters, 4)]
    random.shuffle(batters)
    return batters


def simulate_at_bat(batter_side, is_risp):
    base_hit_rate = 0.211 if batter_side == "左" else 0.263
    if is_risp:
        base_hit_rate += 0.04

    home_run_rate = 0.025
    walk_rate = 0.045
    hbp_rate = 0.02
    k_rate = 83 / 361
    out_rate = 1.0 - (base_hit_rate + home_run_rate + walk_rate + hbp_rate + k_rate)

    r = random.random()
    if r < base_hit_rate:
        return "単打"
    elif r < base_hit_rate + home_run_rate:
        return "ホームラン"
    elif r < base_hit_rate + home_run_rate + walk_rate:
        return "四球"
    elif r < base_hit_rate + home_run_rate + walk_rate + hbp_rate:
        return "死球"
    elif r < base_hit_rate + home_run_rate + walk_rate + hbp_rate + k_rate:
        return "三振"
    else:
        return "凡退"


def outcome_comment(result):
    return {
        "三振": "三振！ズバッと決まった",
        "単打": "単打！逆方向へ流した",
        "ホームラン": "ホームラン！スタンド一直線！",
        "四球": "フォアボール！制球が定まらない",
        "死球": "死球！当たったー！大丈夫か？",
        "凡退": "凡退！打たされた"
    }[result]


def advance_runners(bases, outcome):
    runs = 0
    if outcome == "単打":
        if bases[2]: runs += 1
        bases = [True, bases[0], bases[1]]
    elif outcome in ["四球", "死球"]:
        if not bases[0]:
            bases[0] = True
        elif not bases[1]:
            bases = [True, True, bases[2]]
        elif not bases[2]:
            bases = [True, True, True]
        else:
            runs += 1
    elif outcome == "ホームラン":
        runs += sum(bases) + 1
        bases = [False, False, False]
    return bases, runs


# Streamlit 用の試合描画
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.lineup = get_random_lineup()
    st.session_state.index = 0
    st.session_state.outs = 0
    st.session_state.runs = 0
    st.session_state.bases = [False, False, False]
    st.session_state.park = random.choice(ballparks)
    st.session_state.log = []

st.title("フジナミ・シミュレーター")
st.subheader(f"舞台は {st.session_state.park}！")

for log in st.session_state.log:
    st.write(log)

if st.session_state.outs < 3 and st.session_state.index < len(st.session_state.lineup):
    if st.button("【ENTERで打席に入ります】"):
        name, side = st.session_state.lineup[st.session_state.index]
        st.session_state.index += 1

        is_risp = st.session_state.bases[1] or st.session_state.bases[2]
        result = simulate_at_bat(side, is_risp)
        comment = outcome_comment(result)

        st.session_state.log.append(f"{side}打者 {name}：{comment}")

        if result in ["三振", "凡退"]:
            st.session_state.outs += 1
            st.session_state.log.append(f"{st.session_state.outs}アウト")
        else:
            bases, scored = advance_runners(st.session_state.bases, result)
            st.session_state.bases = bases
            st.session_state.runs += scored
            st.session_state.log.append(f"ランナー：{'1' if bases[0] else '_'} {'2' if bases[1] else '_'} {'3' if bases[2] else '_'}")
            if scored:
                st.session_state.log.append(f"→ {scored}点追加！（合計 {st.session_state.runs} 点）")
            else:
                st.session_state.log.append("→ 得点なし")
else:
    st.success(f"チェンジ！この回の失点：{st.session_state.runs} 点")
    if st.button("もう一度プレイ"):
        st.session_state.clear()
