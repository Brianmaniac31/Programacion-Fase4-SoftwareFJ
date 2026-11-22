"""
Módulo de modelos principales para Software FJ.
Define las clases abstractas y concretas del sistema: EntidadSistema, Cliente,
Servicio y Reserva.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


# Clase abstracta base para todas las entidades del sistema
class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad general del sistema."""

    # Inicializador de la clase EntidadSistema con validación de identificador
    def __init__(self, id_entidad: str):
        # Valida que el identificador no llegue vacío antes de asignarlo
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        # Atributo protegido para almacenar el identificador único
        self._id_entidad = str(id_entidad).strip()
        self._fecha_creacion = datetime.now()

    # Propiedad para acceder al identificador de la entidad
    @property
    def id_entidad(self) -> str:
        """Devuelve el identificador de la entidad."""
        return self._id_entidad

    # Método abstracto que obliga a las clases hijas a implementar su descripción
    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las clases hijas a describirse."""
        pass


# Clase concreta que representa un cliente del sistema
class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación de datos personales."""

    # Inicializador de la clase Cliente
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        # Se asignan a través de los setters para aplicar validaciones y limpieza de datos
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # Propiedades para acceder y modificar los atributos del cliente con validación
    @property
    def nombre(self) -> str:
        return self._nombre

    # Setter para el nombre del cliente, validando longitud mínima y eliminando espacios
    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        if len(valor.strip()) < 3:
            raise DatosInvalidosError(f"El nombre '{valor}' es demasiado corto (mínimo 3 caracteres).")
        self._nombre = valor.strip()

    # Propiedad para acceder al correo electrónico del cliente
    @property
    def correo(self) -> str:
        return self._correo

    # Setter para el correo del cliente, verificando formato válido con arroba y dominio
    @correo.setter
    def correo(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor.strip().lower()

    # Propiedad para acceder al teléfono del cliente
    @property
    def telefono(self) -> str:
        return self._telefono

    # Setter para el teléfono del cliente, exigiendo mínimo 7 dígitos numéricos
    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatosInvalidosError(f"El teléfono '{valor}' debe contener al menos 7 dígitos numéricos.")
        self._telefono = limpio

    # Implementación del método abstracto para obtener un resumen del cliente
    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen para un Cliente."""
        return f"Cliente [{self.id_entidad}]: {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"


# Clase abstracta base para todos los servicios del sistema
class Servicio(EntidadSistema, ABC):
    """Clase abstracta base para todos los servicios que ofrece Software FJ."""

    # Inicializador de la clase Servicio con validación de nombre y tarifa positiva
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        super().__init__(id_servicio)
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError(f"La tarifa base ({tarifa_base}) debe ser un número mayor a cero.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True  # Controla si el servicio puede reservarse

    # Propiedad para acceder al nombre del servicio
    @property
    def nombre(self) -> str:
        return self._nombre

    # Propiedad para acceder a la tarifa base del servicio
    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    # Propiedad para consultar la disponibilidad del servicio
    @property
    def disponible(self) -> bool:
        return self._disponible

    # Setter para modificar el estado de disponibilidad validando tipo booleano
    @disponible.setter
    def disponible(self, estado: bool):
        if not isinstance(estado, bool):
            raise DatosInvalidosError("El estado de disponibilidad debe ser booleano (True/False).")
        self._disponible = estado

    # Método protegido que aplica descuentos, impuestos y encadena excepciones matemáticas
    def _aplicar_impuestos_y_descuentos(self, subtotal: float, descuento: float, impuesto: float) -> float:
        """Valida porcentajes y calcula el total final con encadenamiento de excepciones."""
        try:
            # Verifica que los porcentajes estén dentro de rangos lógicos
            if not (0.0 <= descuento < 1.0):
                raise ValueError(f"Descuento fuera de rango (0.0 a 0.99): {descuento}")
            if impuesto < 0.0:
                raise ValueError(f"El impuesto no puede ser negativo: {impuesto}")
            total = (subtotal * (1 - descuento)) * (1 + impuesto)
            if total <= 0:
                raise ValueError("El total calculado resultó menor o igual a cero.")
            return round(total, 2)
        except (TypeError, ValueError) as error_original:
            # Encadena el error técnico original dentro de la excepción personalizada del negocio
            raise CalculoInconsistenteError(
                f"Inconsistencia matemática al calcular el costo del servicio '{self.nombre}'."
            ) from error_original

    # Método abstracto para calcular el costo final del servicio
    @abstractmethod
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Método abstracto y sobrecargado mediante parámetros opcionales.
        Permite calcular el costo solo con horas, o añadiendo descuentos e impuestos.
        """
        pass

    # Método abstracto para validar parámetros específicos del servicio
    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> None:
        """Valida las reglas específicas de cada tipo de servicio."""
        pass


# Implementación de servicio concreto para salas que hereda de Servicio
class ReservaSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o capacitación."""

    # Inicializador de la clase ReservaSala con validación de aforo positivo
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad_personas: int):
        super().__init__(id_servicio, nombre, tarifa_base)
        if not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero mayor a cero.")
        self._capacidad_personas = capacidad_personas

    # Implementación del método abstracto para validar parámetros específicos de la sala
    def validar_parametros(self, duracion_horas: int) -> None:
        # Las salas requieren mínimo 1 hora entera para ser reservadas
        if not isinstance(duracion_horas, int) or duracion_horas < 1:
            raise DatosInvalidosError("La reserva de sala requiere una duración mínima de 1 hora entera.")

    # Implementación del método abstracto para calcular el costo de la sala
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula costo por hora más un recargo fijo de limpieza ($15.000)."""
        self.validar_parametros(duracion_horas)
        subtotal = (self._tarifa_base * duracion_horas) + 15000
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    # Implementación del método abstracto para obtener un resumen de la sala
    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Sala [{self.id_entidad}]: {self.nombre} (Capacidad: {self._capacidad_personas} pers.) - {estado}"


# Implementación de servicio concreto para equipos que hereda de Servicio
class AlquilerEquipo(Servicio):
    """Servicio especializado para el préstamo/alquiler de equipos tecnológicos."""

    # Inicializador de la clase AlquilerEquipo con validación de número de serial
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, serial_equipo: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        if not serial_equipo or not str(serial_equipo).strip():
            raise ParametroFaltanteError("El serial del equipo es obligatorio para su registro.")
        self._serial_equipo = serial_equipo.strip()

    # Implementación del método abstracto para validar parámetros específicos del equipo
    def validar_parametros(self, duracion_horas: int) -> None:
        # Los equipos se alquilan en bloques mínimos de 2 horas
        if not isinstance(duracion_horas, int) or duracion_horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un mínimo de 2 horas.")

    # Implementación del método abstracto para calcular el costo del alquiler de equipo
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula costo por hora más un seguro tecnológico del 5% sobre la tarifa base."""
        self.validar_parametros(duracion_horas)
        seguro = self._tarifa_base * 0.05
        subtotal = (self._tarifa_base * duracion_horas) + seguro
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    # Implementación del método abstracto para obtener un resumen del equipo
    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Alquilado"
        return f"Equipo [{self.id_entidad}]: {self.nombre} (Serial: {self._serial_equipo}) - {estado}"


# Implementación de servicio concreto para asesorías que hereda de Servicio
class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría técnica con ingenieros de Software FJ."""

    # Inicializador de la clase AsesoriaEspecializada con validación de especialidad
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        if not especialidad or not str(especialidad).strip():
            raise ParametroFaltanteError("Debe especificarse el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    # Implementación del método abstracto para validar parámetros específicos de la asesoría
    def validar_parametros(self, duracion_horas: int) -> None:
        # Las asesorías tienen un rango permitido de 1 a 8 horas por sesión
        if not isinstance(duracion_horas, int) or not (1 <= duracion_horas <= 8):
            raise DatosInvalidosError("La asesoría especializada debe durar entre 1 y 8 horas.")

    # Implementación del método abstracto para calcular el costo de la asesoría
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula costo por hora; si supera 4 horas aplica un bono de eficiencia del 10%."""
        self.validar_parametros(duracion_horas)
        subtotal = self._tarifa_base * duracion_horas
        if duracion_horas > 4:
            subtotal *= 0.90  # 10% de descuento automático por sesión larga
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    # Implementación del método abstracto para obtener un resumen de la asesoría
    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Asignada"
        return f"Asesoría [{self.id_entidad}]: {self.nombre} (Área: {self._especialidad}) - {estado}"


# Implementación de la clase Reserva que integra Cliente y Servicio
class Reserva(EntidadSistema):
    """Integra un Cliente y un Servicio, gestionando el ciclo de vida de la reserva."""

    # Inicializador de la clase Reserva con validación de instancias y duración
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere una instancia válida de Cliente para reservar.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere una instancia válida de Servicio para reservar.")
        # Valida la duración desde la creación según las reglas del servicio elegido
        servicio.validar_parametros(duracion_horas)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "PENDIENTE"  # Estados posibles: PENDIENTE, CONFIRMADA, CANCELADA
        self._costo_total = 0.0

    # Propiedad para acceder al estado actual de la reserva
    @property
    def estado(self) -> str:
        return self._estado

    # Propiedad para acceder al costo total calculado de la reserva
    @property
    def costo_total(self) -> float:
        return self._costo_total

    # Método para calcular costo, bloquear el servicio y confirmar la reserva
    def procesar_y_confirmar(self, descuento: float = 0.0, impuesto: float = 0.19):
        """Calcula el costo final, marca el servicio como ocupado y confirma la reserva."""
        if self._estado == "CONFIRMADA":
            raise OperacionNoPermitidaError(f"La reserva {self.id_entidad} ya se encuentra confirmada.")
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"No se puede confirmar la reserva {self.id_entidad} porque fue cancelada.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' ({self._servicio.id_entidad}) no está disponible."
            )

        self._costo_total = self._servicio.calcular_costo(
            self._duracion_horas, descuento=descuento, impuesto=impuesto
        )
        self._servicio.disponible = False
        self._estado = "CONFIRMADA"

    # Método para cancelar la reserva y liberar nuevamente el servicio
    def cancelar(self):
        """Cancela la reserva y libera nuevamente el servicio."""
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva {self.id_entidad} ya fue cancelada previamente.")
        if self._estado == "CONFIRMADA":
            self._servicio.disponible = True
        self._estado = "CANCELADA"

    # Implementación del método abstracto para obtener un resumen de la reserva
    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion_horas}h | Total: ${self._costo_total:,.2f}"
        )