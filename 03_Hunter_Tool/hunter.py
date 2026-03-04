import streamlit as st
import pandas as pd
import google.generativeai as genai
import glob
import os

# APIキーの設定
genai.configure(api_key="AIzaSyDWhhLNNAb0KLZu-4YYvIMxCkWKSxzBupI")

st.set_page_config(page_title="相棒ハンター", page_icon="🔍")
st.title("🔍 相棒ハンター")

# 1. 全てのCSVを読み込んで1つにする
csv_files = glob.glob('03_Hunter_Tool/*.csv')

if csv_files:
    df_list = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(df_list, ignore_index=True)
    product_list = df['商品名'].unique().tolist()
else:
    st.error("CSVファイルが見つかりません。03_Hunter_ToolフォルダにCSVを入れてください。")
    product_list = []

# 2. 画面の作成
target_product = st.selectbox("メインの商品を選んでください", product_list)

if st.button("相棒を探す"):
    with st.spinner("コンシェルジュが探索中..."):
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        # 全リストを渡すとAIがパンクするので、ランダムに候補を混ぜて渡すなどの工夫もできますが、まずはシンプルに。
        all_items = ", ".join(product_list[:500]) # 最初は500件程度でテスト
        
        prompt = f"""
        あなたは京都の高級スーパー「フレンドフーズ」の熟練コンシェルジュです。
        【メイン商品】: {target_product}
        以下のリストから、最高に相性の良い「相棒」を3つ選んでください。
        リスト: {all_items}

        【回答形式】
        ### 1. **[商品名]**
        **理由：** [理由を改行して記載]
        """
        response = model.generate_content(prompt)
        st.markdown(response.text)