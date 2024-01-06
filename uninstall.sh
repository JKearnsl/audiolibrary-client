#!/bin/sh

echo 'Удаление программы AudioLibrary'

set -e

if [ "$(id -u)" -ne 0 ]; then
  echo "Ошибка: этот скрипт должен быть запущен с правами суперпользователя." >&2
  exit 1
fi

# Remove app
echo 'Удаление приложения...'
INSTALL_PATH=/opt/audiolibrary

rm -rf ${INSTALL_PATH:?}/

# Remove files
getent passwd | while IFS=: read -r _ _ uid _ _ home _; do
  if [ "$uid" -ge 1000 ] && [ -d "$home" ]; then
    rm -rf "${home:?}/.audiolibrary"
  fi
done

# Remove executable
rm -f /usr/local/bin/audiolibrary

# Remove .desktop file
rm -f /usr/share/applications/audiolibrary.desktop
update-desktop-database /usr/share/applications

# Remove icon
rm -f /usr/share/icons/hicolor/64x64/apps/audiolibrary.png
rm -f /usr/share/icons/hicolor/128x128/apps/audiolibrary.png
rm -f /usr/share/icons/hicolor/256x256/apps/audiolibrary.png

# Update icon cache
# GNOME
if [ -x "$(command -v gtk-update-icon-cache)" ]; then
    echo "Обновление кэша иконок GNOME..."
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor/
fi

# KDE
if [ -x "$(command -v kbuildsycoca5)" ]; then
    echo "Обновление кэша иконок KDE..."
    kbuildsycoca5 --noincremental
fi

# XFCE
if [ -x "$(command -v xfce4-panel)" ]; then
    echo "Обновление кэша иконок XFCE..."
    xfce4-panel --restart
fi

# LXDE
if [ -x "$(command -v lxpanelctl)" ]; then
    echo "Обновление кэша иконок LXDE..."
    lxpanelctl restart
fi

# MATE
if [ -x "$(command -v mate-panel)" ]; then
    echo "Обновление кэша иконок MATE..."
    mate-panel --replace &
fi

echo "Обновление кэша иконок завершено."

echo 'Удаление успешно завершено.'
