import streamlit as st
import random
import time
import requests
import pandas as pd
import plotly.express as px

# --- НАСТРОЙКИ ДИЗАЙНА (ЧЕРНЫЙ + БИРЮЗА + КРАСНЫЙ) ---
st.set_page_config(page_title="Travorium Championship", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3 { color: #00FBFF !important; text-align: center; text-transform: uppercase; }
    .question-box { 
        background-color: #111; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #333;
        margin-bottom: 25px;
        min-height: 150px;
    }
    .question-text { font-size: 22px; line-height: 1.5; color: white; }
    
    div.stButton > button {
        background-color: #1A1C24 !important;
        color: #00FBFF !important;
        border: 2px solid #00FBFF !important;
        border-radius: 12px !important;
        padding: 20px !important;
        font-size: 18px !important;
        width: 100% !important;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        background-color: #FF4B4B !important;
        color: white !important;
        border: 2px solid #FF4B4B !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- НАСТРОЙКИ TELEGRAM ---
TOKEN = "ТВОЙ_ТОКЕН"
CHAT_ID = "ТВОЙ_CHAT_ID"

def send_tg(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

# --- ПОЛНЫЙ СПИСОК ИЗ 20 ВОПРОСОВ ---
if 'quiz_data' not in st.session_state:
    q_list = [
        {"q": "В каком году компания была основана и когда она перешла на модель сетевого маркетинга?", "o": ["2010 и 2015", "2013 и 2019", "2015 и 2024", "2012 и 2024"], "a": "2013 и 2019"},
        {"q": "Где расположен главный офис компании?", "o": ["Мадрид (Испания)", "Алматы (Казахстан)", "Темекула (Калифорния, США)", "Мюнхен (Германия)"], "a": "Темекула (Калифорния, США)"},
        {"q": "Каков минимальный возраст для оформления членства в Travorium?", "o": ["16 лет", "18 лет", "21 год", "14 лет"], "a": "18 лет"},
        {"q": "В скольких странах компания официально представлена или доступна для регистрации?", "o": ["Более 65", "Ровно 100", "120 (включая регистрацию через крипту)", "170"], "a": "120 (включая регистрацию через крипту)"},
        {"q": "Какой процент кэшбэка в виде баллов лояльности начисляется за бронирование отелей через Travel сайт?", "o": ["1%", "3%", "5%", "0%"], "a": "1%"},
        {"q": "Как называется платформа, позволяющая бронировать курорты (Resorts) со скидкой до 80% и более?", "o": ["World Tour", "Getaways", "Travorium Plus", "Поощерительная поездка"], "a": "Getaways"},
        {"q": "В течение какого срока новый участник может запросить полный возврат средств?", "o": ["7 дней", "14 дней", "30 дней", "28 дней"], "a": "14 дней"},
        {"q": "Что такое «Travel Points»?", "o": ["Живые деньги для вывода", "Баллы для снижения цены туров Getaway и World Tour", "Акции компании", "Доход для вывода на карту"], "a": "Баллы для снижения цены туров Getaway и World Tour"},
        {"q": "Через какое время неиспользованные баллы Travel Points сгорают?", "o": ["12 месяцев", "24 месяца", "Никогда", "48 месяцев"], "a": "Никогда"},
        {"q": "Какова ежемесячная стоимость членства уровня «Platinum»?", "o": ["$75", "$135", "$269.95", "$270"], "a": "$269.95"},
        {"q": "Сколько туристических баллов начисляется за 1 доллар взноса на уровнях Platinum и Titanium?", "o": ["1 балл", "2 балла", "1.5 балла", "3 балла"], "a": "2 балла"},
        {"q": "Сколько лично приглашенных партнеров необходимо для бесплатного членства?", "o": ["1", "3", "10", "5"], "a": "3"},
        {"q": "Какой ежедневный пассивный доход получает партнер в ранге Platinum Director (3 личных)?", "o": ["$1.75", "$2.50", "$4.45", "$10"], "a": "$4.45"},
        {"q": "Какой фиксированный ежемесячный бонус полагается партнеру в ранге 1 Star Director?", "o": ["$100", "$300", "$750", "$200"], "a": "$300"},
        {"q": "Что происходит с аккаунтом и баллами после 90 дней неактивности?", "o": ["Блокировка", "Удаление", "Сохранение", "Передача вышестоящему"], "a": "Удаление"},
        {"q": "Каков максимальный ежемесячный бонус Lifestyle для ранга 3 Star Director?", "o": ["$100", "$300", "$500", "$1000"], "a": "$500"},
        {"q": "Какое количество баллов (BV) дает личная продажа подписки Platinum?", "o": ["35 BV", "80 BV", "50 BV", "100 BV"], "a": "50 BV"},
        {"q": "Какое условие необходимо выполнить для ранга 2 Star Director?", "o": ["3 личных / 50 чел", "5 личных / 4000 BV общего объема", "10 личных", "5 личных / 16 чел"], "a": "5 личных / 4000 BV общего объема"},
        {"q": "Куда попадает новый партнер сразу после регистрации до расстановки?", "o": ["Сразу в слабую ногу", "В «Комнату ожидания» (Waiting Room) до 7 дней", "В архив", "В ячейку"], "a": "В «Комнату ожидания» (Waiting Room) до 7 дней"}
    ]
    for q in q_list: random.shuffle(q['o']) # Перемешиваем ответы
    st.session_state.quiz_data = q_list
    st.session_state.score = 0
    st.session_state.current_q = 0
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = []

# --- ПЕРЕКЛЮЧАТЕЛЬ ЭКРАНОВ ---
if 'step' not in st.session_state: st.session_state.step = 'login'

if st.session_state.step == 'login':
    st.title("🏆 TRAVORIUM RACE 🏁")
    u_id = st.text_input("ID Участника", placeholder="Твой номер")
    u_name = st.text_input("Имя Фамилия", placeholder="Иван Иванов")
    if st.button("ПОЕХАЛИ! 🔥"):
        if u_id and u_name:
            st.session_state.u_id, st.session_state.u_name = u_id, u_name
            st.session_state.start_t, st.session_state.step = time.time(), 'quiz'
            st.rerun()

elif st.session_state.step == 'quiz':
    curr = st.session_state.current_q
    total = len(st.session_state.quiz_data)
    st.progress(curr / total)
    
    q_item = st.session_state.quiz_data[curr]
    st.markdown(f"<div class='question-box'><p class='question-text'><b>Вопрос {curr+1} из {total}:</b><br>{q_item['q']}</p></div>", unsafe_allow_html=True)
    
    for option in q_item['o']:
        if st.button(option, key=f"btn_{curr}_{option}"):
            if option == q_item['a']: st.session_state.score += 1
            if curr + 1 < total:
                st.session_state.current_q += 1
                st.rerun()
            else:
                duration = time.time() - st.session_state.start_t
                st.session_state.leaderboard.append({"ID": st.session_state.u_id, "Имя": st.session_state.u_name, "Баллы": st.session_state.score, "Время": round(duration, 1)})
                send_tg(f"🏁 *ФИНИШ!* \n👤 {st.session_state.u_name} (ID: {st.session_state.u_id})\n🎯 {st.session_state.score}/{total}\n⏱ {duration:.1f} сек.")
                st.session_state.step, st.session_state.final_time = 'finish', duration
                st.rerun()

elif st.session_state.step == 'finish':
    st.balloons()
    st.title("РЕЗУЛЬТАТ")
    st.header(f"Баллы: {st.session_state.score} | Время: {st.session_state.final_time:.1f} сек.")
    
    st.markdown("---")
    st.subheader("📊 ТАБЛИЦА ЛИДЕРОВ (TOP)")
    df = pd.DataFrame(st.session_state.leaderboard)
    if not df.empty:
        df = df.sort_values(by=["Баллы", "Время"], ascending=[False, True]).reset_index(drop=True)
        st.table(df.head(10))
    
    if st.button("Пройти еще раз"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.step = 'login'
        st.rerun()