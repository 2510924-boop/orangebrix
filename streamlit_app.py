import streamlit as st
import joblib
import numpy as np

# 페이지 설정
st.set_page_config(page_title="제주도 감귤 당도 예측", layout="centered")

# 제목
st.title("🍊 제주도 성산지역 감귤 당도 예측")
st.markdown("---")

# 모델 로드
@st.cache_resource
def load_model():
    model = joblib.load("brix_model.joblib")
    return model

try:
    model = load_model()
    
    # 사용자 입력 섹션
    st.subheader("📊 기상 데이터 입력")
    
    col1, col2 = st.columns(2)
    
    with col1:
        avg_temp = st.number_input(
            "평균기온 (°C)",
            value=20.0,
            step=0.1,
            format="%.1f"
        )
    
    with col2:
        min_temp = st.number_input(
            "최저기온 (°C)",
            value=15.0,
            step=0.1,
            format="%.1f"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        sunshine_hours = st.number_input(
            "가조시간 (시간)",
            value=6.0,
            step=0.1,
            format="%.1f"
        )
    
    with col4:
        min_frost_temp = st.number_input(
            "최저초상온도 (°C)",
            value=10.0,
            step=0.1,
            format="%.1f"
        )
    
    st.markdown("---")
    
    # 예측 버튼
    if st.button("당도 예측", type="primary", use_container_width=True):
        # 입력값을 배열로 변환
        input_features = np.array([[avg_temp, min_temp, sunshine_hours, min_frost_temp]])
        
        # 모델 예측
        prediction = model.predict(input_features)[0]
        
        # 결과 표시
        st.success("✅ 예측 완료!")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("예상 당도 (°Brix)", f"{prediction:.2f}")
        
        with col2:
            if prediction >= 11:
                st.markdown("**등급: 🥇 우수**")
            elif prediction >= 9:
                st.markdown("**등급: 🥈 보통**")
            else:
                st.markdown("**등급: 🥉 일반**")
        
        st.markdown("---")
        
        # 입력된 조건 표시
        st.subheader("📋 입력된 기상 조건")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("평균기온", f"{avg_temp}°C")
        col2.metric("최저기온", f"{min_temp}°C")
        col3.metric("가조시간", f"{sunshine_hours}시간")
        col4.metric("최저초상온도", f"{min_frost_temp}°C")

except FileNotFoundError:
    st.error("❌ 모델 파일(brix_model.joblib)을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"❌ 오류 발생: {str(e)}")