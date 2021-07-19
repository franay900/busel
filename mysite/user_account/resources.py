from import_export import resources
from .models import UserNet
 
class MemberResource(resources.ModelResource):
    class Meta:
        model = UserNet