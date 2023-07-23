from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from shareholding.application import ShareholdingApplication
from shareholding.domainmodel import ShareClass, Shareholding


class TestShareholdingApplication(TestCase):
    def test_shareholding(self):
        app = ShareholdingApplication()
        # A situation...
        person = app.register_person(name="Joe")
        self.assertEqual(person.name, "Joe")
        company = app.register_company(name="Acme")

        # Something happens...
        shareholding = company.allot_shares(
            person_id=person.id,
            number_of_shares=10,
            share_class_name="ordinary",
            nominal_value_per_share=Decimal("1.00"),
            price_paid_per_share=Decimal("1.00"),
            currency="GBP",
            allotted_on=datetime.now(),
        )

        self.assertIsInstance(shareholding, Shareholding)
        self.assertEqual(shareholding.shareholder, person.id)
        self.assertEqual(shareholding.number_of_shares, 10)
        self.assertEqual(shareholding.share_class_name, "ordinary")

        share_class_name = shareholding.share_class_name
        share_class = company.get_shareclass(share_class_name)
        self.assertIsInstance(share_class, ShareClass)
        self.assertEqual(share_class.name, "ordinary")
        self.assertEqual(share_class.nominal_value, Decimal("1.00"))
        self.assertEqual(share_class.currency, "GBP")

        self.assertEqual(
            company.count_shareholdings(person.id, share_class_name), 1
        )

        shareholding = company.allot_shares(
            person_id=person.id,
            number_of_shares=10,
            share_class_name="ordinary",
            nominal_value_per_share=Decimal("1.00"),
            price_paid_per_share=Decimal("1.00"),
            currency="GBP",
            allotted_on=datetime.now(),
        )

        self.assertEqual(
            company.count_shareholdings(person.id, share_class_name), 2
        )

        # company.issue_shares(
        #     person_id=person.id,
        #     number_of_shares=10,
        #     share_class_name="ordinary",
        #     nominal_value_per_share=Decimal("1.00"),
        #     price_paid_per_share=Decimal("1.00"),
        #     currency='GBP',
        #     issued_on=datetime.now(),
        # )
