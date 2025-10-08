FROM node:22.7.0
RUN apt update; apt install -y wget software-properties-common apt-transport-https git

# Flutter SDK をダウンロードしてパスを通す
RUN git clone https://github.com/flutter/flutter.git /opt/flutter -b stable
ENV PATH="/opt/flutter/bin:/opt/flutter/bin/cache/dart-sdk/bin:${PATH}"
# Supabase CLI を手動でダウンロードしてインストール
RUN curl -L "https://github.com/supabase/cli/releases/latest/download/supabase_linux_arm64.tar.gz" -o supabase.tar.gz && \
    tar -xzf supabase.tar.gz -C /usr/local/bin && \
    rm supabase.tar.gz

# 安全なディレクトリとして追加
RUN git config --global --add safe.directory /workspaces/book_scanner_app

# 作業ディレクトリ
WORKDIR /workspaces/book_scanner_app