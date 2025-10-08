# ベースイメージ例
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# 必要な依存パッケージ
RUN apt-get update && apt-get install -y curl unzip

# Supabase CLI を手動でダウンロードしてインストール
RUN curl -L "https://github.com/supabase/cli/releases/latest/download/supabase_linux_arm64.tar.gz" -o supabase.tar.gz && \
    tar -xzf supabase.tar.gz -C /usr/local/bin && \
    rm supabase.tar.gz

# パス確認
RUN supabase --version
