FROM nginx:alpine

# Create a real logs directory (we'll mount a volume here at runtime)
RUN mkdir -p /var/log/nginx-files && chown -R nginx:nginx /var/log/nginx-files

# Copy our config into the image (no bind mounts needed)
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx","-g","daemon off;"]