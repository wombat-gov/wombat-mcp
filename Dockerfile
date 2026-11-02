FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir hatchling build

COPY pyproject.toml README.md VERSION ./
COPY wombat_mcp/ wombat_mcp/

RUN pip install --no-cache-dir .

EXPOSE 3001

CMD ["wombat-mcp"]
