FROM node:20-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Копируем конфиги
COPY package*.json ./

# Устанавливаем основные зависимости
RUN npm install

# ПРЕДУСТАНОВКА NGROK (чтобы не было вопроса в консоли)
RUN npm install -g @expo/ngrok@^4.1.0

# Устанавливаем expo-cli
RUN npm install -g expo-cli

COPY . .

EXPOSE 8081 19000 19001 19002

# Используем флаг --non-interactive на всякий случай
CMD ["npx", "expo", "start", "--tunnel", "--non-interactive"]