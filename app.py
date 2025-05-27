# ai_lyric_generator.py

import streamlit as st
import random

st.title("🎶 AI 작사가 - 나만의 노래 만들기")

# 키워드 입력
keyword = st.text_input("노래 가사의 주제 또는 키워드를 입력하세요", "")

# 버튼 클릭 시 가사 생성
if st.button("가사 생성하기"):
    if keyword.strip() == "":
        st.warning("키워드를 입력해 주세요!")
    else:
        # 간단한 가사 패턴
        verses = [
            f"{keyword} 속에 숨겨진 내 마음",
            f"밤하늘에 {keyword}를 그려봐",
            f"{keyword}처럼 너는 내게 다가와",
            f"잊지 못할 {keyword}의 기억들",
            f"내 하루는 온통 {keyword}뿐이야"
        ]
        chorus = [
            f"Oh {keyword}, you're my only one",
            f"With you, {keyword} feels like home",
            f"I sing this song for you and {keyword}",
            f"My heart beats for your {keyword}"
        ]

        # 랜덤으로 구절 조합
        st.subheader("🎵 생성된 가사:")
        st.write("\n".join(random.sample(verses, 3)))
        st.write("\n**후렴:**")
        st.write(random.choice(chorus))

---

### 실행 방법
1. 파일을 예: `ai_lyric_generator.py`로 저장
2. 터미널에서 실행:
   ```bash
   streamlit run ai_lyric_generator.py

