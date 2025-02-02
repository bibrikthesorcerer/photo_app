from django.db import models
from .managers import SoftDelManager

class SoftDelMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, default=None, blank=True)
    objects = SoftDelManager()
    
    class Meta:
        abstract = True
    


class MetaAbstract(models.Model):
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def show_info(self):
      """Custom method to show record fields inside the console."""
      print("-" * 20)
      fields = [field.name for field in list(self._meta.fields)]
      for field in [f"{field}: {getattr(self, field)}" for field in fields]:
         print(field, end="\n")
      print("-" * 20)

   def in_use(self):
      print(self.get_related_objects())
      return any(self.get_related_objects())

   def get_related_objects(self):
      related_objects = []
      for related_object in self._meta.get_fields():
         if (
               (related_object.one_to_many or related_object.one_to_one)
               and related_object.auto_created
               and not related_object.concrete
         ):
               accessor_name = related_object.get_accessor_name()
               related_manager = getattr(self, accessor_name)
               if related_manager.exists():
                  related_objects.append(related_manager)
         elif related_object.many_to_many:
               related_manager = getattr(self, related_object.name)
               if related_manager.exists():
                  related_objects.append(related_manager)
      return related_objects

   class Meta:
      abstract = True


class BaseModel(MetaAbstract):
    class Meta:
        abstract = True