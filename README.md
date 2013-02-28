Monti

Monti: Aplicacion escrita en python ayudado de la libreria wxpython. 
Su principal funcionalidad es montar imagenes iso en medios extraibles (usb, sd), ayudados del comando dd. 
En un principio fue pensada para montar la imagen iso de para Raspberry en una memoria SD asi que funciona perfectamente con los archivos iso disponibles en la web de raspberry.
Una vez avanzado en el desarrollo de la aplicación incluí soporte para otro tipo de medio extraible no necesariamente tarjetas SD.

Precaución:
Verificar muy bien el lugar donde esta montado su medio extraible, a manera de protección omite el punto de montaje /dev/sda debido a que normalmente en este esta montado el SO principal.

Modo de uso:

