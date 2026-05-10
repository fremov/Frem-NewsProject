# Используем Node.js
FROM node:20-slim

WORKDIR /app

# Копируем конфиги
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальной код
COPY . .

# Собираем проект (Next.js требует сборки для продакшена)
RUN npm run build

# Открываем порт
EXPOSE 3000

# Запускаем сервер
CMD ["npm", "start"]