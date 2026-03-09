import streamlit as st
import time
import random
import requests
import plotly.express as px

# --- НАСТРОЙКИ ДИЗАЙНА (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stRadio [data-testid="stWidgetLabel"] p {
        color: #00FBFF; /* Бирюзовый для вопросов */
        font-size: 20px;
        font-weight: bold;
    }
    div.stButton > button:first-child {
        background-color: #FF4B4B; /* Красный для кнопок */
        color: white;
        border-radius: 10px;
        border: none;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        border: 2px solid #00FBFF;
        color: #00FBFF;
    }
    .stTextInput>div>div>input {
        background-color: #1A1C24;
        color: #00FBFF;
        border: 1px solid #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TELEGRAM CONFIG ---
TOKEN = "ТВОЙ_ТОКЕН_БОТА"
CHAT_ID = "ТВОЙ_CHAT_ID"

def send_to_tg(report):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": report, "parse_mode": "Markdown"})

# --- ДАННЫЕ (20 ВОПРОСОВ) ---
if 'questions' not in st.session_state:
    raw_data = [
        {"q": "В каком году компания основана и перешла на MLM?", "o": ["2010/2015", "2013/2019", "2015/2024", "2012/2024"], "a": "2013/2019"},
        {"q": "Где расположен главный офис компании?", "o": ["Мадрид", "Алматы", "Темекула (Калифорния)", "Мюнхен"], "a": "Темекула (Калифорния)"},
        {"q": "Минимальный возраст для членства?", "o": ["16 лет", "18 лет", "21 год", "14 лет"], "a": "18 лет"},
        {"q": "В скольких странах представлена компания?", "o": ["65+", "100", "120+", "170"], "a": "120+"},
        {"q": "Кэшбэк баллами за бронирование отелей?", "o": ["1%", "3%", "5%", "0%"], "a": "1%"},
        {"q": "Платформа для бронирования со скидкой 80%?", "o": ["World Tour", "Getaways", "Travorium Plus", "Поощерительная поездка"], "a": "Getaways"},
        {"q": "Срок возврата средств?", "o": ["7 дней", "14 дней", "30 дней", "28 дней"], "a": "14 дней"},
        {"q": "Что такое Travel Points?", "o": ["Деньги на карту", "Баллы для туров", "Акции", "Доход"], "a": "Баллы для туров"},
        {"q": "Срок сгорания Travel Points?", "o": ["12 мес", "24 мес", "Никогда", "48 мес"], "a": "Никогда"},
        {"q": "Ежемесячный взнос Platinum?", "o": ["$75", "$135", "$269.95", "$270"], "a": "$269.95"},
        {"q": "Баллы за $1 взноса (Platinum)?", "o": ["1", "2", "1.5", "3"], "a": "2"},
        {"q": "Личников для бесплатного членства?", "o": ["1", "3", "10", "5"], "a": "3"},
        {"q": "Пассивный доход Platinum Director?", "o": ["$1.75", "$2.50", "$4.45", "$10"], "a": "$4.45"},
        {"q": "Бонус 1 Star Director?", "o": ["$100", "$300", "$750", "$200"], "a": "$300"},
        {"q": "90 дней неактивности — что будет?", "o": ["Блок", "Удаление", "Сохранение", "Передача"], "a": "Удаление"},
        {"q": "Бонус Lifestyle для 3 Star Director?", "o": ["$100", "$300", "$500", "$1000"], "a": "$500"},
        {"q": "Баллы (BV) за продажу Platinum?", "o": ["35 BV", "80 BV", "50 BV", "100 BV"], "a": "50 BV"},
        {"q": "Условие 2 Star Director?", "o": ["3 личн/50 чел", "5 личн/4000 BV", "10 личн", "5 личн/16 чел"], "a": "5 личн/4000 BV"},
        {"q": "Где партнер до расстановки?", "o": ["Слабая нога", "Waiting Room", "Архив", "Ячейка"], "a": "Waiting Room"},
    ]
    # Перемешиваем ответы
    for item in raw_data:
        random.shuffle(item['o'])
    st.session_state.questions = raw_data

# --- ЛОГИКА ПРИЛОЖЕНИЯ ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'

if st.session_state.page == 'login':
    st.title("🔴 TRAVORIUM RACE 💎")
    st.subheader("Авторизация участника")
    st.session_state.u_id = st.text_input("Твой ID номер")
    st.session_state.u_name = st.text_input("Имя Фамилия")
    
    if st.button("ВОЙТИ В КАБИНЕТ И НАЧАТЬ"):
        if st.session_state.u_id and st.session_state.u_name:
            st.session_state.start_t = time.time()
            st.session_state.page = 'test'
            st.rerun()

elif st.session_state.page == 'test':
    st.info(f"🚀 Участник: {st.session_state.u_name} | ID: {st.session_state.u_id}")
    ans_map = {}
    
    for i, q_item in enumerate(st.session_state.questions):
        ans_map[i] = st.radio(f"{i+1}. {q_item['q']}", q_item['o'], key=f"q{i}", index=None)
        st.write("---")
    
    if st.button("ЗАВЕРШИТЬ ТЕСТ И ВЫСЛАТЬ РЕЗУЛЬТАТ"):
        duration = time.time() - st.session_state.start_t
        score = sum(1 for i, q in enumerate(st.session_state.questions) if ans_map[i] == q['a'])
        
        # Отчет в ТГ
        report = (f"🔥 *ФИНИШ!*\n\n"
                  f"🆔 ID: `{st.session_state.u_id}`\n"
                  f"👤 Имя: {st.session_state.u_name}\n"
                  f"✅ Баллы: {score}/{len(st.session_state.questions)}\n"
                  f"⏱ Время: {duration:.2f} сек.")
        send_to_tg(report)
        
        st.session_state.final_score = score
        st.session_state.final_time = duration
        st.session_state.page = 'finish'
        st.rerun()

elif st.session_state.page == 'finish':
    st.balloons()
    st.title("🏁 ТВОЙ РЕЗУЛЬТАТ")
    col1, col2 = st.columns(2)
    col1.metric("Правильно", f"{st.session_state.final_score}")
    col2.metric("Время (сек)", f"{st.session_state.final_time:.1f}")
    
    fig = px.pie(values=[st.session_state.final_score, len(st.session_state.questions)-st.session_state.final_score], 
                 names=['Верно', 'Ошибки'], hole=0.7, 
                 color_discrete_sequence=['#00FBFF', '#FF4B4B'])
    st.plotly_chart(fig)
    st.write("Твой результат отправлен куратору!")