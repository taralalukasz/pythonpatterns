import abc #this stands for abstract base class
from domain.model import Batch


#technically, every class witch has add() and get() methods is repository abstraction
#duck typing - recognizing objects by it's methods  or behavior, not actual hardcoded Type (which in python frequently isn't defined)
#ABC serves as interface in other languages - python doesn't have "interface" keyword, we have to simiulate it
#CONCLUSION - Repository pattern is btter in bigger project. In small CRUD it's better to use automated ORM 
class AbstractRepository(abc.ABC):

    @abc.abstractmethod  #<- python will refuse to instantiate a class if all annotated methods are not implemented
    def add(self, batch: Batch):
        raise NotImplementedError
    @abc.abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(Batch).all()
    
class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = batches

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return self._batches