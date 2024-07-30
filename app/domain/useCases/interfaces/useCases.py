from abc import ABC, abstractmethod

class EntityUseCasesInterface(ABC):
  """Template with the use cases for implementing into adapters"""

  @abstractmethod
  def create(self):
    pass

  @abstractmethod
  def get(self):
    pass

  @abstractmethod
  def get_all(self):
    pass

  @abstractmethod
  def update(self):
    pass

  @abstractmethod
  def delete(self):
    pass
