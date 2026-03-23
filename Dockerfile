FROM nginx:alpine
RUN echo "<h1>Primera imagen publicada desde GitHub Actions!</h1>" > /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]