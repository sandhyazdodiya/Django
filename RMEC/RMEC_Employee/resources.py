from import_export import resources
from .models import RMEC_Employee

class RMEC_EmployeeResource(resources.ModelResource):
    class Meta:
        model = RMEC_Employee