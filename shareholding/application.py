from eventsourcing.application import Application

from shareholding.domainmodel import Company, Person


class ShareholdingApplication(Application):

    def register_person(self, name):
        person = Person(name=name)
        self.save(person)
        return person

    def register_company(self, name):
        company = Company(name=name)
        self.save(company)
        return company
