import streamlit as st
import pandas as pd
import urllib.parse

# Page Config
st.set_page_config(page_title="Church Hymn Library", page_icon="⛪")

st.title("⛪ 詩歌歌詞與譜庫搜尋")
st.markdown("快速搜尋詩歌、歌詞及 Cantonhymn 連結")

# 1. Load Data
@st.cache_data
def load_data():
    # 讀取 CSV
    df = pd.read_csv('eccc-song-library-2026.csv', encoding='utf-8-sig')
    
    # --- 新增這行：自動移除所有欄位名稱前後的空白 ---
  
      df.columns = df.columns.str.strip() 
    return df
try:
    df = load_data()
except:
    st.error("⚠️ 找不到 Master_Church_Songs.csv，請確保檔案已上傳至 GitHub。")
    st.stop()

# 2. Sidebar Filters
st.sidebar.header("搜尋篩選")
search_query = st.sidebar.text_input("輸入關鍵字 (歌名或歌詞)")
artist_filter = st.sidebar.multiselect("選擇單位/歌手", options=df['Artist'].unique())
year_filter = st.sidebar.multiselect("年份", options=sorted(df['Year'].unique(), reverse=True))

# 3. Search Logic
filtered_df = df.copy()

if search_query:
    # Searches across both Song Title AND Lyrics
    mask = (filtered_df['Song Title'].str.contains(search_query, case=False, na=False)) | \
           (filtered_df['Lyrics'].str.contains(search_query, case=False, na=False))
    filtered_df = filtered_df[mask]

if artist_filter:
    filtered_df = filtered_df[filtered_df['Artist'].isin(artist_filter)]

if year_filter:
    filtered_df = filtered_df[filtered_df['Year'].isin(year_filter)]

# 4. Display Results
st.write(f"找到 {len(filtered_df)} 首詩歌")

for index, row in filtered_df.iterrows():
    with st.expander(f"🎵 {row['Song Title']} - {row['Artist']} ({row['Year']})"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("歌詞")
            st.text(row['Lyrics'])
            
        with col2:
            st.subheader("連結與資源")
            # Link to YouTube Music
            st.link_button("▶️ YouTube Music", row['Link'])
            
            # Auto-generate Cantonhymn Link
            # We URL-encode the song name to handle Chinese characters correctly
            encoded_name = urllib.parse.quote(row['Song Title'])
            ch_url = f"https://cantonhymn.net/songs/{encoded_name}"
            st.link_button("🔍 Cantonhymn 搵譜", ch_url)
            
            st.info("💡 如果 Cantonhymn 連結失效，請嘗試在該網站手動搜尋。")

# Footer
st.divider()
st.caption("Developed for Church Worship Team | Data from YTMusic & Cantonhymn")
