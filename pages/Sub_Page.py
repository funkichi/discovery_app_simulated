import streamlit as st
import pandas as pd
from PIL import Image
import base64
import io
import os

# 画像サイズを変数に代入
size_logo = (320, 180)
size_area1 = (200, 200)
size_area2 = (200, 200)
size_area3 = (200, 200)
size_disaster = (200, 200)

# 画像ファイルを読み込んでthumbnail関数でサイズを指定
image_logo = Image.open('Material/logo.png')
image_logo.thumbnail(size_logo)
image_area1 = Image.open('Material/area1.png')
image_area1.thumbnail(size_area1)
image_area2 = Image.open('Material/area2.png')
image_area2.thumbnail(size_area2)
image_area3 = Image.open('Material/area3.png')
image_area3.thumbnail(size_area3)
image_disaster = Image.open('Material/disaster.png')
image_disaster.thumbnail(size_disaster)

# 画像をバイナリで読み込みbase64でエンコードして文字列化する(streamlitではHTMLタグで参照できないから)
def get_image_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

#base64エンコードされた文字列を取得
img_str_logo = get_image_base64(image_logo)

#HTMLで画像を表示する
st.markdown(f'<p style="text-align: center;"><img src="data:image/png;base64,{img_str_logo}"></p>', unsafe_allow_html=True)

#3列改行
for i in range(3):
    st.write('\n')

# pandasでcsvファイルを読み込む
df = pd.read_csv('DataBase/避難場所.csv')

# 1. エリアのセレクトボックス
st.image(image_area1)
available_areas = list(df['エリア'].drop_duplicates())
selected_location_1 = st.selectbox("", available_areas, label_visibility="collapsed")

# 2. 都道府県のセレクトボックス
# エリアが選択されたら、そのエリアに含まれる都道府県のみを抽出
st.image(image_area2)
if selected_location_1: # エリアが選択されている場合
    filtered_df_by_area = df[df['エリア'] == selected_location_1]
    available_prefectures = list(filtered_df_by_area['都道府県'].drop_duplicates())
    selected_location_2 = st.selectbox("都道府県を選択してください", available_prefectures, label_visibility="collapsed")

    # 3. 市区町村のセレクトボックス
    # 都道府県が選択されたら、その都道府県に含まれる市区町村のみを抽出
    st.image(image_area3)
    if selected_location_2: # 都道府県が選択されている場合
        filtered_df_by_prefecture = filtered_df_by_area[filtered_df_by_area['都道府県'] == selected_location_2]
        available_cities = list(filtered_df_by_prefecture['市区町村'].drop_duplicates())
        selected_location_3 = st.selectbox("市区町村を選択してください", available_cities, label_visibility="collapsed")

        # 4. 災害のセレクトボックス
        # 市区町村が選択されたら、その市区町村に含まれる災害を抽出
        st.image(image_disaster)
        if selected_location_3: # 市区町村が選択されている場合
            filtered_df_by_area1 = filtered_df_by_prefecture[filtered_df_by_prefecture['市区町村'] == selected_location_3]
            available_disasters = list(filtered_df_by_area1['災害'].drop_duplicates())
            selected_disaster = st.selectbox("災害の種類を選択してください", available_disasters, label_visibility="collapsed")
        else:
            selected_disaster = st.selectbox("災害の種類を選択してください", [], label_visibility="collapsed")
    else:
        selected_location_3 = st.selectbox("市区町村を選択してください", [], label_visibility="collapsed") 
        selected_disaster = st.selectbox("災害の種類を選択してください", [], label_visibility="collapsed") 
else:
    selected_location_2 = st.selectbox("都道府県を選択してください", [], label_visibility="collapsed")
    selected_location_3 = st.selectbox("市区町村を選択してください", [], label_visibility="collapsed")
    selected_disaster = st.selectbox("災害の種類を選択してください", [], label_visibility="collapsed")

# 検索ボタンが押された時の動作
with st.form(key='my_form'):
    #検索ボタンが押された時
    if st.form_submit_button("検索"):
        if selected_location_1 and selected_location_2 and selected_location_3 and selected_disaster:
            selected_row = df[
                (df["エリア"] == selected_location_1) &
                (df["都道府県"] == selected_location_2) &
                (df["市区町村"] == selected_location_3) &
                (df["災害"] == selected_disaster)
            ]

            if not selected_row.empty:
                st.write("### 検索結果")
                # 検索結果のDataFrameを表示
                st.dataframe(selected_row)

                # MAP列からURLを取得し、リンクとして表示
                st.markdown("<h5 style='text-align: left; color: darkturquoise;'>関連マップ</h5>", unsafe_allow_html=True)
                for index, row in selected_row.iterrows():
                    map_url = row["MAP"]
                    map_name = f"{row['市区町村']} の避難場所マップを見る"
                    st.markdown(f"[{map_name}]({map_url})")
            else:
                st.write("該当する避難場所は見つかりませんでした。")
        else:
            st.write("全ての項目を選択してください。")