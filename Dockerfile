
# Stage 1: Base build stage
From python:3.12-slim as builder

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
# This stage I'm quite not sure why it's here again. Guess it's about checking if it's installed or not and such as cahcing thing.
From python:3.12-slim 

# Create user who's not root authentication
# and give ownership of app folder to appuser
RUN useradd -m -r appuser &&\
    mkdir /app && \
    chown -R appuser /app

# Copy the Python dependencies from the Builder Stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Switch to Non-root user
USER appuser

# Expose the application port
EXPOSE 8081
