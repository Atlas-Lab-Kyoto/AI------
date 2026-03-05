import streamlit as st
import pandas as pd
import google.generativeai as genai
import glob  # 複数ファイルを探すためのライブラリ

# ==========================================
# 1. 初期設定（APIキーをここに貼ってください）
# ==========================================
genai.configure(api_key="AIzaSyDWhhLNNAb0KLZu-4YYvIMxCkWKSxzBupI")

# ==========================================
# 2. データの読み込み関数（複数CSV対応版）
# ==========================================
@st.cache_data
def load_data():
    # フォルダ内のすべてのCSVファイルを取得
    csv_files = glob.glob('*.csv')
    
    if not csv_files:
        st.error("CSVファイルが一つも見つかりません。03_Hunter_Toolフォルダ内に置いてください。")
        return pd.DataFrame()

    df_list = []
    for file in csv_files:
        try:
            # 各ファイルを読み込んでリストに追加
            temp_df = pd.read_csv(file, encoding='utf-8-sig')
            df_list.append(temp_df)
        except Exception as e:
            st.warning(f"{file} の読み込みに失敗しました: {e}")

    if not df_list:
        return pd.DataFrame()

    # すべてのCSVを一つに合体
    df = pd.concat(df_list, ignore_index=True)
    
    # 欠損値（空欄）を空文字で埋める
    df = df.fillna('')
    
    # 検索用テキストの作成
    # ※すべてのCSVに「商品名」「メーカー名」「カナ名」の列があることが前提です
    df['search_text'] = (
        df['商品名'].astype(str) + " " + 
        df['メーカー名'].astype(str) + " " + 
        df['カナ名'].astype(str)
    )
    
    # 画面表示用の整形
    df['display_info'] = df.apply(
        lambda x: f"【{x['商品名']}】 (メーカー:{x['メーカー名']} / 規格:{x['規格']})", axis=1
    )
    return df

# ==========================================
# 3. AIによる「相棒」診断ロジック
# ==========================================
def find_partner_with_ai(target_product, all_products_list):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = f"""
    あなたは京都の高級スーパー「フレンドフーズ」の熟練コンシェルジュです。
    お客様が選んだ【メイン商品】に対して、最高に相性の良い「名脇役（相棒）」を、提供された商品リストの中から3つ選んでください。

    【メイン商品】: {target_product}

    【選定基準】:
    1. 味の相性
    2. 食卓のストーリー
    3. フレンドフーズらしい「こだわり」

    【商品リスト】:
    {all_products_list}

    【重要：回答形式】:
    以下の形式を厳守してください。余計な挨拶や前置きは不要です。

    ### 1. **[商品名を入れてください]**
    **理由：** [ここに改行して理由を書いてください。一文で簡潔に。]

    ### 2. **[商品名を入れてください]**
    **理由：** [理由]

    ### 3. **[商品名を入れてください]**
    **理由：** [理由]
    """
    
    response = model.generate_content(prompt)
    return response.text

# ==========================================
# 4. Streamlit 画面レイアウト
# ==========================================
st.set_page_config(page_title="名脇役ハンター", page_icon="🔍")
st.title("🔍 名脇役ハンター")
st.caption("フォルダ内のすべてのCSVから、最高の一品を見つけ出します。")

df = load_data()

if not df.empty:
    # 検索窓
    search_query = st.text_input("探したいキーワードを入力（商品名、メーカー名など）")

    if search_query:
        # 部分一致で候補を絞り込み
        results = df[df['search_text'].str.contains(search_query, na=False)]

        if not results.empty:
            st.write(f"🔍 {len(results)} 件の候補が見つかりました：")
            
            # 商品選択
            selected_display = st.selectbox("正しい商品を選択してください：", results['display_info'])
            
            if st.button("この商品の「相棒」をAIに聞く"):
                with st.spinner("熟練コンシェルジュが考え中..."):
                    # 在庫リストからランダムに100件を抽出してAIに渡す
                    sample_list = df.sample(min(100, len(df)))['display_info'].to_list()
                    answer = find_partner_with_ai(selected_display, "\n".join(sample_list))
                    
                    st.success("✨ コンシェルジュからの提案：")
                    st.markdown(answer)
        else:
            st.warning("該当する商品が見つかりませんでした。")