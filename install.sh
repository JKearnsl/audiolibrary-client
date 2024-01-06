#!/bin/sh

echo 'Установка программы AudioLibrary'

set -e

if [ "$(id -u)" -ne 0 ]; then
  echo "Ошибка: этот скрипт должен быть запущен с правами суперпользователя." >&2
  exit 1
fi

# Check if python3.12 is installed
if ! [ -x "$(command -v python3.12)" ]; then
  echo 'Внимание: python3.12 не установлен.'

  # Install python3.12
  echo 'Установка python3.12...' >&2
  if [ -x "$(command -v apt)" ]; then
    apt install python3.12
  elif [ -x "$(command -v pacman)" ]; then
    pacman -S python3.12
  elif [ -x "$(command -v dnf)" ]; then
    dnf install python3.12
  elif [ -x "$(command -v zypper)" ]; then
    zypper install python3.12
  elif [ -x "$(command -v xbps-install)" ]; then
    xbps-install -S python3.12
  elif [ -x "$(command -v eopkg)" ]; then
    eopkg install python3.12
  elif [ -x "$(command -v emerge)" ]; then
    emerge -av python3.12
  elif [ -x "$(command -v pkg)" ]; then
    pkg install python3.12
  elif [ -x "$(command -v apk)" ]; then
    apk add python3.12
  elif [ -x "$(command -v swupd)" ]; then
    swupd bundle-add python3.12
  elif [ -x "$(command -v tazpkg)" ]; then
    tazpkg get-install python3.12
  elif [ -x "$(command -v guix)" ]; then
    guix install python3.12
  elif [ -x "$(command -v nix-env)" ]; then
    nix-env -i python3.12
  elif [ -x "$(command -v brew)" ]; then
    brew install python3.12
  elif [ -x "$(command -v yay)" ]; then
    yay -S python3.12
  elif [ -x "$(command -v snap)" ]; then
    snap install python3.12
  elif [ -x "$(command -v flatpak)" ]; then
    flatpak install python3.12
  elif [ -x "$(command -v termux)" ]; then
    pkg install python3.12
  elif [ -x "$(command -v pkg_add)" ]; then
    pkg_add python3.12
  elif [ -x "$(command -v kcp)" ]; then
    kcp -i python3.12
  else
    echo 'Ошибка: не удалось установить python3.12.' >&2
    echo 'Пожалуйста, установите python3.12 вручную и повторите попытку' >&2
    exit 1
  fi
fi

# Install icon
cp ./src/audiolibrary/assets/icons/logo-64.png /usr/share/icons/hicolor/64x64/apps/audiolibrary.png
cp ./src/audiolibrary/assets/icons/logo-128.png /usr/share/icons/hicolor/128x128/apps/audiolibrary.png
cp ./src/audiolibrary/assets/icons/logo-256.png /usr/share/icons/hicolor/256x256/apps/audiolibrary.png

# Install .desktop file
cp ./linux/.desktop /usr/share/applications/audiolibrary.desktop
update-desktop-database /usr/share/applications

# Install app
echo 'Установка приложения...'

INSTALL_PATH=/opt/audiolibrary

cp -r ./src $INSTALL_PATH/

# Create config file
getent passwd | while IFS=: read -r username _ uid _ _ home _; do
  if [ "$uid" -ge 1000 ] && [ -d "$home" ]; then
    mkdir -p "$home/.audiolibrary"
    cp ./config.ini "$home/.audiolibrary/config.ini"
    chown "$username":"$username" "$home/.audiolibrary/config.ini"
  fi
done

# Create uninstall script
cp ./uninstall.sh $INSTALL_PATH/
chmod +x $INSTALL_PATH/uninstall.sh

# Make executable
cp ./audiolibrary.sh $INSTALL_PATH/
chmod +x $INSTALL_PATH/audiolibrary.sh
ln -sf $INSTALL_PATH/audiolibrary.sh /usr/local/bin/audiolibrary
chmod +x /usr/local/bin/audiolibrary

# Install dependencies for app
python3.12 -m venv $INSTALL_PATH/venv
. $INSTALL_PATH/venv/bin/activate
pip install -e .

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

echo 'Установка успешно завершена.'
echo 'Приложение было установлено в ' $INSTALL_PATH
echo 'Вы можете удалить приложение выполнив: ' $INSTALL_PATH'/uninstall.sh'
