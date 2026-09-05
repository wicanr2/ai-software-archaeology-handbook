# 本專案的首個 PDF 工具鏈。既有 report-docx 僅有 DOCX；此映像補齊分頁、SVG 與 PDF 驗收。
FROM python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36
ARG DEBIAN_SNAPSHOT=20260901T000000Z
RUN rm /etc/apt/sources.list.d/debian.sources \
 && printf 'deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/%s/ trixie main\n' "$DEBIAN_SNAPSHOT" > /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    pandoc fonts-noto-cjk fonts-dejavu-core fontconfig \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
    poppler-utils librsvg2-bin \
 && dpkg-query -W > /opt/debian-packages.txt \
 && rm -rf /var/lib/apt/lists
COPY tools/pdf/requirements.txt /opt/pdf-requirements.txt
RUN pip install --no-cache-dir -r /opt/pdf-requirements.txt \
 && pip check \
 && pip freeze > /opt/python-packages.txt
ENV PYTHONDONTWRITEBYTECODE=1 XDG_CACHE_HOME=/tmp/osa-cache
WORKDIR /work
CMD ["python", "tools/pdf/build.py"]
