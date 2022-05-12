from django.urls import path
from planning.views import CalendarView, month, week, day


urlpatterns = [
    path('calendar/', CalendarView.as_view()),
    path("planner/api/calendar/month/<int:year>/<int:month>/", month),
    path("planner/api/calendar/week/<int:year>/<int:month>/<int:day>/", week),
    path("planner/api/calendar/day/<int:year>/<int:month>/<int:day>/", day)

]
