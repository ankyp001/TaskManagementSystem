from django.db import models

class taskModel(models.Model):
    assign_to = models.CharField(max_length=50)
    assign_by = models.CharField(max_length=50,null=True)
    created_by = models.CharField(max_length=50)
    comp_Name = models.CharField(max_length=50)
    task_Name =  models.CharField(max_length=50)
    task_Desc = models.TextField()
    task_Create = models.DateField()
    start_Date = models.DateField(null=True)
    start_Time = models.TimeField(null=True)
    end_Date = models.DateField(null=True)
    end_Time = models.TimeField(null=True)
    deadline_Date = models.DateField(null=True)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'task_Details'