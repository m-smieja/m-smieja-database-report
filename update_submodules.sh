#!/bin/bash
# Skrypt do aktualizacji submodułów

echo "Aktualizuję submoduły..."
git submodule update --remote --merge

echo ""
echo "Status submodułów:"
git submodule status

echo ""
echo "Czy chcesz zacommitować zmiany? (t/n)"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Tt]$ ]]; then
    git add .
    git commit -m "Update submodules"
    echo "Zmiany zacommitowane."
fi
