import streamlit as st
import requests
import uuid
import time
from typing import List, Dict, Any

API_URL = "http://localhost:8000"

st.set_page_config(page_title="To do List", page_icon="✅")
st.title("To do List")

# session başlatma
if 'todos' not in st.session_state:
    st.session_state.todos = []
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = 0
if 'action_performed' not in st.session_state:
    st.session_state.action_performed = False

# Todo listesini getir
def fetch_todos():
    try:
        response = requests.get(f"{API_URL}/todos", timeout=3)
        if response.status_code == 200:
            st.session_state.todos = response.json()
            st.session_state.last_refresh = time.time()
            return True
        else:
            if not st.session_state.todos:  # Eğer daha önce veri alınmadıysa boş liste döndür
                st.session_state.todos = []
            return False
    except requests.RequestException:
        if not st.session_state.todos:  # Eğer daha önce veri alınmadıysa boş liste döndür
            st.session_state.todos = []
        st.error("API'ye bağlanırken hata oluştu!")
        return False

# To do ekle
def add_todo(title: str, description: str):
    todo = {
        "title": title,
        "description": description,
        "completed": False
    }
    try:
        response = requests.post(f"{API_URL}/todos", json=todo, timeout=3)
        success = response.status_code == 201
        if success:
            # Başarılı olursa verileri tekrar çek
            fetch_todos()
            st.session_state.action_performed = True
        return success
    except requests.RequestException:
        st.error("API'ye bağlanırken hata oluştu!")
        return False

# To do sil
def delete_todo(todo_id: str):
    try:
        response = requests.delete(f"{API_URL}/todos/{todo_id}", timeout=3)
        success = response.status_code == 200
        if success:
            # Başarılı olursa verileri tekrar çek
            fetch_todos()
            st.session_state.action_performed = True
        return success
    except requests.RequestException:
        st.error("API'ye bağlanırken hata oluştu!")
        return False

# To do durumunu güncelle 
def update_todo_status(todo: Dict[str, Any], completed: bool):
    updated_todo = todo.copy()  
    updated_todo["completed"] = completed
    try:
        response = requests.put(f"{API_URL}/todos/{updated_todo['id']}", json=updated_todo, timeout=3)
        success = response.status_code == 200
        if success:
            # başarılı olursa verileri tekrar çek
            fetch_todos()
            st.session_state.action_performed = True
        return success
    except requests.RequestException:
        st.error("API'ye bağlanırken hata oluştu!")
        return False

#  tamamlama checkbox işleyicisi
def handle_status_change(todo, status):
    # eğer tamamlama durumu değiştiyse, güncelle
    if status != todo["completed"]:
        with st.spinner(""):
            success = update_todo_status(todo, status)
            if success:
                return True
    return False

# silme butonu işleyicisi
def handle_delete(todo_id):
    with st.spinner(""):
        success = delete_todo(todo_id)
        if success:
            st.success("To do silindi!")
            time.sleep(0.3)
            st.rerun()
            return True
    return False

# ana uygulama
def main():
    # Başlangıçta verileri yükle
    if st.session_state.last_refresh == 0 or time.time() - st.session_state.last_refresh > 30:
        # 30 saniyeden fazla zaman geçtiyse veya hiç yüklenmemişse yeniden yükle
        with st.spinner(""):
            fetch_todos()
    
    # Önceki işlemde bir aksiyon yapıldıysa ve sayfayı yenilememiz gerekiyorsa
    if st.session_state.action_performed:
        st.session_state.action_performed = False
        st.rerun()
    
    # To do ekleme formu
    with st.form("todo_form", clear_on_submit=True):
        st.subheader("Yeni To do Ekle")
        title = st.text_input("Başlık")
        description = st.text_area("Açıklama")
        submitted = st.form_submit_button("Ekle")
        
        if submitted and title:
            # Form gönderildi ve başlık doluysa
            success_placeholder = st.empty()
            with st.spinner(""):
                if add_todo(title, description):
                    success_placeholder.success("To do başarıyla eklendi!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    success_placeholder.error("Todo eklenirken bir hata oluştu.")
    
    # Yenileme butonu ve Todo listesi
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.subheader("To do List")
    with col2:
        if st.button("🔄 Yenile"):
            with st.spinner(""):
                fetch_todos()
                st.rerun()
    
    # To do listele
    todos = st.session_state.todos
    
    if not todos:
        st.info("Henüz hiç to do yok. Yeni bir to do ekleyin!")
    else:
        # Tüm todoları tek seferde işle
        for todo in todos:
            # Her todo için benzersiz key oluştur
            todo_id = todo["id"]
            
            col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
            
            with col1:
                if todo["completed"]:
                    # HTML kullanarak üstünü çiz
                    st.markdown(f"<s>{todo['title']}</s>", unsafe_allow_html=True)
                else:
                    st.write(todo["title"])
                
                with st.expander("Detay"):
                    st.write(todo["description"])
            
            with col2:
                # Checkbox key'i
                checkbox_key = f"check_{todo_id}"
                
                # Checkbox oluştur
                status = st.checkbox(
                    "Tamamlandı", 
                    value=todo["completed"], 
                    key=checkbox_key,
                    on_change=handle_status_change,
                    args=(todo, not todo["completed"])
                )
            
            with col3:
                # Silme butonu
                if st.button("Sil", key=f"delete_{todo_id}"):
                    handle_delete(todo_id)

if __name__ == "__main__":
    main() 