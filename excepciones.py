"""
Módulo de excepciones personalizadas para Software FJ.
Define un control de errores para mantener el sistema estable.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base de la cual heredan todos los errores controlados del sistema."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando un dato tiene formato incorrecto"""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un argumento obligatorio o llega vacío."""
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta una acción inválida según el estado."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando el servicio ya está ocupado o reservado por otro cliente."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando las tarifas, descuentos o impuestos producen resultados inválidos."""
    pass