from django.contrib.gis.db.models.query import GeoQuerySet


class LiveGeoQuerySet(GeoQuerySet):

    def delete(self):
        # Override Django's built-in default.
        self.soft_delete()

    def soft_delete(self):
        self.update(alive=False)

    def undelete(self):
        self.update(alive=True)

    def hard_delete(self):
        # Default Django behavior.
        super(LiveGeoQuerySet, self).delete()

    def alive(self):
        return self.filter(alive=True)

    def non_dead(self):
        return self.alive()

    def dead(self):
        return self.filter(alive__isnull=True)
