# sistemas-multiagentes

Este proyecto fue realizado por el equipo 3, cuyos integrantes son:
Jorge Daniel Cruz Case - A01634536
Alejandro Hidalgo Badillo - A01423412
Alejandro León Carmona - A01568537

# Descripción

El reto es hacer una simulación de tráfico usando un sistema multiagentes. Los agentes (vehículos) deberán crucar una intersección, haciendo caso a las indicaciones de los semáforos.

El archivo de Interseccion.py genera los agentes y el modelo de la simulación y lo corre, generando los resultados en archivos de texto que se van a pasar a un script en Unity. Este se debe correr antes de correr el script de Unity para que se puedan pasar los valores a la animación.

AgentSP.cs es el script de Unity que va a recibir los archivos de texto y los va a pasar a objetos que se generan en el mismo script para que estos representen el movimiento de los agentes en la simulación.

Simul_completa.unitypackage es todo lo que hay dentro de la simulación en Unity (versión 2020 en adelante). Para que todos los modelos se puedan generar bien, es necesario tener instalado ProBuilder para Unity. En este paquete también se encuentran los mismos códigos anteriores.