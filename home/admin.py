from django.contrib import admin
from .models import About, Recent, Upcoming, Gallery, StudentProfile, HallOfFame, ActivationStatus, OnlineContestProfile, SustContestProfile, Bio, UvaProblems

admin.site.register(About)
admin.site.register(Recent)
admin.site.register(Upcoming)
admin.site.register(Gallery)
admin.site.register(HallOfFame)
admin.site.register(StudentProfile)
admin.site.register(ActivationStatus)
admin.site.register(Bio)
admin.site.register(OnlineContestProfile)
admin.site.register(SustContestProfile)
admin.site.register(UvaProblems)
