FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY index.html .
COPY main.jsx .

EXPOSE 5173

CMD ["npm", "run", "start"]