FROM debian:bookworm-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_LINK_MODE=copy

# Setup workspace
RUN mkdir /workspace
WORKDIR /workspace
COPY . .

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    curl \
    git \
    make \
    && rm -rf /var/lib/apt/lists/* \
    && uv sync \
    # Install pre-commit hook.
    && uv run pre-commit install \
    # Shell completion
    && echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc \
    # Auto activate venv
    && echo 'source /workspace/.venv/bin/activate' >> ~/.bashrc

# Default command (can be overridden)
CMD ["/bin/bash"]
