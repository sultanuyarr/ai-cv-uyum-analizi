İş ve staj başvuru süreçlerinde adayların özgeçmişlerinin (CV) başvurulan pozisyonlarla uyumu büyük önem taşımaktadır. Özellikle öğrenci, stajyer ve yeni mezun adaylar, sahip oldukları yetkinliklerin hangi meslek gruplarına daha uygun olduğunu belirlemekte zorlanabilmektedir. Bu proje, adayların CV’lerini analiz ederek onların yetkinlik profillerine uygun meslek önerileri sunmayı amaçlayan, yapay zekâ destekli bir karar destek sistemi geliştirmeyi hedeflemektedir.
Özellikle **stajyerler, öğrenciler ve yeni mezunlar** için,  
“Bu CV ile hangi meslek bana daha uygun?” sorusuna anlaşılır ve yönlendirici cevaplar sunar.

Kullanılan Teknolojiler

### Frontend
- React + Vite
- TypeScript
- TailwindCSS

### Backend
- Python
- FastAPI
- SQLite

### Analiz
- Kural tabanlı yetkinlik çıkarımı
- Meslek–yetkinlik eşleştirme modeli
- Ağırlıklı uyum skoru hesaplama

 Sistem Nasıl Çalışır?

1. Kullanıcı CV’sini (PDF / DOCX) sisteme yükler  
2. CV’den metin çıkarılır ve analiz edilir  
3. Yetkinlikler, eğitim durumu ve deneyim seviyesi belirlenir  
4. Önceden tanımlı meslek profilleri ile karşılaştırma yapılır  
5. Kullanıcıya en uygun meslekler ve uyum skorları sunulur  


  Sunulan Çıktılar

- Genel meslek uyum skorları  
- Mesleğe uygunluk nedenleri  
- Geliştirilmesi gereken alanlar  
- Anlaşılır ve sade rapor ekranı  
