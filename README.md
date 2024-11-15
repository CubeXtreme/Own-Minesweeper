# Own-Minesweeper
Just a chill project for a minesweeper, I'm bored

**Historial de Desarrollo del Proyecto Buscaminas en Python**

Durante el desarrollo del juego Buscaminas en Python utilizando Pygame, hemos enfrentado y resuelto una serie de desafíos que han mejorado significativamente la funcionalidad y la experiencia del juego. A continuación, se detalla el progreso y las soluciones implementadas hasta el momento:

1. **Inicio del Proyecto y Configuración Inicial:**
   - Comenzamos creando las estructuras básicas del juego, incluyendo las clases `Board` y `Cell` en `game.py`, que gestionan la lógica del tablero y las celdas respectivamente.
   - En `main.py`, configuramos la ventana del juego, cargamos recursos como imágenes, sonidos y fuentes, y establecimos los niveles de dificultad (Fácil, Medio, Difícil).

2. **Problemas Iniciales con el Tamaño del Tablero:**
   - Al implementar diferentes niveles de dificultad, surgió un problema donde las variables relacionadas con el tamaño del tablero (`COLS`, `ROWS`, `WIDTH`, `HEIGHT`) no estaban correctamente sincronizadas.
   - Esto causaba que el tablero se volviera "infinito" y que el juego se bloquease al intentar reiniciarlo.
   - **Solución Implementada:** Reubicamos la configuración del tamaño del tablero para que dependiera de la dificultad seleccionada por el usuario. Además, aseguramos que la pantalla (`screen`) se configurara dinámicamente según las dimensiones del tablero seleccionado.

3. **Definición de `CELL_SIZE` y Parpadeo de la Pantalla:**
   - Se identificó que la variable `CELL_SIZE` no estaba definida globalmente, lo que impedía su uso en diferentes partes del código.
   - Además, al iniciar el juego, la pantalla experimentaba un parpadeo intenso.
   - **Soluciones Implementadas:**
     - Definimos `CELL_SIZE` de manera global para garantizar su accesibilidad en todo el proyecto.
     - Optimizamos el bucle principal de Pygame eliminando llamadas repetidas a `pygame.display.set_mode()`, lo que eliminó el parpadeo.
     - Implementamos un enfoque basado en tiempo para manejar las animaciones, evitando el uso de retardos que bloqueaban el bucle principal.

4. **Problemas con la Imagen de Fondo y la Revelación de Celdas:**
   - Al iniciar el juego, la imagen de fondo no se mostraba correctamente y solo aparecía después de seleccionar una dificultad.
   - La función diseñada para revelar automáticamente las celdas adyacentes sin minas o números no funcionaba como se esperaba, obligando al jugador a abrir cada celda manualmente.
   - **Soluciones Implementadas:**
     - Ajustamos la función de menú de selección de dificultad para que no sobrescribiera la imagen de fondo, asegurando que ésta se mantuviera visible desde el inicio.
     - Mejoramos la lógica de revelación de celdas adyacentes, permitiendo que todas las celdas sin minas o números se revelaran automáticamente de manera fluida y sin bloquear el bucle principal.
     - Implementamos una lista de celdas en proceso de animación (`animation_cells`) para gestionar las animaciones de revelación de manera eficiente y no bloqueante.

5. **Optimización de Animaciones y Experiencia de Usuario:**
   - Refinamos las animaciones para que fueran más suaves y estéticamente agradables, eliminando cualquier efecto de parpadeo residual.
   - Aseguramos que todas las interacciones del usuario, como reiniciar el juego o seleccionar una dificultad, funcionaran de manera coherente y sin errores.
   - Mejoramos la gestión de recursos, garantizando que todas las imágenes, sonidos y fuentes se cargaran correctamente y se escalaran según las dimensiones del tablero.

6. **Estado Actual del Proyecto:**
   - El juego Buscaminas ahora funciona correctamente, permitiendo a los jugadores seleccionar diferentes niveles de dificultad, interactuar con el tablero sin inconvenientes y disfrutar de animaciones fluidas al revelar celdas.
   - La imagen de fondo se muestra correctamente desde el inicio, y las celdas adyacentes se revelan automáticamente cuando no hay minas o números cercanos.
   - Se ha optimizado la experiencia del usuario eliminando parpadeos innecesarios y asegurando que todas las funcionalidades operen de manera eficiente.

**Conclusión:**

A través de una serie de ajustes y optimizaciones, hemos logrado superar los desafíos iniciales del proyecto Buscaminas en Python. El juego ahora ofrece una experiencia de usuario más fluida y agradable, con una interfaz gráfica coherente y funcionalidades robustas. Continuaremos monitoreando el desempeño y realizando mejoras adicionales para asegurar que el juego mantenga altos estándares de calidad.

## Nuevas Funcionalidades

### **Volver al Menú Principal**

Se ha añadido un nuevo botón **"Menú Principal"** en la interfaz del juego, que permite a los jugadores regresar al menú de selección de dificultad en cualquier momento durante una partida en curso.

**Características:**

- **Botón de "Menú Principal":** Posicionado en la parte inferior central de la pantalla de juego.
- **Funcionalidad:** Al hacer clic en el botón, el juego se reinicia y se muestra el menú de selección de dificultad.
- **Integración:** Fácil de usar y no interfiere con las otras funcionalidades del juego.

#### Added
- **Hotfix HF001:** Soluciona el problema de carga del icono de la ventana cambiando el formato de `.ico` de `256x256` a `32x32` píxeles para asegurar compatibilidad con Pygame.