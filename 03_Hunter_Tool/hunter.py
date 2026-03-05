import streamlit as st
import pandas as pd
import google.generativeai as genai
import glob
import os
import re

# --- 1. 画面の設定 ---
st.set_page_config(page_title="名脇役ハンター", page_icon="🔍")

# --- 2. スタイル設定（ペアリング診断と統一） ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1 { color: #313131 !important; font-weight: bold !important; }
    .stWidgetLabel p { color: #4a4a4a !important; font-weight: bold !important; }

    /* 入力ボックスの改善 */
    input { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border: 1px solid #d3d3d3 !important; 
        caret-color: #6a994e !important; 
        font-size: 1.1rem !important;
    }
    input:focus { 
        border: 2px solid #6a994e !important; 
        box-shadow: 0 0 5px rgba(106, 153, 78, 0.5) !important; 
        outline: none !important; 
    }

    /* 診断ボタン：ペアリング診断と同じ形状、色は緑 */
    div.stButton > button {
        background-color: #6a994e !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 3.5rem !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }

    /* 診断結果ボックス */
    .result-container {
        background-color: #f7fcf2;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #6a994e;
        color: #313131 !important;
        margin-top: 20px;
    }

    .section-title {
        font-weight: bold;
        font-size: 1.3rem;
        color: #6a994e;
        margin-bottom: 5px;
        display: block;
    }

    .loading-text { color: #6a994e !important; font-size: 1.2rem !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Google AIの設定（Secrets対応） ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# --- 4. データの読み込み ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    csv_pattern = os.path.join(current_dir, '*.csv')
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        st.error(f"CSVファイルが見つかりません。")
        return pd.DataFrame()

    df_list = []
    for file in csv_files:
        try:
            temp_df = pd.read_csv(file, encoding='utf-8-sig')
            df_list.append(temp_df)
        except Exception as e:
            st.warning(f"{os.path.basename(file)} の読み込み失敗")

    if not df_list: return pd.DataFrame()
    df = pd.concat(df_list, ignore_index=True).fillna('')
    
    # 検索用と表示用の列作成
    df['search_text'] = df['商品名'].astype(str) + " " + df['メーカー名'].astype(str)
    df['display_info'] = df.apply(lambda x: f"【{x.get('商品名','')}】 ({x.get('メーカー名','')})", axis=1)
    return df

# --- 5. AI診断ロジック ---
def find_partner_with_ai(target_product, all_products_list):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = f"""
    あなたは京都の高級スーパー「フレンドフーズ」の熟練コンシェルジュです。
    お客様が選んだ【メイン商品】に対して、最高に相性の良い「名脇役」を、リストの中から3つ厳選してください。

    【メイン商品】: {target_product}
    【商品リスト】: {all_products_list}

    【重要：回答形式】
    以下の形式を厳守し、各項目の間には必ず空行を入れてください。
    理由のタイトル（キャッチコピー）と、その後の詳細な説明文の間は必ず改行してください。

    ### 1. **[商品名]**
    **選んだ理由：[ここに短いキャッチコピー]**
    
    [ここから詳細な説明文を詳しく書く。コンシェルジュらしい丁寧な口調で。]

    ### 2. **[商品名]**
    **選んだ理由：[ここに短いキャッチコピー]**
    
    [詳細な説明文]

    ### 3. **[商品名]**
    **選んだ理由：[ここに短いキャッチコピー]**
    
    [詳細な説明文]
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- 6. メイン画面 ---
st.title("🔍 名脇役ハンター")
df = load_data()

if not df.empty:
    search_query = st.text_input("探したいキーワードを入力（商品名、メーカー名など）", placeholder="例：食パン")

    if search_query:
        results = df[df['search_text'].str.contains(search_query, na=False)]

        if not results.empty:
            selected_display = st.selectbox("正しい商品を選択してください：", results['display_info'])
            
            if st.button("この商品の「相棒」をAIに聞く"):
                status = st.empty()
                status.markdown('<p class="loading-text">🔍 最高の相棒を探索中...</p>', unsafe_allow_html=True)
                
                # サンプルから相棒候補を抽出
                sample_list = df.sample(min(100, len(df)))['display_info'].to_list()
                answer = find_partner_with_ai(selected_display, "\n".join(sample_list))
                
                status.empty()
                st.markdown(f"""
                    <div class="result-container">
                        <span class="section-title">✨ コンシェルジュからの提案</span>
                        <div style="line-height:1.7;">{answer}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("該当する商品が見つかりませんでした。")