FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLCONFIGDIR=/tmp/matplotlib \
    JUPYTER_CONFIG_DIR=/tmp/jupyter-config \
    JUPYTER_RUNTIME_DIR=/tmp/jupyter-runtime
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && useradd --create-home --uid 1000 apprenant \
    && mkdir -p /workspace && chown apprenant:apprenant /workspace
USER apprenant
WORKDIR /workspace
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.root_dir=/workspace"]
