# SMS Catcher

# Despliegue del Proyecto de Raspberry Pi

Este documento proporciona una guía completa sobre cómo instalar y operar el proyecto en una Raspberry Pi.

## Instalación de la Imagen

### Requisitos

Para llevar a cabo este proceso, se necesitan los siguientes elementos:
- Una computadora con lector de tarjetas SD.
- Tarjeta SD para utilizar en una Raspberry Pi.
- La imagen de Raspberry Pi descargada.
- Software para escribir la imagen en la tarjeta SD.

### Descargar la Imagen

Primero, es necesario descargar la imagen de la Raspberry Pi desde [hackerlab.cl](https://hackerlab.cl/proyectos/bee-sms/).

### Escribir la Imagen a la Tarjeta SD

A continuación, se detallan los pasos para escribir la imagen a la tarjeta SD en diferentes sistemas operativos. Para este proceso, es necesario reemplazar `/path/to/imagen_raspberry_pi.img` y `/dev/sdX` con la ruta correcta de la imagen y el nombre del dispositivo.

#### En Windows

1. Inserta la tarjeta SD en el lector de tarjetas de la computadora.
2. Descarga e instala [Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/).
3. Abre Win32 Disk Imager.
4. Selecciona la unidad correspondiente a la tarjeta SD.
5. Selecciona la imagen descargada haciendo clic en el ícono de la carpeta y buscando el archivo `imagen_raspberry_pi.img`.
6. Haz clic en `Write` para escribir la imagen en la tarjeta SD.

#### En macOS

1. Inserta la tarjeta SD en el lector de tarjetas de la computadora.
2. Abre la Terminal.
3. Encuentra el nombre del dispositivo de la tarjeta SD ejecutando el siguiente comando:
    ```bash
    diskutil list
    ```
4. Desmonta la tarjeta SD ejecutando:
    ```bash
    diskutil unmountDisk /dev/diskX
    ```
    donde `/dev/diskX` es el nombre del dispositivo de la tarjeta SD.
5. Escribe la imagen a la tarjeta SD utilizando `dd`:
    ```bash
    sudo dd if=/path/to/imagen_raspberry_pi.img of=/dev/rdiskX bs=1m
    ```

#### En Linux

1. Inserta la tarjeta SD en el lector de tarjetas de la computadora.
2. Abre una terminal.
3. Encuentra el nombre del dispositivo de la tarjeta SD ejecutando:
    ```bash
    lsblk
    ```
4. Desmonta la tarjeta SD ejecutando:
    ```bash
    sudo umount /dev/sdX*
    ```
    donde `/dev/sdX` es el nombre del dispositivo de la tarjeta SD.
5. Escribe la imagen a la tarjeta SD utilizando `dd`:
    ```bash
    sudo dd if=/path/to/imagen_raspberry_pi.img of=/dev/sdX bs=1M
    ```

## Operación del Sistema

### Activación de Cronjobs

Es necesario activar cron para monitorear la llegada de nuevos mensajes. Para eso, se debe ejecutar el siguiente comando:
```bash
sudo service cron start
```

Para dejar de obtener nuevos mensajes, utiliza el siguiente comando:
```bash
sudo service cron stop
```

##  Creación de .env

Dentro de la carpeta /sms-catcher/backend, modifica un archivo de nombre .config ubicado en la dirección boot/.config, en el cual debes guardar la dirección de la API receptora de mensajes de la siguiente forma y opcionalmente un API TOKEN. Los datos en este archivo posteriormente serán copiados y utilizados como variables de entorno para la ejecución.
```bash
POST_API_URL = "my_api_url"
API_TOKEN = "my_api_token"
```

Donde my_api_url debe reemplazarse por la dirección de la API.

## Ejecución del Sistema

El sistema comienza a operar de manera autónoma al realizar un reinicio con:
```bash
sudo reboot
```

Para desplegar el frontend:
```bash
cd sms-catcher/frontend/sms-catcher
serve -s build -l 3000
```




