import streamlit as st
import pandas as pd
import google.generativeai as genai
import glob
import os

# --- 1. 初期設定 (Secretsから安全に読み込む) ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。StreamlitのSecretsを確認してください。")

# --- 2. データの読み込み (パス指定を確実に) ---
@st.cache_data
def load_data():
    # hunter.pyがある場所を基準にCSVを探す設定
    current_dir = os.path.dirname(__file__)
    csv_pattern = os.path.join(current_dir, '*.csv')
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        st.error(f"CSVが見つかりません。場所: {current_dir}")
        return pd.DataFrame()

    df_list = []
    for file in csv_files:
        try:
            temp_df = pd.read_csv(file, encoding='utf-8-sig')
            df_list.append(temp_df)
        except Exception as e:
            st.warning(f"{os.path.basename(file)} の読み込み失敗: {e}")

    if not df_list: return pd.DataFrame()

    df = pd.concat(df_list, ignore_index=True).fillna('')
    
    # 必要列の作成
    for col in ['商品名', 'メーカー名', 'カナ名', '規格']:
        if col not in df.columns: df[col] = ""

    df['search_text'] = df['商品名'] + " " + df['メーカー名'] + " " + df['カナ名']
    df['display_info'] = df.apply(lambda x: f"【{x['商品名']}】 ({x['メーカー名']} / {x['規格']})", axis=1)
    return df

# --- 3. AI診断 (モデル名を安定版に変更) ---
def find_partner_with_ai(target_product, all_products_list):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    prompt = f"熟練コンシェルジュとして、{target_product}に合う相棒をリストから3つ選んで理由と共に教えてください。\nリスト:\n{all_products_list}"
    response = model.generate_content(prompt)
    return response.text

# --- 4. 画面レイアウト ---
st.title("🔍 名脇役ハンター")
df = load_data()

if not df.empty:
    search_query = st.text_input("キーワードを入力（パン、メーカー名など）")
    if search_query:
        results = df[df['search_text'].str.contains(search_query, na=False)]
        if not results.empty:
            selected = st.selectbox("正しい商品を選択：", results['display_info'])
            if st.button("「相棒」をAIに聞く"):
                with st.spinner("考え中..."):
                    sample = df.sample(min(150, len(df)))['display_info'].to_list()
                    st.markdown(find_partner_with_ai(selected, "\n".join(sample)))