import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BiologicalSimulation:
    def __init__(self, initial_preys, initial_predators, time_steps=100, disease_transmission_rate=0.001, predation_rate=0.01, weather_amplitude=0.05, weather_frequency=0.1):
        self.initial_preys = initial_preys
        self.initial_predators = initial_predators
        self.time_steps = time_steps
        self.disease_transmission_rate = disease_transmission_rate
        self.predation_rate = predation_rate
        self.weather_amplitude = weather_amplitude
        self.weather_frequency = weather_frequency
        
        if self.initial_preys < 0 or self.initial_predators < 0:
            raise ValueError("Initial population sizes cannot be negative")

    def run_simulation(self):
        # Simulation parameters
        growth_rate_preys = 0.1
        death_rate_predators = 0.05
        
        # Initialize arrays to hold population data
        prey_data = np.zeros((self.time_steps, 2))
        prey_data[:, 0] = np.arange(self.time_steps)  # Time steps
        prey_data[:, 1] = self.initial_preys  # Initialize prey population
        
        predator_data = np.zeros((self.time_steps, 2))
        predator_data[:, 0] = np.arange(self.time_steps)  # Time steps
        predator_data[:, 1] = self.initial_predators  # Initialize predator population
        
        infected_preys = np.zeros(self.time_steps)  # Initialize infected prey population
        infected_preys[0] = 10  # Initialize with 10 infected individuals
        
        # Simulation loop
        for i in range(1, self.time_steps):
            # Calculate weather factor
            weather_factor = 1 + self.weather_amplitude * np.sin(self.weather_frequency * i)
            
            # Adjust growth rate and predation rate based on weather
            growth_rate_preys_effective = growth_rate_preys * weather_factor
            predation_rate_effective = self.predation_rate * (1 - weather_factor)
            
            # Calculate disease transmission and mortality
            disease_transmission = self.disease_transmission_rate * infected_preys[i-1] * prey_data[i-1, 1]
            disease_mortality = 0.05 * infected_preys[i-1]
            
            # Update population sizes
            prey_data[i, 1] = max(0, prey_data[i-1, 1] * (1 + growth_rate_preys_effective * (1 - prey_data[i-1, 1] / 500) - predation_rate_effective * predator_data[i-1, 1] - disease_mortality))
            prey_data[i, 1] = min(500, max(0, prey_data[i-1, 1] * (1 + growth_rate_preys_effective * (1 - prey_data[i-1, 1] / 500) - predation_rate_effective * predator_data[i-1, 1] - disease_mortality)))

            infected_preys[i] = infected_preys[i-1] + disease_transmission - disease_mortality
            predator_data[i, 1] = max(0, predator_data[i-1, 1] * (1 - death_rate_predators + 0.005 * prey_data[i-1, 1] * predator_data[i-1, 1]))
            predator_data[i, 1] = min(200, max(0, predator_data[i-1, 1] * (1 - death_rate_predators + 0.005 * prey_data[i-1, 1] * predator_data[i-1, 1])))

        
        return prey_data, predator_data, infected_preys

    def visualize_results(self, prey_data, predator_data, infected_preys):
        df_preys = pd.DataFrame(prey_data, columns=['Time', 'Preys'])
        df_predators = pd.DataFrame(predator_data, columns=['Time', 'Predators'])
        df_infected = pd.DataFrame({'Time': np.arange(self.time_steps), 'Infected Preys': infected_preys})
        
        plt.plot(df_preys['Time'], df_preys['Preys'], label='Preys')
        plt.plot(df_predators['Time'], df_predators['Predators'], label='Predators')
        plt.plot(df_infected['Time'], df_infected['Infected Preys'], label='Infected Preys')
        plt.xlabel('Time')
        plt.ylabel('Population Size')
        plt.title('Population Growth Over Time with Disease, Predation, and Weather Changes')
        plt.legend()
        plt.show()

# Example usage
simulation = BiologicalSimulation(
    initial_preys=100,
    initial_predators=20,
    time_steps=200,
    disease_transmission_rate=0.005,
    predation_rate=0.02,
    weather_amplitude=0.1,
    weather_frequency=0.2
)
prey_data, predator_data, infected_preys = simulation.run_simulation()
simulation.visualize_results(prey_data, predator_data, infected_preys)