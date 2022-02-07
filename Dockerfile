ARG PYCLOWDER_PYTHON=""
FROM clowder/extractors-simple-extractor${PYCLOWDER_PYTHON}:onbuild

RUN pip install opensmile

ENV EXTRACTION_FUNC="openSmileExtractor"
ENV EXTRACTION_MODULE="openSmileExtractor"
