import axios from 'axios';

const API_URL = 'http://5.35.93.59:8000';

export const fetchNews = async () => {
    try {
        const response = await axios.get(`${API_URL}/news`);
        return response.data;
    } catch (error) {
        console.error("Ошибка при получении новостей:", error);
        return [];
    }
};