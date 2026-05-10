# Используем Node.js
FROM node:20-slim

WORKDIR /app

# Устанавливаем системные зависимости для Expo
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копируем package.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Устанавливаем expo-cli глобально
RUN npm install -g expo-cli

# Копируем весь проект
COPY . .

# Экспонируем порты:
# 19000 - Expo Packager
# 19001 - Metro Bundler
# 19002 - Expo Developer Tools
EXPOSE 19000 19001 19002 8081

# Запускаем приложение в режиме туннеля (чтобы телефон видел его через интернет)
CMD ["npx", "expo", "start", "--tunnel"]