"""
Módulo principal de ejecución del Software FJ.
Ejecuta un conjunto de 12 operaciones completas sobre clientes,
servicios y reservas, demostrando la estabilidad del programa ante errores controlados.
"""

from excepciones import ErrorSistemaFJ
from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSoftwareFJ


# Función auxiliar para registrar intentos de creación de entidades con control de errores
def crear_cliente_seguro(gestor: GestorSoftwareFJ, id_c: str, nombre: str, correo: str, tel: str):
    """Intenta instanciar y registrar un Cliente capturando errores de validación."""
    try:
        cliente = Cliente(id_c, nombre, correo, tel)
        gestor.registrar_cliente(cliente)
        return cliente
    except ErrorSistemaFJ as e:
        # Registra el fallo en el log del gestor sin detener el flujo principal
        gestor._logger.error(f"Error al crear cliente [{id_c}]: {e}")
        print(f"[ERROR CONTROLADO] Creación de cliente [{id_c}]: {e}")
        return None


# Función auxiliar para registrar intentos de creación de servicios con control de errores
def crear_servicio_seguro(gestor: GestorSoftwareFJ, constructor, *args):
    """Intenta instanciar y registrar un Servicio capturando parámetros inválidos."""
    try:
        servicio = constructor(*args)
        gestor.registrar_servicio(servicio)
        return servicio
    except ErrorSistemaFJ as e:
        gestor._logger.error(f"Error al crear servicio {args}: {e}")
        print(f"[ERROR CONTROLADO] Creación de servicio: {e}")
        return None


# Función principal que ejecuta la simulación completa de operaciones sobre el sistema
def ejecutar_simulacion():
    """Simula escenarios reales y fallos críticos para validar la robustez del sistema."""
    print("=================================================================")
    print("INICIANDO SIMULACIÓN INTEGRAL - SOFTWARE FJ (SIN BASE DE DATOS)")
    print("=================================================================\n")

    # Instancia el controlador central y crea/abre el archivo de logs
    gestor = GestorSoftwareFJ("sistema_fj.log")

    # BLOQUE 1: REGISTRO DE CLIENTES
    print("--- 1. GESTIÓN DE CLIENTES ---")
    # Operación 1: Registro exitoso de cliente 1
    cliente_1 = crear_cliente_seguro(gestor, "C-001", "Laura Gómez", "laura.gomez@empresa.com", "3104567890")
    # Operación 2: Registro exitoso de cliente 2
    cliente_2 = crear_cliente_seguro(gestor, "C-002", "Carlos Mendoza", "cmendoza@tech.co", "3209876543")
    # Operación 3: Error controlado por correo inválido
    crear_cliente_seguro(gestor, "C-003", "Andrés Ruiz", "andres.ruiz.sin.arroba", "3001112233")
    # Operación 4: Error controlado por parámetro faltante
    crear_cliente_seguro(gestor, "C-004", "   ", "valido@correo.com", "3152223344")

    # BLOQUE 2: REGISTRO DE SERVICIOS
    print("\n--- 2. GESTIÓN DE SERVICIOS ---")
    # Operación 5: Creación exitosa de Sala de Juntas
    sala_1 = crear_servicio_seguro(gestor, ReservaSala, "S-101", "Sala Ejecutiva Norte", 80000, 12)
    # Operación 6: Creación exitosa de Alquiler de Equipo
    equipo_1 = crear_servicio_seguro(gestor, AlquilerEquipo, "E-201", "Servidor Portátil Dell Precision", 45000, "SN-998877")
    # Operación 7: Creación exitosa de Asesoría Especializada
    asesoria_1 = crear_servicio_seguro(gestor, AsesoriaEspecializada, "A-301", "Arquitectura Cloud y Seguridad", 120000, "Ciberseguridad")
    # Operación 8: Error controlado por tarifa base negativa en creación de servicio
    crear_servicio_seguro(gestor, ReservaSala, "S-999", "Sala Defectuosa", -50000, 5)

    # BLOQUE 3: RESERVAS, CÁLCULOS SOBRECARGADOS Y CONTROL DE ERRORES
    print("\n--- 3. GESTIÓN DE RESERVAS Y EXCEPCIONES ---")
    # Operación 9: Reserva exitosa de Sala
    reserva_1 = gestor.crear_y_confirmar_reserva("R-001", cliente_1, sala_1, duracion_horas=3)

    # Operación 10: Error controlado por intentar reservar una sala que ya está ocupada
    gestor.crear_y_confirmar_reserva("R-002", cliente_2, sala_1, duracion_horas=2)

    # Operación 11: Reserva exitosa de Asesoría
    reserva_2 = gestor.crear_y_confirmar_reserva("R-003", cliente_2, asesoria_1, duracion_horas=6, descuento=0.10)

    # Operación 12: Error encadenado por descuento fuera de rango en alquiler de equipo
    gestor.crear_y_confirmar_reserva("R-004", cliente_1, equipo_1, duracion_horas=4, descuento=1.5)

    # BLOQUE 4: CANCELACIÓN Y LIBERACIÓN DE RECURSOS

    print("\n--- 4. CANCELACIÓN Y REUTILIZACIÓN ---")
    # Cancela la reserva 1 para liberar la Sala Ejecutiva Norte
    gestor.cancelar_reserva(reserva_1)
    # Intento de cancelar nuevamente la misma reserva
    gestor.cancelar_reserva(reserva_1)
    # Ahora que la sala quedó libre, el cliente 2 sí puede reservarla exitosamente
    gestor.crear_y_confirmar_reserva("R-005", cliente_2, sala_1, duracion_horas=2, descuento=0.05)

    # Muestra el resumen final en consola comprobando que el programa terminó sin caídas
    gestor.mostrar_reporte_general()
    print("Simulación finalizada con éxito. Los datos se han registrado en el archivo 'sistema_fj.log'. Allí se puede ver la auditoría completa.")


if __name__ == "__main__":
    ejecutar_simulacion()