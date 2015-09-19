server {
    # Define the server block
    listen 80;
    server_name {{ site.domain.name }};
    root "{{ site.root }}";

    index index.php;
    client_max_body_size 100m;
    charset utf-8;

    # Rewrite rules
    location / {
        try_files  $uri $uri/ /index.php;
    }

    {% if site.gzip %}
        # Enabling gzip compression
        gzip  on;
        gzip_http_version 1.1;
        gzip_vary on;
        gzip_comp_level 6;
        gzip_proxied any;
        gzip_types text/plain text/css application/json application/x-javascript application/xml application/xml+rss text/javascript application/javascript text/x-js;
        gzip_buffers 16 8k;
        gzip_disable "MSIE [1-6]\.(?!.*SV1)";
    {% endif %}

    # Logging
    access_log off;

    # Pass PHP scripts to php-fpm
    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/var/run/php5-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_intercept_errors off;
        fastcgi_buffer_size 16k;
        fastcgi_buffers 4 16k;
    }
}