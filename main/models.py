from __future__ import unicode_literals

from django.db import models
#from adaptor.fields import *
#from data_importer.importers import CSVImporter

# Create your models here.

#class ContohCsv(CSVImporter):
#	fields = ['age', 'population']

#	class Meta:
#		delimiter = b','
#		ignore_first_line = True

# class History(models.Model):
# 	ID_T1 = CharField()
# 	ID_T2 = CharField()
# 	ID_Z = CharField()
# 	Area = IntegerField()
# 	Period = CharField()
# 	AreaName = CharField()
# 	PlanningUnit = CharField()
# 	PeatType = CharField()
# 	LandcoverName_T1 = CharField()
# 	Carbon_T1 = FloatField()
# 	Peat_T1 = FloatField()
# 	LandcoverName_T2 = CharField()
# 	Carbon_T2 = FloatField()
# 	Peat_T2 = FloatField()
# 	LandProfit_T1 = FloatField()
# 	LandProfit_T2 = FloatField()

# class HistoryCsv(CsvModel):
# 	ID_T1 = CharField(match = "ID_LC_T1")
# 	ID_T2 = CharField(match = "ID_LC_T2")
# 	ID_Z = CharField(match = "ID_Z")
# 	Area = IntegerField(match = "COUNT_AREA")
# 	Period = CharField(match = "PERIOD")
# 	AreaName = CharField(match = "ADMIN")
# 	PlanningUnit = CharField(match = "PLAN")
# 	PeatType = CharField(match = "PEAT")
# 	LandcoverName_T1 = CharField(match = "LC_T1")
# 	Carbon_T1 = FloatField(match = "C_T1")
# 	Peat_T1 = FloatField(match = "P_T1")
# 	LandcoverName_T2 = CharField(match = "LC_T2")
# 	Carbon_T2 = FloatField(match = "C_T2")
# 	Peat_T2 = FloatField(match = "P_T2")
# 	LandProfit_T1 = FloatField(match = "PROF_T1")
# 	LandProfit_T2 = FloatField(match = "PROF_T2")

# 	class Meta:
# 		#delimiter = ','
# 		dbModel = History
# 		#has_header = True

