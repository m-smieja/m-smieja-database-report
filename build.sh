#!/bin/bash
# Skrypt do budowania dokumentacji

# Aktywacja wirtualnego środowiska
source venv/bin/activate

case "$1" in
    html)
        echo "Buduję dokumentację HTML..."
        make html
        echo "Gotowe! Otwórz _build/html/index.html"
        ;;
    pdf)
        echo "Buduję dokumentację PDF..."
        sphinx-build -b pdf . _build/pdf
        echo "Gotowe! PDF znajduje się w _build/pdf/"
        ;;
    clean)
        echo "Czyszczę pliki build..."
        rm -rf _build/
        ;;
    serve)
        echo "Uruchamiam serwer z auto-reload..."
        sphinx-autobuild . _build/html
        ;;
    update)
        echo "Aktualizuję wszystkie submoduły..."
        git submodule update --remote --merge
        ;;
    *)
        echo "Użycie: $0 {html|pdf|clean|serve|update}"
        exit 1
        ;;
esac
