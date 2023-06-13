ARG BASE_IMAGE_TAG=candlestick_base_image

FROM --platform=linux/amd64 ${BASE_IMAGE_TAG}

COPY build/entrypoint.sh .
COPY . .

RUN poetry install

EXPOSE 8081

RUN chmod a+x ./entrypoint.sh

CMD ./entrypoint.sh
