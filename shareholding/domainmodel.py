from decimal import Decimal
from uuid import UUID

from eventsourcing.domain.model.aggregate import AggregateRoot


class Person(AggregateRoot):
    def __init__(self, *, name, **kwargs):
        super(Person, self).__init__(**kwargs)
        self._name = name

    @property
    def name(self):
        return self._name


class Company(AggregateRoot):
    __subclassevents__ = True

    def __init__(self, *, name, **kwargs):
        super(Company, self).__init__(**kwargs)
        self._shareclasses = {}
        self._name = name

    def allot_shares(
        self,
        person_id,
        number_of_shares,
        share_class_name,
        nominal_value_per_share,
        price_paid_per_share,
        currency,
        allotted_on,
    ):
        assert isinstance(person_id, UUID)
        assert isinstance(number_of_shares, int)
        assert isinstance(share_class_name, str)
        assert isinstance(nominal_value_per_share, Decimal)
        assert isinstance(price_paid_per_share, Decimal)
        # The work of the command.
        shareholding = Shareholding(
            shareholder=person_id,
            number_of_shares=number_of_shares,
            share_class_name=share_class_name,
            nominal_value_per_share=nominal_value_per_share,
            price_paid_per_share=price_paid_per_share,
            currency=currency,
            allotted_on=allotted_on,
        )
        self.__trigger_event__(self.SharesAllotted, shareholding=shareholding)
        return shareholding

    class SharesAllotted(AggregateRoot.Event):
        def mutate(self, obj: "Company"):
            try:
                shareclass = obj._shareclasses[self.shareholding.share_class_name]
            except KeyError:
                shareclass = ShareClass(
                    name=self.shareholding.share_class_name,
                    nominal_value=self.shareholding.nominal_value_per_share,
                    currency=self.shareholding.currency,
                )
                obj._shareclasses[self.shareholding.share_class_name] = shareclass
            assert isinstance(shareclass, ShareClass)
            shareclass.add_allotment(self.shareholding)

        @property
        def shareholding(self) -> "Shareholding":
            return self.__dict__["shareholding"]

    def get_shareclass(self, share_class_name):
        return self._shareclasses.get(share_class_name)

    def count_shareholdings(self, person_id, share_class_name):
        count = 0
        share_class = self._shareclasses[share_class_name]
        assert isinstance(share_class, ShareClass)
        for allotment in share_class.shareholdings:
            assert isinstance(allotment, Shareholding)
            if allotment.shareholder == person_id:
                count += 1
        return count


class Shareholding(object):
    def __init__(
        self,
        shareholder,
        number_of_shares,
        share_class_name,
        nominal_value_per_share,
        price_paid_per_share,
        currency,
        allotted_on,
    ):
        self.shareholder = shareholder
        self.number_of_shares = number_of_shares
        self.share_class_name = share_class_name
        self.nominal_value_per_share = nominal_value_per_share
        self.price_paid_per_share = price_paid_per_share
        self.currency = currency
        self.allotted_on = allotted_on
        self.status = "allotted"


class ShareClass(object):
    def __init__(self, name, nominal_value, currency):
        self._name = name
        self._nominal_value = nominal_value
        self._currency = currency
        self._shareholdings = []

    @property
    def name(self):
        return self._name

    @property
    def nominal_value(self):
        return self._nominal_value

    @property
    def currency(self):
        return self._currency

    @property
    def shareholdings(self):
        return self._shareholdings

    def add_allotment(self, allotment):
        self._shareholdings.append(allotment)
