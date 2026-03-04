import streamlit as st
import google.generativeai as genai
import re

# --- 1. 画面の設定 ---
st.set_page_config(page_title="ペアリング診断", page_icon="💖")

# --- 2. スタイル設定 ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1 { color: #313131 !important; font-weight: bold !important; }
    .stWidgetLabel p { color: #4a4a4a !important; font-weight: bold !important; }

    /* ✨ 入力ボックスの改善：カーソル（縦棒）をはっきりさせる */
    input { 
        background-color: #ffffff !important; 
        color: #000000 !important; /* 入力文字を真っ黒にして見やすく */
        border: 1px solid #d3d3d3 !important; 
        caret-color: #ff8c94 !important; /* Geminiのような縦棒カーソルをピンクに */
        font-size: 1.1rem !important;
    }
    input:focus { 
        border: 2px solid #ff8c94 !important; 
        box-shadow: 0 0 5px rgba(255, 140, 148, 0.5) !important; 
        outline: none !important; 
    }
    input::placeholder { color: #aaaaaa !important; }

    /* 🌸 診断ボタン：完全に固定 */
    div.stButton > button {
        background-color: #ff8c94 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 3.5rem !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        transition: none !important;
    }
    div.stButton > button:hover, div.stButton > button:focus, div.stButton > button:active {
        background-color: #ff8c94 !important;
        color: white !important;
        opacity: 1 !important;
    }

    /* 🏆 相性スコア */
    .score-text {
        color: #ff8c94 !important;
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin: 15px 0;
        border-bottom: 2px solid #ff8c94;
        display: inline-block;
        width: 100%;
    }

    /* 📝 診断結果ボックス */
    .result-container {
        background-color: #fff9fa;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #ff8c94;
        color: #313131 !important;
        margin-top: 20px;
    }

    /* 余白の統一：タイトル下の隙間を「理由」に合わせる */
    .section-title {
        font-weight: bold;
        font-size: 1.3rem;
        color: #ff8c94;
        margin-top: 0px !important;
        margin-bottom: 5px !important; /* 隙間を詰めて統一 */
        display: block;
    }

    .reason-text {
        line-height: 1.7;
        font-size: 1.05rem;
        margin-bottom: 20px; /* 次のセクションへの間隔 */
    }

    .tips-list {
        line-height: 1.8;
        font-size: 1.05rem;
    }

    .loading-text { color: #ff8c94 !important; font-size: 1.2rem !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

st.title("💖 ペアリング診断")

# --- 3. Google AIの設定 ---
GOOGLE_API_KEY = ""
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- 4. 入力フォーム ---
with st.form("pairing_form"):
    col1, col2 = st.columns(2)
    with col1:
        food = st.text_input("食材・料理名", placeholder="例：銀だらの西京漬け")
    with col2:
        drink = st.text_input("合わせたいお酒", placeholder="例：やや辛口の日本酒")
    
    submitted = st.form_submit_button("相性を診断する")

# --- 5. 診断ロジック ---
if submitted and food and drink:
    status = st.empty()
    status.markdown('<p class="loading-text">💖 診断中...</p>', unsafe_allow_html=True) 
    
    prompt = f"""
    あなたは京都の「フレンドフーズ」の熟練コンシェルジュです。挨拶は一切不要。
    {food}と{drink}の相性を以下の構成で出力してください。
    
    1行目：相性スコア：◯点
    
    【理由】
    （一連の文章で解説。絶対に箇条書きにしないでください）
    
    【美味しくするコツ】
    （1. 2. 3. ...と必ず番号を振り、各項目を改行してください）
    """

    try:
        response = model.generate_content(prompt)
        status.empty() 
        
        res_text = response.text
        lines = [line.strip() for line in res_text.split('\n') if line.strip()]
        
        # スコア表示
        st.markdown(f'<div class="score-text">{lines[0]}</div>', unsafe_allow_html=True)

        # 内容の解析
        content = '\n'.join(lines[1:])
        if "【美味しくするコツ】" in content:
            parts = content.split("【美味しくするコツ】")
            reason_part = parts[0].replace("【理由】", "").strip()
            tips_part = parts[1].strip()
            
            # 数字の後に必ず改行を入れる処理
            formatted_tips = re.sub(r'(\d+\.)', r'<br>\1', tips_part)
            if formatted_tips.startswith('<br>'):
                formatted_tips = formatted_tips[4:]

            st.markdown(f"""
                <div class="result-container">
                    <span class="section-title">【理由】</span>
                    <div class="reason-text">{reason_part}</div>
                    <span class="section-title">【美味しくするコツ】</span>
                    <div class="tips-list">{formatted_tips}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-container">{content}</div>', unsafe_allow_html=True)
            
    except Exception as e:
        status.empty()
        st.error(f"エラーが発生しました: {e}")