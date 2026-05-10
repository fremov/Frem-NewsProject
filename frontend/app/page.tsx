'use client';

import React, {useState, useEffect} from 'react';
import ReactMarkdown from 'react-markdown';

// Интерфейс для типизации новости
interface NewsItem {
    id: number;
    title: string;
    content: string;
    source_url: string;
    source: string;
    created_at: string;
}

export default function Home() {
    const [news, setNews] = useState<NewsItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);

    // Состояния для фильтрации
    const [filter, setFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        // Укажи здесь адрес своего бэкенда
        fetch('http://5.35.93.59:8000/news')
            .then((res) => res.json())
            .then((data) => {
                setNews(data);
                setLoading(false);
            })
            .catch((err) => console.error("Ошибка загрузки:", err));
    }, []);

    // Логика фильтрации
    const filteredNews = news.filter((item) => {
        const matchesSource = filter === 'all' || item.source === filter;
        const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesSource && matchesSearch;
    });

    if (loading) {
        return (
            <div className="min-h-screen bg-[#0f172a] flex items-center justify-center">
                <div className="text-blue-500 text-xl font-mono animate-pulse">Загрузка новостей...</div>
            </div>
        );
    }

    return (
        <main className="min-h-screen bg-[#0f172a] text-slate-200 p-4 md:p-8">
            {/* Шапка и поиск */}
            <div className="max-w-6xl mx-auto mb-10">
                <h1 className="text-4xl font-black mb-8 text-center tracking-tighter uppercase">
                    Frem <span className="text-blue-500">News</span>
                </h1>

                <div
                    className="flex flex-col md:flex-row gap-4 items-center justify-between bg-[#1e293b] p-4 rounded-2xl border border-slate-700">
                    {/* Кнопки фильтров */}
                    <div className="flex gap-2">
                        {['all', 'Habr', 'IGN'].map((s) => (
                            <button
                                key={s}
                                onClick={() => setFilter(s)}
                                className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${
                                    filter === s ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                                }`}
                            >
                                {s === 'all' ? 'Все' : s}
                            </button>
                        ))}
                    </div>

                    {/* Поле поиска */}
                    <input
                        type="text"
                        placeholder="Поиск по заголовкам..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full md:w-64 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-blue-500"
                    />
                </div>
            </div>

            {/* Сетка новостей */}
            <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredNews.map((item) => (
                    <article
                        key={item.id}
                        onClick={() => setSelectedNews(item)}
                        className="bg-[#1e293b] rounded-2xl border border-slate-700 p-6 hover:border-blue-500/50 hover:translate-y-[-4px] transition-all cursor-pointer flex flex-col h-full"
                    >
                        <div className="flex justify-between items-center mb-4">
              <span className={`text-[10px] font-black px-2 py-1 rounded ${
                  item.source === 'Habr' ? 'bg-blue-500/20 text-blue-400' : 'bg-red-500/20 text-red-400'
              }`}>
                {item.source}
              </span>
                            <span className="text-[10px] text-slate-500 font-mono">
                {new Date(item.created_at).toLocaleDateString()}
              </span>
                        </div>

                        <h2 className="text-xl font-bold mb-3 leading-tight line-clamp-2 text-white">
                            {item.title}
                        </h2>

                        <p className="text-slate-400 text-sm line-clamp-4 leading-relaxed mb-4">
                            {item.content}
                        </p>

                        <div
                            className="mt-auto pt-4 border-t border-slate-800 text-blue-400 text-xs font-bold uppercase tracking-wider">
                            Читать далее →
                        </div>
                    </article>
                ))}
            </div>

            {/* Модальное окно */}
            {selectedNews && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                    {/* Оверлей (фон) */}
                    <div
                        className="absolute inset-0 bg-black/90 backdrop-blur-md"
                        onClick={() => setSelectedNews(null)}
                    ></div>

                    {/* Контент модалки */}
                    <div
                        className="relative bg-[#1e293b] w-full max-w-4xl max-h-[85vh] rounded-3xl border border-slate-700 overflow-hidden flex flex-col shadow-2xl">
                        {/* Header модалки */}
                        <div className="p-6 border-b border-slate-800 flex justify-between items-start">
                            <div>
                                <div className="flex items-center gap-3 mb-2">
                                    <span
                                        className="text-blue-500 text-xs font-black uppercase tracking-widest">{selectedNews.source}</span>
                                    <span
                                        className="text-slate-500 text-xs">{new Date(selectedNews.created_at).toLocaleString()}</span>
                                </div>
                                <h2 className="text-2xl md:text-3xl font-bold text-white leading-tight">{selectedNews.title}</h2>
                            </div>
                            <button
                                onClick={() => setSelectedNews(null)}
                                className="p-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                     fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                                     strokeLinejoin="round">
                                    <line x1="18" y1="6" x2="6" y2="18"></line>
                                    <line x1="6" y1="6" x2="18" y2="18"></line>
                                </svg>
                            </button>
                        </div>

                        {/* Тело модалки */}
                        <div className="p-6 md:p-10 overflow-y-auto">
                            <div className="text-slate-300 text-lg leading-relaxed space-y-6">
                                <ReactMarkdown>
                                    {selectedNews.content}
                                </ReactMarkdown>
                            </div>

                            <div className="mt-12 pt-8 border-t border-slate-800 flex justify-center">
                                <a
                                    href={selectedNews.source_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-3 rounded-xl font-bold transition-colors shadow-lg shadow-blue-900/20"
                                >
                                    Открыть оригинал на {selectedNews.source}
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </main>
    );
}