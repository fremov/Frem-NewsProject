import React, {useEffect, useState} from 'react';
import {
    StyleSheet, Text, View, FlatList,
    TouchableOpacity, Linking, ActivityIndicator, SafeAreaView
} from 'react-native';
import axios from 'axios';

// ВАЖНО: Если запускаешь на реальном телефоне, замени '127.0.0.1'
// на локальный IP твоего компьютера (например, '192.168.1.5')
const API_URL = 'http://5.35.93.59:8000/news';

export default function App() {
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchNews = async () => {
        try {
            const response = await axios.get(API_URL);
            setNews(response.data);
        } catch (error) {
            console.error("Ошибка запроса:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNews();
    }, []);

    const renderItem = ({item}) => (
        <View style={styles.card}>
            <TouchableOpacity onPress={() => Linking.openURL(item.source_url)}>
                <Text style={styles.title}>{item.title}</Text>
            </TouchableOpacity>
            <Text style={styles.content}>{item.content}</Text>
            <Text style={styles.date}>{new Date(item.created_at).toLocaleDateString()}</Text>
        </View>
    );

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTitle}>News Feed</Text>
            </View>

            {loading ? (
                <ActivityIndicator size="large" color="#38bdf8"/>
            ) : (
                <FlatList
                    data={news}
                    keyExtractor={(item) => item.id.toString()}
                    renderItem={renderItem}
                    contentContainerStyle={styles.list}
                />
            )}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {flex: 1, backgroundColor: '#0f172a'},
    header: {padding: 20, paddingTop: 40, backgroundColor: '#1e293b'},
    headerTitle: {fontSize: 24, fontWeight: 'bold', color: '#38bdf8'},
    list: {padding: 15},
    card: {
        backgroundColor: '#1e293b',
        padding: 15,
        borderRadius: 12,
        marginBottom: 15,
        borderWidth: 1,
        borderColor: '#334155'
    },
    title: {fontSize: 18, fontWeight: 'bold', color: '#f8fafc', marginBottom: 10},
    content: {fontSize: 14, color: '#94a3b8', lineHeight: 20},
    date: {fontSize: 10, color: '#64748b', marginTop: 10, textAlign: 'right'}
});