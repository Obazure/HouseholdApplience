FROM node:14.10.0

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build-docs
RUN npm run build
