
# Stage 1: Base build stage
From python:3.12-slim as base

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set Python enviorment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install dependencies first for caching benefit
RUN pip install --upgrade pip
COPY src/requirements/base.txt \
     /app/requirements/
RUN pip install --no-cache-dir -r requirements/base.txt


# Stage 2: Production stage
FROM base
