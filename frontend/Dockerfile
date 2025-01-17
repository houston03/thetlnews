# Используем официальный образ Node.js
FROM node:14

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальные файлы приложения
COPY . .

# Сборка приложения
RUN npm run build

# Используем официальный образ Nginx для обслуживания статических файлов
FROM nginx:alpine

# Копируем собранные файлы в директорию Nginx
COPY --from=0 /app/build /usr/share/nginx/html
# Копируем конфигурационный файл Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Открываем порт 80
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]
