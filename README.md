#Abstrac
Aplication developed in python the function is to burn iso images into external device storage, for example it works perfectly with Raspbian and others SO available for Raspberry, works to with any iso file and any device.

#Monti: 
Aplicación escrita en python con la ayudado de la librería wxpython para crear una interfaz de usuario. Su principal función es montar imágenes iso en medios extraíbles (usb, sd), ayudados del comando dd. En un principio empecé a desarrollarla con el único fin de utilizarla con memorias SD para montar Raspbian dentro de mi Raspberry, durante el desarrollo de la aplicación quise crearla para propósitos más generales. Puede ser usada perfectamente para grabar SO desarrollados para Raspberry pi.

#Precaución:
Verificar bien el lugar donde esta montado su medio extraíble; como protección omití el punto de montaje /dev/sda debido a que normalmente en este esta montado el SO principal de los equipos.

#Dependencias:
La única dependencia es la biblioteca wxpython.

#Instalación de dependencias Debian/Ubuntu
	apt-get install python-wxgtk2.8 python-wxtools

#Modo de uso:
Antes de ejecutar la aplicación es recomendable tener formateado el dispositivo de almacenamiento para evitar cualquier problema, después de tener nuestro dispositivo formateado ejecutamos la aplicación.

	python monti.py

Una vez ejecutada la aplicación siga los sencillos 5 pasos para grabar la imagen, el grabado de los datos tarda un poco(aprox. 3min), cuando presione el botón Quemar notara que se quedara con el efecto presionado, cuando termine el proceso de copiado empezara a correr una barra para verificar el correcto copiado de los archivos cuando la etiqueta Correcto aparece en la ventana ya puede cerrar la aplicación.

#Corriendo
![](https://dl.dropbox.com/u/12001689/montirun.png)
