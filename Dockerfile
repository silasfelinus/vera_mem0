FROM node:18-alpine

COPY . .

RUN corepack enable && pnpm install

EXPOSE 3000

CMD ["npm", "dev"]
