FROM node:21.7.3-alpine as build

WORKDIR /app

# Копируем package.json и package-lock.json
#COPY ./frontend/package*.json ./

COPY ./frontend ./

RUN npm install

RUN npm run build

# Финальный образ для запуска
FROM node:21.7.3-alpine

WORKDIR /app

# Устанавливаем serve глобально
RUN npm install -g serve

# Копируем собранные файлы из стадии сборки
COPY --from=build /app/build ./build

# Открываем порт (по умолчанию serve раздаёт на 5000)
EXPOSE 8080

# Запускаем serve для раздачи build-папки
CMD ["serve", "-s", "build", "-l", "8080"]

