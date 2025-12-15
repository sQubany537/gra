import streamlit as st
import random

# Tytuł aplikacji
st.title("🪨📄✂️ Kamień-Papier-Nożyce")

# Ustalenie dostępnych ruchów i ich zwycięskich relacji
MOVES = ["Kamień", "Papier", "Nożyce"]
WINNING_MOVES = {
    "Kamień": "Nożyce",
    "Papier": "Kamień",
    "Nożyce": "Papier"
}

# --- Inicjalizacja stanu sesji (tylko raz przy starcie) ---
if 'score_user' not in st.session_state:
    st.session_state.score_user = 0
if 'score_computer' not in st.session_state:
    st.session_state.score_computer = 0
if 'result_message' not in st.session_state:
    st.session_state.result_message = "Wybierz swój ruch poniżej, aby zacząć!"

# --- Główna logika gry ---

def determine_winner(user_choice, computer_choice):
    """Określa zwycięzcę i aktualizuje stan gry."""
    
    if user_choice == computer_choice:
        st.session_state.result_message = f"Remis! Oboje wybraliście {user_choice}."
        return 0 # Remis
    elif WINNING_MOVES[user_choice] == computer_choice:
        st.session_state.score_user += 1
        st.session_state.result_message = f"Wygrałeś! {user_choice} bije {computer_choice}."
        return 1 # Użytkownik wygrał
    else:
        st.session_state.score_computer += 1
        st.session_state.result_message = f"Przegrałeś! {computer_choice} bije {user_choice}."
        return -1 # Komputer wygrał

def play(user_choice):
    """Funkcja wywoływana po naciśnięciu przycisku."""
    computer_choice = random.choice(MOVES)
    st.session_state.last_user_choice = user_choice
    st.session_state.last_computer_choice = computer_choice
    determine_winner(user_choice, computer_choice)

# --- Interfejs użytkownika ---

st.header("Aktualny Wynik")
col1, col2 = st.columns(2)
with col1:
    st.metric("Gracz", st.session_state.score_user)
with col2:
    st.metric("Komputer", st.session_state.score_computer)

st.divider()

st.header("Wybierz Swój Ruch")
# Tworzenie kolumn dla przycisków
button_cols = st.columns(len(MOVES))

# Generowanie przycisków z funkcją play
for i, move in enumerate(MOVES):
    with button_cols[i]:
        # Używamy lambda, aby przekazać argument do funkcji play
        st.button(move, on_click=play, args=(move,))

# Wyświetlanie wyniku ostatniej rundy
st.markdown(f"**Ostatnia Runda:** {st.session_state.result_message}")

if 'last_user_choice' in st.session_state:
    st.info(f"Twój wybór: **{st.session_state.last_user_choice}** vs. Wybór Komputera: **{st.session_state.last_computer_choice}**")

# Przycisk resetujący wynik
def reset_scores():
    st.session_state.score_user = 0
    st.session_state.score_computer = 0
    st.session_state.result_message = "Wynik zresetowany. Zaczynamy od nowa!"
    if 'last_user_choice' in st.session_state:
        del st.session_state.last_user_choice
        del st.session_state.last_computer_choice

st.sidebar.button("Zresetuj Wynik", on_click=reset_scores)

# Informacja o Stanie Sesji:
st.sidebar.markdown("""
---
*Gra wykorzystuje **stan sesji Streamlit** (`st.session_state`) do zapamiętywania wyników między kliknięciami.*
""")
