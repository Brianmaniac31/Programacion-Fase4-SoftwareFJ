# Sistema Integral de Gestión - Software FJ
**Curso:** Programación (213023) - UNAD  
**Actividad:** Fase 4 - Componente Práctico  
**Estudiante:** Bryan Duarte Orduz  

## Descripción del Proyecto
Sistema desarrollado en Python para gestionar clientes, servicios (reservas de salas, alquiler de equipos y asesorías especializadas) y reservas sin bases de datos. Implementa clases abstractas, herencia, polimorfismo, encapsulación, manejo avanzado de excepciones y registro de eventos en archivo de logs.

## Estructura del Proyecto
- `excepciones.py`: Jerarquía de excepciones personalizadas.
- `modelos.py`: Clases abstractas y concretas (`Cliente`, `Servicio`, `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`, `Reserva`).
- `gestor.py`: Lógica de control en memoria (listas) y manejo del archivo de logs (`sistema_fj.log`).
- `main.py`: Simulación ejecutable con al menos 10 operaciones (casos exitosos y manejo de errores).
