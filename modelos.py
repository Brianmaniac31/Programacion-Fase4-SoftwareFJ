"""
Módulo de modelos principales para Software FJ.
Define las clases abstractas y concretas del sistema: EntidadSistema, Cliente,
Servicio y Reserva.
"""

from abc import ABC, abstractmethod
from datetime import datetime

# Clase abstracta base para todas las entidades del sistema
class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad general del sistema."""

    # Inicializador de la clase EntidadSistema
    def __init__(self, id_entidad: str):
        # Atributo protegido para almacenar el identificador único
        self._id_entidad = id_entidad
        self._fecha_creacion = datetime.now()

    # Propiedad para acceder al identificador de la entidad
    @property
    def id_entidad(self) -> str:
        """Devuelve el identificador de la entidad."""
        return self._id_entidad

    # Propiedad para acceder a la fecha de creación de la entidad
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

    # Setter para el nombre del cliente, eliminando espacios no deseados
    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = valor.strip()

    # Propiedades para correo y teléfono con validación y limpieza de datos
    @property
    def correo(self) -> str:
        return self._correo

    # Setter para el correo del cliente, eliminando espacios no deseados
    @correo.setter
    def correo(self, valor: str):
        self._correo = valor.strip()

    # Propiedades para el teléfono del cliente con validación y limpieza de datos
    @property
    def telefono(self) -> str:
        return self._telefono

    # Setter para el teléfono del cliente, eliminando espacios no deseados
    @telefono.setter
    def telefono(self, valor: str):
        self._telefono = valor.strip()

    # Implementación del método abstracto para obtener un resumen del cliente
    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen para un Cliente."""
        return f"Cliente [{self.id_entidad}]: {self.nombre} | Correo: {self.correo}"

# Clase abstracta base para todos los servicios del sistema
class Servicio(EntidadSistema, ABC):
    """Clase abstracta base para todos los servicios que ofrece Software FJ."""

    # Inicializador de la clase Servicio
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        super().__init__(id_servicio)
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = True  # Controla si el servicio puede reservarse

    # Propiedades para acceder a los atributos del servicio con encapsulación
    @property
    def nombre(self) -> str:
        return self._nombre

    # Setter para el nombre del servicio
    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    # Setter para la tarifa base del servicio
    @property
    def disponible(self) -> bool:
        return self._disponible

    # Setter para el estado de disponibilidad del servicio
    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = estado

    # Implementación del método abstracto para obtener un resumen del servicio
    @abstractmethod
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Método abstracto y sobrecargado mediante parámetros opcionales.
        Permite calcular el costo solo con horas, o añadiendo descuentos e impuestos.
        """
        pass

    # Implementación del método abstracto para validar parámetros específicos del servicio
    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> bool:
        """Valida las reglas específicas de cada tipo de servicio."""
        pass

# Implementación de servicios concretos que heredan de la clase abstracta Servicio
class ReservaSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o capacitación."""

    # Inicializador de la clase ReservaSala
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad_personas: int):
        super().__init__(id_servicio, nombre, tarifa_base)
        self._capacidad_personas = capacidad_personas

    # Implementación del método abstracto para validar parámetros específicos de la sala
    def validar_parametros(self, duracion_horas: int) -> bool:
        # Las salas requieren mínimo 1 hora y capacidad positiva
        return duracion_horas >= 1 and self._capacidad_personas > 0

    # Implementación del método abstracto para calcular el costo de la sala
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula costo por hora más un recargo fijo de limpieza ($15.000)."""
        subtotal = (self._tarifa_base * duracion_horas) + 15000
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    # Implementación del método abstracto para obtener un resumen de la sala
    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Sala [{self.id_entidad}]: {self.nombre} (Capacidad: {self._capacidad_personas} pers.) - {estado}"

# Implementación de servicios concretos que heredan de la clase abstracta Servicio
class AlquilerEquipo(Servicio):
    """Servicio especializado para el préstamo/alquiler de equipos tecnológicos."""

    # Inicializador de la clase AlquilerEquipo
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, serial_equipo: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        self._serial_equipo = serial_equipo

    # Implementación del método abstracto para validar parámetros específicos del equipo
    def validar_parametros(self, duracion_horas: int) -> bool:
        # Los equipos se alquilan en bloques mínimos de 2 horas
        return duracion_horas >= 2 and bool(self._serial_equipo.strip())
    
    # Implementación del método abstracto para calcular el costo del alquiler de equipo
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula costo por hora más un seguro tecnológico del 5% sobre la tarifa base."""
        seguro = self._tarifa_base * 0.05
        subtotal = (self._tarifa_base * duracion_horas) + seguro
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    # Implementación del método abstracto para obtener un resumen del equipo
    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Alquilado"
        return f"Equipo [{self.id_entidad}]: {self.nombre} (Serial: {self._serial_equipo}) - {estado}"

# Implementación de servicios concretos que heredan de la clase abstracta Servicio
class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría técnica con ingenieros de Software FJ."""

    # Inicializador de la clase AsesoriaEspecializada
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        self._especialidad = especialidad

    # Implementación del método abstracto para validar parámetros específicos de la asesoría
    def validar_parametros(self, duracion_horas: int) -> bool:
        # Las asesorías tienen un máximo de 8 horas por sesión
        return 1 <= duracion_horas <= 8 and bool(self._especialidad.strip())

    # Implementación del método abstracto para calcular el costo de la asesoría
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula costo por hora; si supera 4 horas aplica un bono de eficiencia del 10%."""
        subtotal = self._tarifa_base * duracion_horas
        if duracion_horas > 4:
            subtotal *= 0.90  # 10% de descuento automático por sesión larga
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    # Implementación del método abstracto para obtener un resumen de la asesoría
    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Asignada"
        return f"Asesoría [{self.id_entidad}]: {self.nombre} (Área: {self._especialidad}) - {estado}"

# Implementación de la clase Reserva que integra Cliente y Servicio
class Reserva(EntidadSistema):
    """Integra un Cliente y un Servicio, gestionando el ciclo de vida de la reserva."""

    # Inicializador de la clase Reserva
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__(id_reserva)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "PENDIENTE"  # Estados posibles: PENDIENTE, CONFIRMADA, CANCELADA
        self._costo_total = 0.0

    # Propiedades para acceder a los atributos de la reserva con encapsulación
    @property
    def estado(self) -> str:
        return self._estado

    # Propiedad para acceder al costo total de la reserva
    @property
    def costo_total(self) -> float:
        return self._costo_total

    # Implementación del método abstracto para obtener un resumen de la reserva
    def procesar_y_confirmar(self, descuento: float = 0.0):
        """Calcula el costo final, marca el servicio como ocupado y confirma la reserva."""
        self._costo_total = self._servicio.calcular_costo(self._duracion_horas, descuento=descuento)
        self._servicio.disponible = False
        self._estado = "CONFIRMADA"

    # Implementación del método para cancelar la reserva y liberar el servicio
    def cancelar(self):
        """Cancela la reserva y libera nuevamente el servicio."""
        self._servicio.disponible = True
        self._estado = "CANCELADA"

    # Implementación del método abstracto para obtener un resumen de la reserva
    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion_horas}h | Total: ${self._costo_total:,.2f}"
        )