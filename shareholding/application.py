from eventsourcing.application.sqlalchemy import SQLAlchemyApplication
from eventsourcing.domain.model.aggregate import AggregateRoot

from shareholding.domainmodel import Person, Company


class ShareholdingApplication(SQLAlchemyApplication):
    persist_event_type = AggregateRoot.Event

    def register_person(self, name):
        person = Person.__create__(name=name)
        person.__save__()
        return person

    def register_company(self, name):
        company = Company.__create__(name=name)
        company.__save__()
        return company