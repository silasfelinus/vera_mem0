FROM cgr.dev/chainguard/node:20-dev

WORKDIR /vera

COPY . .

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev"]

