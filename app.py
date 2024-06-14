from constraint import Problem, AllDifferentConstraint
import pandas as pd

def generate_timetable(courses, teachers, days_per_course):
    # Initialize the problem
    problem = Problem()

    # Define time slots
    days = ["Sun", "Mon", "Tue", "Wed", "Thu"]
    slots_per_day = {
        "Sun": 5, "Mon": 5, "Tue": 3, "Wed": 5, "Thu": 5
    }
    time_slots = []
    for day in days:
        for slot in range(1, slots_per_day[day] + 1):
            time_slots.append(f"{day}_{slot}") 

    # Define variables and domains
    for course in courses:
        allowed_slots = [slot for slot in time_slots if slot.split('_')[0] in days_per_course[course]]
        if "TP" in teachers[course]:
            problem.addVariables([f"{course}_lecture", f"{course}_TD", f"{course}_TP"], allowed_slots)
        else:
            problem.addVariables([f"{course}_lecture", f"{course}_TD"], allowed_slots)

    # Hard Constraints

    # Four or five successive slots of work are not accepted (max three successive slots)
    def max_three_successive(*args):
        slots = sorted([int(slot.split('_')[1]) for slot in args])
        return all(abs(slots[i] - slots[i-1]) <= 1 for i in range(1, len(slots))) and len(slots) <= 3

    for course in courses:
        if "TP" in teachers[course]:
            problem.addConstraint(max_three_successive, [f"{course}_lecture", f"{course}_TD", f"{course}_TP"])
        else:
            problem.addConstraint(max_three_successive, [f"{course}_lecture", f"{course}_TD"])

    # Lectures of the same course should not be scheduled in the same slot
    for course in courses:
        if "TP" in teachers[course]:
            problem.addConstraint(lambda lecture, td, tp: lecture != td and lecture != tp and td != tp, (f"{course}_lecture", f"{course}_TD", f"{course}_TP"))
        else:
            problem.addConstraint(lambda lecture, td: lecture != td, (f"{course}_lecture", f"{course}_TD"))

    # Different courses for the same group must have different slot allocations
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            problem.addConstraint(AllDifferentConstraint(), [f"{courses[i]}_lecture", f"{courses[j]}_lecture"])
            problem.addConstraint(AllDifferentConstraint(), [f"{courses[i]}_TD", f"{courses[j]}_TD"])
            if "TP" in teachers[courses[i]] and "TP" in teachers[courses[j]]:
                problem.addConstraint(AllDifferentConstraint(), [f"{courses[i]}_TP", f"{courses[j]}_TP"])

    # Soft Constraints

    # Each teacher should have a maximum of two days of work
    def max_two_days(*args):
        days = [slot.split('_')[0] for slot in args]
        return len(set(days)) <= 2

    # Add the max_two_days constraint for each teacher's courses
    for course, teacher_list in teachers.items():
        if "TP" in teacher_list:
            problem.addConstraint(max_two_days, [f"{course}_lecture", f"{course}_TD", f"{course}_TP"])
        else:
            problem.addConstraint(max_two_days, [f"{course}_lecture", f"{course}_TD"])

    # Solve the problem
    solution = problem.getSolution()
    return solution

# Default courses and predefined teacher names
default_courses = [
    "Securite", "MethodesFormelles", "NumericalAnalysis", "Entrepreneuriat", 
    "RechercheOperationnelle2", "DistributedArchitecture", "Reseaux2", "ArtificialIntelligence"
]
default_teacher_names = {
    "Securite": ["Dr. Smith"], 
    "MethodesFormelles": ["Dr. Johnson"], 
    "NumericalAnalysis": ["Prof. Lee"], 
    "Entrepreneuriat": ["Dr. Brown"], 
    "RechercheOperationnelle2": ["Dr. Garcia"], 
    "DistributedArchitecture": ["Dr. Martinez"], 
    "Reseaux2": ["Dr. Robinson", "Dr. Clark", "Prof. Rodriguez", "Dr. Lewis"], 
    "ArtificialIntelligence": ["Prof. Walker", "Dr. Hall", "Dr. Allen"]
}
days_per_course = {
    "Securite": ["Sun", "Mon", "Tue", "Wed", "Thu"],
    "MethodesFormelles": ["Sun", "Mon", "Tue", "Wed", "Thu"],
    "NumericalAnalysis": ["Sun", "Mon", "Tue", "Wed", "Thu"],
    "Entrepreneuriat": ["Sun", "Mon", "Tue", "Wed", "Thu"],
    "RechercheOperationnelle2": ["Sun", "Mon", "Tue", "Wed", "Thu"],
    "DistributedArchitecture": ["Sun", "Mon", "Tue", "Wed", "Thu"],
    "Reseaux2": ["Sun", "Mon", "Tue", "Wed", "Thu"],
    "ArtificialIntelligence": ["Sun", "Mon", "Tue", "Wed", "Thu"]
}

solution = generate_timetable(default_courses, default_teacher_names, days_per_course)

if solution:
    print("Generated Timetable:")
    timetable_data = []
    for var, slot in solution.items():
        course, class_type = var.split('_')
        teachers = ", ".join(default_teacher_names[course])
        timetable_data.append((course, class_type, slot, teachers))
    
    df = pd.DataFrame(timetable_data, columns=["Course", "Class Type", "Time Slot", "Teachers"])
    print(df)
else:
    print("No solution found")


