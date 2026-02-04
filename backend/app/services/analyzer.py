import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

class LocalAnalyzer:
    def __init__(self):
        self.stop_words = ["ve", "ile", "için", "bir", "bu", "şu", "o", "de", "da", "ki", "mi", "mı", "mu", "mü", "ben", "sen", "o", "biz", "siz", "onlar"]
        
        # Güncellenmiş Meslek Haritası (Core/Support Ayrımı)
        self.CAREER_MAP = {
            "Yazılım Geliştirici": {
                "core": ["python", "java", "javascript", "typescript", "c#", ".net", "go", "php", "sql", "c++"],
                "support": ["react", "node", "git", "docker", "aws", "kubernates", "html", "css", "mongodb", "postgresql", "mysql", "redis", "linux", "agile", "scrum", "rest api"],
                "soft": ["problem çözme", "analitik düşünme", "takım çalışması", "sürekli öğrenme"],
                "description": "Yazılım sistemleri tasarlar, geliştirir ve bakımını yapar. Kod kalitesine ve mimariye odaklanır."
            },
            "Veri Analisti / Bilimci": {
                "core": ["python", "sql", "r", "istatistik", "matematik"],
                "support": ["excel", "pandas", "numpy", "tableau", "power bi", "looker", "matplotlib", "seaborn", "big data", "hadoop", "spark", "etl", "veri temizleme"],
                "soft": ["analitik düşünme", "merak", "iletişim", "sunum", "stoytelling"],
                "description": "Verilerden anlamlı içgörüler çıkarır, görselleştirir ve karar süreçlerini destekler."
            },
            "Dijital Pazarlama Uzmanı": {
                "core": ["seo", "sem", "google ads", "facebook ads", "sosyal medya yönetimi", "dijital pazarlama"],
                "support": ["analytics", "google analytics", "email marketing", "crm", "hubspot", "copywriting", "içerik üretimi", "canva", "photoshop", "video kurgu"],
                "soft": ["yaratıcılık", "iletişim", "trend takibi", "analiz"],
                "description": "Dijital kanalları kullanarak markaların görünürlüğünü artırır, kampanyalar yönetir."
            },
            "Proje Yöneticisi": {
                "core": ["proje yönetimi", "planlama", "bütçe yönetimi", "risk yönetimi"],
                "support": ["scrum", "agile", "kanban", "waterfall", "jira", "trello", "asana", "ms project", "koordinasyon", "paydaş yönetimi"],
                "soft": ["liderlik", "iletişim", "zaman yönetimi", "kriz yönetimi", "müzakere"],
                "description": "Projelerin zamanında, bütçe dahilinde ve hedeflere uygun tamamlanmasını sağlar."
            },
            "Satış / Müşteri Temsilcisi": {
                "core": ["satış", "ikna", "müşteri ilişkileri", "pazarlama"],
                "support": ["crm", "salesforce", "teklif hazırlama", "sözleşme", "b2b", "b2c", "cold calling", "sunum", "raporlama"],
                "soft": ["iletişim", "ikna kabiliyeti", "dayanıklılık", "hedef odaklılık", "dinleme"],
                "description": "Ürün veya hizmetlerin satışını gerçekleştirir, müşteri portföyünü yönetir."
            },
             "Muhasebe / Finans": {
                "core": ["muhasebe", "finans", "genel muhasebe", "vergi", "maliyet muhasebesi"],
                "support": ["excel", "ileri excel", "logo", "netsis", "sap", "mikro", "zirve", "fatura", "bordro", "sgk", "beyanname", "denetim"],
                "soft": ["dikkat", "dürüstlük", "analitik", "düzen", "sorumluluk"],
                "description": "Mali kayıtları tutar, raporlar ve yasal süreçleri takip eder."
            }
        }

    def clean_text(self, text: str) -> str:
        text = text.lower()
        # Noktalama işaretlerini boşlukla değiştir, böylece "python." gibi durumlarda kelime ayrışsın
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        filtered_words = [w for w in text.split() if w not in self.stop_words]
        return " ".join(filtered_words)

    def extract_cv_details(self, cv_text: str) -> Dict[str, Any]:
        """CV metninden temel bilgileri ve tüm bilinen yetkinlikleri çıkarır."""
        clean_cv = self.clean_text(cv_text)
        
        # 1. Becerileri Çıkar
        # Tüm mesleklerdeki keywordleri topla
        all_keywords = set()
        for role, details in self.CAREER_MAP.items():
            all_keywords.update(details["core"])
            all_keywords.update(details["support"])
            all_keywords.update(details["soft"])
        
        found_skills = []
        for kw in all_keywords:
            # Tam kelime eşleşmesi için boşluklu kontrol
            if f" {kw} " in f" {clean_cv} ":
                found_skills.append(kw)
        
        # 2. Eğitim Seviyesi
        education_score = 0
        education_label = "Lise / Belirtilmedi"
        
        if any(w in clean_cv for w in ["doktora", "phd"]):
            education_label = "Doktora"
            education_score = 100
        elif any(w in clean_cv for w in ["yüksek lisans", "master"]):
            education_label = "Yüksek Lisans"
            education_score = 90
        elif any(w in clean_cv for w in ["lisans", "fakülte", "mühendisliği", "bölümü", "üniversitesi"]):
            # Lisans genelde standarttır
            education_label = "Lisans"
            education_score = 80
        elif any(w in clean_cv for w in ["ön lisans", "meslek yüksekokulu", "myo"]):
            education_label = "Ön Lisans"
            education_score = 60
        elif any(w in clean_cv for w in ["lise"]):
            education_label = "Lise"
            education_score = 40

        # 3. Deneyim Seviyesi
        experience_label = "Giriş Seviyesi"
        experience_score = 40 # Junior default
        
        years = re.findall(r'(\d+)\s+(?:yıl|sene)', clean_cv)
        max_year = 0
        if years:
            max_year = max([int(y) for y in years])
        
        if max_year > 5:
            experience_label = "Senior (Deneyimli)"
            experience_score = 100
        elif max_year >= 2:
            experience_label = "Mid-Level (Orta)"
            experience_score = 70
        elif max_year >= 1:
            experience_label = "Junior (Giriş)"
            experience_score = 50
        elif "staj" in clean_cv or "stajyer" in clean_cv:
            experience_label = "Stajyer"
            experience_score = 40 # Stajyer de olsa puan ver, user: 'cezalandırılmasın'

        return {
            "skills": found_skills,
            "education": education_label,
            "education_int": education_score,
            "experience": experience_label,
            "experience_int": experience_score
        }

    def suggest_careers(self, cv_text: str) -> List[Dict[str, Any]]:
        """Ağırlıklı skorlama ile kariyer önerileri."""
        cv_details = self.extract_cv_details(cv_text)
        cv_skills = set(cv_details["skills"])
        
        suggestions = []
        
        for role, details in self.CAREER_MAP.items():
            # Ağırlıklar
            W_CORE = 0.50
            W_SUPPORT = 0.25
            W_EDU = 0.15
            W_EXP = 0.10
            
            # 1. Çekirdek Beceri Skoru
            core_matches = [kw for kw in details["core"] if kw in cv_skills]
            # Hedef: 4 çekirdek yetkinlik tam puan getirir (User logic: artışla sınırlı)
            core_score_raw = min(len(core_matches) / 4.0, 1.0) * 100
            
            # 2. Destekleyici Beceri Skoru
            support_matches = [kw for kw in details["support"] if kw in cv_skills]
            # Hedef: 4 destekleyici yetkinlik tam puan
            support_score_raw = min(len(support_matches) / 4.0, 1.0) * 100
            
            # 3. Eğitim ve Deneyim
            # Bu meslek için eğitim ne kadar kritik? Yazılım için orta, Doktorluk için yüksek.
            # Şimdilik herkese CV'deki puanı verelim.
            edu_score = cv_details["education_int"]
            exp_score = cv_details["experience_int"]
            
            # Toplam Ağırlıklı Skor
            final_score = (
                (core_score_raw * W_CORE) + 
                (support_score_raw * W_SUPPORT) + 
                (edu_score * W_EDU) + 
                (exp_score * W_EXP)
            )
            
            # 4. Taban Puan ve Bonus Kuralları
            if len(core_matches) >= 3:
                final_score = max(final_score, 40)
                final_score += 10 # 3+ core varsa extra boost
            elif len(core_matches) >= 2:
                final_score = max(final_score, 30)
                final_score += 5

            # 5. Normalizasyon ve Sınırlama
            final_score = min(final_score, 100)
            
            # Sadece biraz olsun alakalıysa listeye ekle
            if len(core_matches) > 0 or len(support_matches) > 1:
                
                # Feedback Oluşturma
                missing_core = [kw for kw in details["core"] if kw not in core_matches][:3]
                reason = "Becerileriniz bu rolle genel olarak örtüşüyor."
                
                if final_score < 40:
                    reason = "Teknik altyapı başlangıç seviyesinde, proje deneyimi ve framework bilgisi ile desteklenmeli."
                elif final_score < 70:
                    reason = f"Temel {len(core_matches)} yetkinliğe sahipsiniz. {', '.join(missing_core)} gibi alanlarda gelişim sizi öne taşır."
                else:
                    reason = "Harika bir eşleşme! Hem çekirdek hem yardımcı yetkinlikleriniz bu rol için çok uygun."

                suggestions.append({
                    "title": role,
                    "score": int(final_score),
                    "reason": reason,
                    "missing": missing_core,
                    "description": details["description"]
                })
        
        # Puana göre sırala ve ilk 3'ü al
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions[:3]

    def analyze(self, cv_text: str, job_text: str) -> Dict[str, Any]:
        """Tam analiz fonksiyonu."""
        
        cv_details = self.extract_cv_details(cv_text)
        career_suggestions = self.suggest_careers(cv_text)
        
        # İlan Uyumu
        job_match_result = {}
        clean_job = self.clean_text(job_text)
        
        if len(clean_job) < 20:
             job_match_result = {
                 "status": "INVALID_INPUT",
                 "score": 0,
                 "feedback": "İlan metni çok kısa...",
                 "missing_skills": []
             }
        else:
            # Mevcut "analyze" logic'ini koru ama UI text kurallarını güncelle
            # ... eski logic tekrarı ...
            clean_cv = self.clean_text(cv_text)
            
            # Basit overlap skoru (TF-IDF yerine daha kontrol edilebilir)
            job_words = set(clean_job.split())
            cv_words = set(clean_cv.split())
            common = job_words.intersection(cv_words)
            
            overlap_score = 0
            if len(job_words) > 0:
                 overlap_score = (len(common) / len(job_words)) * 100
                 
            # Biraz boost
            final_score = min(overlap_score * 2.5, 95) # Basit bir scaling
            final_score = int(final_score)

            status_label = "DÜŞÜK BAŞLANGIÇ ÇİZGİSİ"
            if final_score >= 60:
                status_label = "YÜKSEK UYUM"
                feedback = "İlanla aranızda güçlü bir uyum var."
            elif final_score >= 30:
                status_label = "GELİŞTİRİLEBİLİR UYUM"
                feedback = "Uygunluk var ancak bazı teknik gereksinimler eksik görünüyor."
            else:
                status_label = "DÜŞÜK AMA BAŞLANGIÇ İÇİN UYGUN"
                feedback = "İlan beklentileri ile CV'niz arasında farklar var, ancak temel becerilerinizle başvuruyu değerlendirebilirsiniz."

            # Eksik becerileri bul (basitçe)
            missing = []
            # CAREER_MAP'ten tüm keywordleri alıp ilanda geçenleri bul
            all_known = set()
            for d in self.CAREER_MAP.values():
                all_known.update(d["core"])
                all_known.update(d["support"])
            
            for kw in all_known:
                if kw in clean_job and kw not in clean_cv:
                    missing.append(kw)

            job_match_result = {
                "status": status_label,
                "score": final_score,
                "feedback": feedback,
                "missing_skills": list(set(missing))[:5]
            }

        return {
            "cv_analysis": {
                "skills": cv_details["skills"],
                "education": cv_details["education"],
                "experience": cv_details["experience"]
            },
            "career_suggestions": career_suggestions,
            "job_match": job_match_result
        }

analyzer = LocalAnalyzer()
