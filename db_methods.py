import Functions

def update_schedule(hours, minutes, daily):
    new_schedule = []
    for i in range(len(hours)):
        if hours[i].get() != "":
            if minutes[i].get() == "":
                new_schedule.append(hours[i].get() + ":00")
            else:
                new_schedule.append(hours[i].get() + ":" + minutes[i].get())
    daily["schedule"] = new_schedule
    Functions.db.update("database", "DailyTours", [daily])
    Functions.hide_all_frames("coordinator_menu")


def change_rules(new_rules):
    Functions.db.update("database", "general_data", [{"name": "general_rules",
                                                      "data": new_rules}])
    return Functions.hide_all_frames("admin_menu")

def get_locations():
    return [x["Location"] for x in Functions.upcoming_tours]

def get_schedules():
    schedules = dict()
    for location in get_locations():
        schedules[location] = \
            schedule = Functions.db.search_by_value("database", "DailyTours",
                                                    "Name",location)
        if schedule:
            schedules[location] = schedule[0]["schedule"]
    return schedules



