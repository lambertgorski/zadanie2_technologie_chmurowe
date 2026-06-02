
FROM python:3.12-bookworm as builder 

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


# ze względu na to, że python jest językiem interpretowalnym można byłoby 
# pomyśleć, że można pominąć etap budowy, jednak ze względu na to, że niektóre
# biblioteki instalowane menadżerem pakietów `pip` nie zawierająca bezpośrednio
# kodu pythona a czasami pliki .C, które musiałby zostać skompilowane (szczególnie na linux)
# zaleca się zastosowanie multistage building

FROM python:3.12-slim-bookworm as prod


# postanowiłem nie używać obrazu `scratch` ponieważ 
# 1. skrypt pythona potrzebuje interpretera, dlatego niemogłem skompilować kodu do kodu maszynwego
#, który mógłby być uruchomiany na warstwie scratch
# 2. twórcy obrazu pythona przygotowali już lekki obraz przeznaczony do uruchomienia skryptu 


LABEL org.opencontainers.image.authors="Lambert Górski"

WORKDIR /usr/src/app

# instalacja curla do healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# stworzenie użytkownika ktory bedzie korzystał z aplikacji
RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser

# kopiowanie blibiotek do uruchomienia aplikacji
COPY --from=builder /root/.local /home/appuser/.local


RUN chown -R appuser:appuser /usr/src/app

COPY main.py .

#dodanie servera uvicorn (programu) do PATH
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/usr/src/app

#sprawdzamy czy możliwe jest dostanie się na strone główną aplikacji
#(przez flage -f gdy będzie błąd otrzymamy kod procesu=1 co 
#jest równe unhealthy)
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

USER appuser


#uruchamiamy server uvicorn na którym działa skrypt main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
