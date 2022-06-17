FROM node:17.0.0-alpine

ENV NODE_ENV=production

WORKDIR /opt/frontend

COPY ./frontend/package.json ./frontend/yarn.lock /opt/frontend/

RUN yarn install --production --no-progress

COPY . .

CMD [ "yarn", "build" ]