"""
Módulo controlador del sistema Software FJ.
Gestiona los datos en memoria y el registro de eventos y errores en archivo de logs,
implementando bloques try, except, else, finally para garantizar la estabilidad del sistema.
"""

import logging
from typing import List, Optional
from modelos import Cliente, Servicio, Reserva
from excepciones import ErrorSistemaFJ, OperacionNoPermitidaError


class GestorSoftwareFJ:
    """Controlador central que administra clientes, servicios, reservas y logs del sistema."""

    def __init__(self, archivo_log: str = "sistema_fj.log"):
        # Almacenamiento en memoria mediante listas
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []
        self._archivo_log = archivo_log
        self._configurar_logger()

    def _configurar_logger(self):
        """Configura el registro de eventos y errores hacia archivo y consola."""
        self._logger = logging.getLogger("SoftwareFJ")
        self._logger.setLevel(logging.INFO)
        # Evita duplicar manejadores si se llama varias veces al constructor
        if not self._logger.handlers:
            formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            manejador_archivo = logging.FileHandler(self._archivo_log, encoding="utf-8")
            manejador_archivo.setFormatter(formato)
            self._logger.addHandler(manejador_archivo)

    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Agrega un cliente validado a la lista interna usando try/except/else/finally."""

        # Bloque try para controlar errores de negocio
        try:
            if any(c.id_entidad == cliente.id_entidad for c in self._clientes):
                raise OperacionNoPermitidaError(f"Ya existe un cliente registrado con el ID '{cliente.id_entidad}'.")
        except ErrorSistemaFJ as e:
            self._logger.error(f"Error al registrar cliente: {e}")
            print(f"[ERROR CONTROLADO] {e}")
            return False
        else:
            # Solo se ejecuta si el bloque try no lanzó ninguna excepción
            self._clientes.append(cliente)
            mensaje = f"Cliente registrado exitosamente -> {cliente.obtener_resumen()}"
            self._logger.info(mensaje)
            print(f"[OK] {mensaje}")
            return True
        finally:
            # Se ejecuta siempre para dejar trazabilidad
            self._logger.info("Auditoría: Finalizó intento de registro de cliente.")

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Agrega un servicio validado al catálogo en memoria."""

        # Bloque try para controlar errores de negocio
        try:
            if any(s.id_entidad == servicio.id_entidad for s in self._servicios):
                raise OperacionNoPermitidaError(f"Ya existe un servicio registrado con el ID '{servicio.id_entidad}'.")
        except ErrorSistemaFJ as e:
            self._logger.error(f"Error al registrar servicio: {e}")
            print(f"[ERROR CONTROLADO] {e}")
            return False
        else:
            self._servicios.append(servicio)
            mensaje = f"Servicio registrado exitosamente -> {servicio.obtener_resumen()}"
            self._logger.info(mensaje)
            print(f"[OK] {mensaje}")
            return True
        finally:
            self._logger.info("Auditoría: Finalizó intento de registro de servicio.")

    # Bloque para crear y confirmar reservas
    def crear_y_confirmar_reserva(
        self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int,
        descuento: float = 0.0, impuesto: float = 0.19
    ) -> Optional[Reserva]:
        """Crea una reserva, la procesa y la confirma controlando cualquier falla."""
        nueva_reserva = None

        # Bloque try para controlar errores inesperados
        try:
            if any(r.id_entidad == id_reserva for r in self._reservas):
                raise OperacionNoPermitidaError(f"El código de reserva '{id_reserva}' ya existe.")
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion_horas)
            nueva_reserva.procesar_y_confirmar(descuento=descuento, impuesto=impuesto)
        except ErrorSistemaFJ as e:
            # Captura errores de negocio y su causa en caso de existir
            causa = f" (Causa original: {e.__cause__})" if e.__cause__ else ""
            self._logger.error(f"Fallo en reserva [{id_reserva}]: {e}{causa}")
            print(f"[ERROR CONTROLADO] Reserva [{id_reserva}]: {e}{causa}")
            return None
        except Exception as e_inesperado:
            self._logger.critical(f"Error inesperado en reserva [{id_reserva}]: {e_inesperado}")
            print(f"[ERROR CRÍTICO CONTROLADO] {e_inesperado}")
            return None
        else:
            self._reservas.append(nueva_reserva)
            mensaje = f"Reserva confirmada -> {nueva_reserva.obtener_resumen()}"
            self._logger.info(mensaje)
            print(f"[OK] {mensaje}")
            return nueva_reserva
        finally:
            self._logger.info(f"Auditoría: Cierre de transacción para reserva '{id_reserva}'.")

    # Bloque para cancelar reservas
    def cancelar_reserva(self, reserva: Optional[Reserva]) -> bool:
        """Cancela una reserva existente de forma segura."""
        try:
            if reserva is None:
                raise OperacionNoPermitidaError("No se puede cancelar una reserva inexistente (None).")
            reserva.cancelar()
        except ErrorSistemaFJ as e:
            self._logger.error(f"Error al cancelar reserva: {e}")
            print(f"[ERROR CONTROLADO] {e}")
            return False
        else:
            mensaje = f"Reserva cancelada -> {reserva.obtener_resumen()}"
            self._logger.info(mensaje)
            print(f"[OK] {mensaje}")
            return True
        finally:
            self._logger.info("Auditoría: Finalizó intento de cancelación de reserva.")

    # Bloque para mostrar reportes
    def mostrar_reporte_general(self):
        """Imprime en consola el estado actual de todas las listas en memoria."""
        print("\n" + "=" * 65)
        print("REPORTE FINAL EN MEMORIA - SOFTWARE FJ")
        print("=" * 65)
        print(f"Total Clientes registrados : {len(self._clientes)}")
        for c in self._clientes:
            print(f"  - {c.obtener_resumen()}")

        print(f"\nTotal Servicios registrados: {len(self._servicios)}")
        for s in self._servicios:
            print(f"  - {s.obtener_resumen()}")

        print(f"\nTotal Reservas registradas : {len(self._reservas)}")
        for r in self._reservas:
            print(f"  - {r.obtener_resumen()}")
        print("=" * 65 + "\n")