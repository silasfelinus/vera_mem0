FROM node:18-alpine

WORKDIR /vera

COPY . .

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev"]
