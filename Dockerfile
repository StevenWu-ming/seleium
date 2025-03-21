FROM --platform=linux/amd64 python:3.9-bullseye
WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxtst6 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libasound2 \
    fonts-liberation libu2f-udev libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO google-chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_134.0.6998.117-1_amd64.deb && \
    apt-get update && apt-get install -y ./google-chrome.deb && \
    rm google-chrome.deb

RUN ln -sf /usr/bin/google-chrome-stable /usr/bin/google-chrome

RUN CHROMEDRIVER_VERSION="134.0.6998.117" \
    && wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver-linux64.zip

RUN /usr/bin/google-chrome --version
RUN /usr/local/bin/chromedriver --version

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV CHROME_BIN=/usr/bin/google-chrome
ENV DOCKER_ENV=true
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--log-level", "debug"]