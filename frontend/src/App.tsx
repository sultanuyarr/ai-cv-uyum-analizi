```
import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface AnalysisResult {
  id: number;
  status: string;
  score: number;
  result: {
    overall_score: number;
    missing_skills: string[];
    recommendations: string[];
  };
  cv_text_preview: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobText, setJobText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !jobText) {
      setError('Lütfen hem CV dosyasını yükleyin hem de ilan metnini girin.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_text', jobText);

    try {
      const response = await fetch('http://localhost:8000/analysis/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analiz sırasında bir hata oluştu.');
      }

      const data = await response.json();
      
      // Since our MVP returns simplified result immediately or we poll
      // For this MVP version, endpoint returns result directly (simulated sync) similar to our plan
      // Let's assume we get the full result or fetch it.
      // Endpoint returned: {id, status, score}
      // Let's fetch the full details immediately
      
      const detailResponse = await fetch(`http://localhost:8000/analysis/${data.id}`);
const detailData = await detailResponse.json();
setResult(detailData);

    } catch (err: any) {
    setError(err.message || 'Bir hata oluştu.');
} finally {
    setLoading(false);
}
  };

return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4">
        <header className="mb-10 text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Destekli İş / Staj Uyum Analizi</h1>
            <p className="text-gray-600">CV'nizi yükleyin, İlanı yapıştırın, Uyum Skorunuzu Öğrenin.</p>
        </header>

        <main className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Form Section */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <Upload className="w-5 h-5" /> Analiz Başlat
                </h2>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">CV Yükle (PDF/DOCX)</label>
                        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 hover:bg-gray-50 transition-colors text-center cursor-pointer relative">
                            <input
                                type="file"
                                accept=".pdf,.docx"
                                onChange={handleFileChange}
                                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                            />
                            <div className="pointer-events-none">
                                {file ? (
                                    <div className="flex items-center justify-center gap-2 text-green-600 font-medium">
                                        <FileText className="w-5 h-5" /> {file.name}
                                    </div>
                                ) : (
                                    <span className="text-gray-500">Dosya seçmek için tıklayın veya sürükleyin</span>
                                )}
                            </div>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">İlan Metni</label>
                        <textarea
                            value={jobText}
                            onChange={(e) => setJobText(e.target.value)}
                            rows={6}
                            className="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="İş ilanı açıklamasını buraya yapıştırın..."
                        ></textarea>
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-600 p-3 rounded-lg flex items-center gap-2 text-sm">
                            <AlertCircle className="w-4 h-4" /> {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-5 h-5 animate-spin" /> Analiz Ediliyor...
                            </>
                        ) : (
                            'Analizi Başlat'
                        )}
                    </button>
                </form>
            </div>

            {/* Result Section */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <CheckCircle className="w-5 h-5" /> Analiz Sonucu
                </h2>

                {result ? (
                    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
                        <div className="text-center p-6 bg-blue-50 rounded-xl">
                            <div className="text-sm text-gray-600 mb-1">Genel Uyum Skoru</div>
                            <div className="text-5xl font-bold text-blue-600 mb-2">{result.score}/100</div>
                            <div className="text-sm text-blue-800 font-medium">
                                {result.score > 70 ? 'Yüksek Uyum' : result.score > 40 ? 'Orta Uyum' : 'Düşük Uyum'}
                            </div>
                        </div>

                        <div>
                            <h3 className="font-semibold text-gray-900 mb-2">Eksik Beceriler</h3>
                            {result.result.missing_skills.length > 0 ? (
                                <div className="flex flex-wrap gap-2">
                                    {result.result.missing_skills.map((skill, idx) => (
                                        <span key={idx} className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium">
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-sm text-green-600 font-medium">Harika! Önemli bir eksik bulunamadı.</p>
                            )}
                        </div>

                        <div>
                            <h3 className="font-semibold text-gray-900 mb-2">Öneriler</h3>
                            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                                {result.result.recommendations.map((rec, idx) => (
                                    <li key={idx}>{rec}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-gray-400 min-h-[300px]">
                        <FileText className="w-16 h-16 mb-4 opacity-20" />
                        <p>Sonuçları görmek için analiz başlatın.</p>
                    </div>
                )}
            </div>
        </main>
    </div>
);
}

export default App;
```
