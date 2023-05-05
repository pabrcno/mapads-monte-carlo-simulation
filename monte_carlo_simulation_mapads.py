import random
import math
import numpy as np

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def monte_carlo_simulation(num_clients, num_trials, radius, city_area, minimum_desired_clients):
    successful_trials = 0
    side_length = math.sqrt(city_area)
    
    # Generate clients' positions
    clients_positions = [(random.uniform(0, side_length), random.uniform(0, side_length)) for _ in range(num_clients)]

    for _ in range(num_trials):
        clients_within_radius = 0
        # simulate ride find random start and end points
        start_x, start_y = random.uniform(0, side_length), random.uniform(0, side_length)
        end_x, end_y = random.uniform(0, side_length), random.uniform(0, side_length)

        for client_x, client_y in clients_positions:
            # measure how many clients are within both end and start radius
            if distance(start_x, start_y, client_x, client_y) <= radius or distance(end_x, end_y, client_x, client_y) <= radius:
                clients_within_radius += 1
        # Sum if there are enough clients to complete the whole advertising space
        if clients_within_radius >= minimum_desired_clients:
            successful_trials += 1
   # return the percentage of successes
    return successful_trials / num_trials

def success_rate_city(num_clients, num_trials, radius, city_areas, minimum_desired_clients):
    success_rate_ci = {}
    
    for city, area in city_areas.items():
        success_rates = [monte_carlo_simulation(num_clients, num_trials, radius, area, minimum_desired_clients) for _ in range(num_simulations)]
        mean_success_rate = np.mean(success_rates)
        sem = np.std(success_rates) / math.sqrt(num_trials)
        # find lower and upper bound (assing error 4%)
        lower_bound = mean_success_rate - 1.96 * sem
        upper_bound = mean_success_rate + 1.96 * sem
        success_rate_ci[city] = (lower_bound, upper_bound)
    
    return success_rate_ci

def break_even_analysis(success_rate_city, adjusted_initial_investment):
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<25} {:<25} {:<25}".format("City", "Clients (Lower)", "Clients (Upper)", "Avg Clients", "Num Drivers", "Client per driver ratio", "Time to Recover Months", "Success Rate (Monte Carlo)"))
    print("-" * 165)
    
    for city, (lower_bound, upper_bound) in success_rate_city.items():
        clients_lower = base_num_clients + (base_num_clients * lower_bound)
        clients_upper = base_num_clients + (base_num_clients * upper_bound)
        avg_clients = math.ceil((clients_lower + clients_upper) / 2)
        clients_per_driver_ratio_value = math.ceil(avg_expected_client_payment / revenue_per_driver)
        num_drivers = math.ceil(avg_clients * clients_per_driver_ratio_value)
        clients_per_driver_ratio = f'1 : {clients_per_driver_ratio_value}'
        time_to_recover = math.ceil(adjusted_initial_investment / (avg_clients * avg_expected_client_payment))
        success_rate = (lower_bound + upper_bound) / 2

        print("{:<15} {:<15.2f} {:<15.2f} {:<15.2f} {:<15} {:<25} {:<25} {:<25.2%}".format(city, clients_lower, clients_upper, avg_clients, num_drivers, clients_per_driver_ratio, time_to_recover, success_rate))


avg_expense_per_driver = 98.94
revenue_per_driver = avg_expense_per_driver * 2
avg_expected_client_payment = 500
adjusted_initial_investment = 552600  # Fixed the value here
base_num_clients = math.ceil(adjusted_initial_investment / (avg_expected_client_payment * 12))
num_trials = 1000
radius = 1.5


minimum_desired_clients_per_trip = 4

city_areas = {
    "New York City": 468.9,
    "Los Angeles": 1302,
    "Chicago": 606.1,
    "Houston": 1709,
    "Phoenix": 1340,
    "Philadelphia": 347.6,
    "San Antonio": 1462,
    "San Diego": 963.6,
    "Dallas": 999.3,
    "San Jose": 467.4,
    "Austin": 964.5,
}


cities_success_rate = success_rate_city(base_num_clients, num_trials, radius, city_areas, minimum_desired_clients_per_trip)  # Fixed the parameter here

break_even_analysis(cities_success_rate, adjusted_initial_investment)