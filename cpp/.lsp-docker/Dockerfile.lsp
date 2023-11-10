FROM debian:bookworm

RUN apt-get update -yqq && apt-get install build-essential clangd -yqq
