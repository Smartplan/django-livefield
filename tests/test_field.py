from django.db import IntegrityError
from django.db import transaction
from django.test import TestCase

from .models import Person


class LiveFieldTests(TestCase):

    def test_inits_alive(self):
        o = Person(name='test')
        self.assertTrue(o.alive)

    def test_saving_retains_alive(self):
        o = Person(name='test')
        o.save()
        o2 = Person.all_objects.get(id=o.id)
        self.assertTrue(o2.alive)

    def test_saving_retains_dead(self):
        o = Person(name='test')
        o.alive = False
        o.save()
        o2 = Person.all_objects.get(id=o.id)
        self.assertFalse(o2.alive)

    def test_truthy_values_dont_delete(self):
        for name, val in enumerate(['truthy', 11, float(6.0), True, (1, 3)]):
            obj = Person(name=name)
            obj.alive = val
            obj.save()
            obj.refresh_from_db()
            # Use 'is' to make sure that we're returning bools.
            self.assertTrue(obj.alive is True)

    def test_falsy_values_delete(self):
        for name, val in enumerate(['', 0, False, {}, None]):
            obj = Person(name=name)
            obj.alive = val
            obj.save()
            obj = Person.all_objects.get(id=obj.id)
            # Again, use 'is' to make sure that we're returning bools.
            self.assertTrue(obj.alive is False)

    def test_allows_uniqueness_with_many_dead(self):
        first = Person(name='collision')
        first.save()
        second = Person(name='collision')
        # Uniqueness constraint should prevent a second live object with the
        # same name.
        with transaction.atomic():
            self.assertRaises(IntegrityError, second.save)

        # Should be able to have several dead objects with same name
        first.alive = False
        first.save()
        # Now we can save and delete second
        second.save()
        second.alive = False
        second.save()

        third = Person(name='collision')
        third.save()
        self.assertEqual(Person.all_objects.count(), 3)

        # Resurrecting one of the dead dupes should violate uniqueness
        first.alive = True
        with transaction.atomic():
            self.assertRaises(IntegrityError, first.save)
