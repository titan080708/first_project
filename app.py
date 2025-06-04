import streamlit as st  # Streamlit 라이브러리를 불러옵니다. 웹 앱 인터페이스를 만드는 데 사용됩니다.
import random  # 카드 섞기를 위해 random 모듈을 사용합니다.

# 세션 상태를 이용해 deck(덱)이 없다면 초기화
if "deck" not in st.session_state:
    st.session_state.deck = list(range(1, 14)) * 4  # 카드 번호 1~13까지를 4세트로 만들어 총 52장의 카드 생성
    random.shuffle(st.session_state.deck)  # 덱을 무작위로 섞습니다
    st.session_state.score = {"플레이어": 0, "컴퓨터": 0, "무승부": 0}  # 초기 점수 설정
    st.session_state.last_draw = []  # 마지막으로 뽑은 카드 저장 리스트

st.title("🃏 카드 대결 게임")  # 앱의 타이틀 표시

# '카드 뽑기' 버튼을 클릭했을 때의 동작 정의
if st.button("카드 뽑기"):
    if len(st.session_state.deck) >= 2:  # 카드가 2장 이상 남아있을 때만 실행
        player_card = st.session_state.deck.pop()  # 플레이어가 카드 1장 뽑음 (덱에서 제거됨)
        computer_card = st.session_state.deck.pop()  # 컴퓨터도 카드 1장 뽑음
        st.session_state.last_draw = [player_card, computer_card]  # 이번 라운드의 카드 저장

        # 플레이어와 컴퓨터의 카드 크기를 비교하여 점수 계산
        if player_card > computer_card:
            st.session_state.score["플레이어"] += 1  # 플레이어 점수 증가
            result = "😊 당신이 이겼어요!"
        elif player_card < computer_card:
            st.session_state.score["컴퓨터"] += 1  # 컴퓨터 점수 증가
            result = "😢 컴퓨터가 이겼어요."
        else:
            st.session_state.score["무승부"] += 1  # 무승부 처리
            result = "😐 무승부입니다."
        st.success(result)  # 결과 메시지 출력
    else:
        st.warning("덱에 카드가 부족합니다. 아래 버튼으로 리셋하세요.")  # 카드가 부족할 경우 경고 메시지

# 마지막 뽑은 카드 정보 표시
if st.session_state.last_draw:
    st.subheader("🆚 이번 라운드")  # 소제목 출력
    st.write(f"**플레이어:** {st.session_state.last_draw[0]}   |   **컴퓨터:** {st.session_state.last_draw[1]}")  # 각자의 카드 표시

# 현재 점수 출력
st.subheader("📊 현재 점수")
st.write(st.session_state.score)

# 남은 카드 수 표시
st.caption(f"남은 카드 수: {len(st.session_state.deck)}")

# 게임 리셋 버튼
if st.button("🔁 게임 초기화"):
    st.session_state.deck = list(range(1, 14)) * 4  # 새로운 덱 생성
    random.shuffle(st.session_state.deck)  # 덱 섞기
    st.session_state.score = {"플레이어": 0, "컴퓨터": 0, "무승부": 0}  # 점수 초기화
    st.session_state.last_draw = []  # 마지막 카드 기록도 초기화



