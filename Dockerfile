FROM python:3.7-slim as base-image
WORKDIR /service
RUN pip install "poetry~=1.8.0"
ADD pyproject.toml poetry.lock README.md ./
ADD makeqr makeqr
RUN poetry build
RUN python -m venv .venv
RUN .venv/bin/pip install dist/*.whl

FROM python:3.7-slim as runtime-image
WORKDIR /service
COPY --from=base-image /service/.venv ./.venv
ENTRYPOINT ["/service/.venv/bin/python3", "-m", "makeqr"]
