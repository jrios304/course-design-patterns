"""
Implementación del patrón Observer - Subject
Este patrón permite que múltiples observadores se suscriban a eventos
"""
from abc import ABC, abstractmethod
from typing import List, Any


class Observer(ABC):
    """
    Interfaz para los observadores.
    Los observadores reciben notificaciones cuando el subject cambia de estado.
    """

    @abstractmethod
    def update(self, subject: 'Subject', event: str, data: Any) -> None:
        """
        Método llamado cuando el subject notifica un cambio.

        Args:
            subject: El subject que notifica
            event: Nombre del evento
            data: Datos asociados al evento
        """
        pass


class Subject:
    """
    Clase base para subjects en el patrón Observer.
    Mantiene una lista de observadores y los notifica de cambios.
    """

    def __init__(self):
        """Inicializa la lista de observadores"""
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """
        Suscribe un observador.

        Args:
            observer: El observador a suscribir
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer {observer.__class__.__name__} attached")

    def detach(self, observer: Observer) -> None:
        """
        Desuscribe un observador.

        Args:
            observer: El observador a desuscribir
        """
        try:
            self._observers.remove(observer)
            print(f"Observer {observer.__class__.__name__} detached")
        except ValueError:
            pass

    def notify(self, event: str, data: Any = None) -> None:
        """
        Notifica a todos los observadores de un evento.

        Args:
            event: Nombre del evento
            data: Datos asociados al evento
        """
        print(f"Notifying {len(self._observers)} observers about event: {event}")
        for observer in self._observers:
            observer.update(self, event, data)

    def get_observers_count(self) -> int:
        """Retorna el número de observadores suscritos"""
        return len(self._observers)
