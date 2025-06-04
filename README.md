# ToDoList Uygulaması

Bu proje, FastAPI, SQLite ve Streamlit kullanılarak geliştirilmiş basit bir TodoList uygulamasıdır.


## Kullanım

1. Backend ve Frontend'i ayrı terminal pencerelerinde çalıştırın
2. Tarayıcınızda `http://localhost:8501` adresine giderek uygulamayı kullanabilirsiniz

## Özellikler

- To do ekleme
- To do silme
- To do'ları tamamlandı olarak işaretleme/işareti kaldırma
- To do detaylarını görüntüleme
- SQLite veritabanında kalıcı veri depolama

## Teknolojiler

- **Backend**: FastAPI (Python)
- **Veritabanı**: SQLite
- **ORM**: SQLAlchemy
- **Frontend**: Streamlit
- **API İletişimi**: Requests kütüphanesi

## Proje Yapısı

```
FastApi/
├── Backend/
│   ├── database/       # Veritabanı bağlantısı ve yapılandırması
│   ├── models/         # SQLAlchemy veritabanı modelleri
│   ├── schemas/        # Pydantic modelleri (veri doğrulama şemaları)
│   └── main.py         # FastAPI uygulaması ve endpoint tanımları
├── Frontend/
│   └── app.py          # Streamlit kullanıcı arayüzü
└── README.md
```
