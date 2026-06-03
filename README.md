# Zadanie 2 - Sprawozdanie

## Stworzony pipeline zawiera:

## 1. Klonowanie plików potrzebnych do zbudowania obrazu 

## 2. Definiowanie metadanych 

Postanowiłem zastosować takie rodzaje typowania ponieważ Pan Doktor takie zastosował w swoim przykładzie, ale są też inne mniej znaczące powody:
* Tag `semver` - zrozumiały dla ludzi, jest krótki i jest zgodny ze specyfikacją Semantic Versioning. (https://semver.org/) 
* Tag `sha` - unikalny dla każdego commita, co eliminuje błąd ludzki (w przypadku ataku haker nie może podmienić tego tagu lub w razie awarii bot ma unikalny tag i może wrócić do starej działającej wersji) (https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

## 3. Uruchamianie QEMU (do arm64)

## 4. Uruchamianie Buildx

## 5. Logowanie na DockerHub (żeby obsługiwać cache)

## 6. Logowanie na GHCR 

## 7. Budowanie Docker Image lokalnie - stworzenie obrazu, który będzie testowany

Zastosowałem stały tag `cache` ponieważ gdybym go nie użył to nie miałbym skąd pobrać tego cache, bo podczas tworzenia otrzymałbym nowy tag, który jeszcze nie istnieje

## 8. Uruchamienie skanera Trivy
Skaner przerwie pracę pipline, jeżeli napotka błędy `CRITICAL` lub `HIGH` (co się wydarzyło).

Problem okazał się `debian 12.14`, który ma `HIGH: 7`, `CRITICAL: 2` błędów. Widać to w workflow: `Wyrzucenie wielopratofrmowej budowy dla obrazu testowego v1.0.3`. Zgodnie z zadaniem obraz nie został wysłany do ghcr.io, ani cache na DockerHub

## 9. Budowanie i wysyłanie bezpiecznego obrazu Docker oraz Cache

Tryb `max` eksportuje wszystkie etapy budowy (nie trzeba teraz pobierać bibliotek do Pythona z pliku `requirements.txt`)