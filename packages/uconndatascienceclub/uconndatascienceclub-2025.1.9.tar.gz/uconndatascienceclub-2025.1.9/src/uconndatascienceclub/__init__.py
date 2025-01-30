import os
import pandas as pd
import numpy as np

uconntact = 'https://uconntact.uconn.edu/organization/datascience'
instagram = '@uconndatascience'
email = 'uconndatascience@gmail.com'
discord = 'https://discord.gg/zTTYvVAa'

def welcome():
        '''Get a welcome message to ensure package is working properly.
        
        Returns
        -------
        str
            A welcome string.
        '''
        return 'Welcome to UConn Data Science Club!'

def schedule(year: int=2025, semester: str='spring') -> dict:
        '''
        Get the schedule for the specified year and semester.

        Parameters
        ----------
        year : int, optional
            The academic year. Must be one of {2024, 2025}. Default is 2025 (current year).
        semester : str, optional
            The academic semester. Must be one of {'spring', 'fall'}. Default is 'spring'.

        Returns
        -------
        dict
            A dictionary representing the schedule for the given year and semester.
        '''
        # implementation
        print('Coming soon!')
        pass

class Courses():
    pass

class Data():
    
    def __init__(self, dataset=None):
        if dataset:
            self.dataset = dataset.lower()
        else:
            self.dataset = None

        self.available_datasets = {
            #'boston': 'housing.csv',
            None: None,
            'forbes': 'Forbes_Global_2000.csv',
            'mall': 'Mall_Customers.csv',
            'fires': 'forestfires.csv',
            'population': ''
        }

        if self.dataset not in self.available_datasets:
            raise ValueError(
                f"Dataset '{self.dataset}' is not available. "
                f"Choose from {self.list_datasets()}."
            )
    
    def dataframe(self) -> pd.DataFrame:

        if not self.dataset:
            self.no_data()

        dataset_path = os.path.join(os.path.dirname(__file__), 'datasets', self.available_datasets[self.dataset])

        if self.dataset == 'forbes':
            return pd.read_csv(dataset_path, encoding='latin1')
        if self.dataset == 'population':
            return pd.DataFrame({
                                    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
                                    "Population": [8419600, 3980400, 2716000, 2328000, 1690000],
                                    "Latitude": [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
                                    "Longitude": [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740]
                                })
        
        return pd.read_csv(dataset_path)
    
    def list_datasets(self):
        return list(self.available_datasets.keys())
    
    def no_data(self):
        #for error handling
        raise ValueError(
            f"No dataset established. "
            f"Choose from {self.list_datasets()}. "
            f"Call the `set_data()` method to establish a dataset."
        )
    
    def set_data(self, data):
         if data not in self.available_datasets:
            raise ValueError(
                f"Dataset '{self.dataset}' is not available. "
                f"Choose from {self.list_datasets()}."
            )
         
         self.dataset = data.lower()

    def save(self) -> None:

        if not self.dataset:
            self.no_data()

        df = self.dataframe()
        df.to_csv(self.available_datasets[self.dataset])

    def source(self, data=None) -> str:
        pass
    
    def standard(self, dim=1, size=100, state=None) -> pd.DataFrame:
        if state:
            np.random.seed(state)  
        data = np.random.standard_normal(size=(size, dim))  
        return pd.DataFrame(data, columns=[f"col_{i+1}" for i in range(dim)])

    def uniform(self, dim=1, size=100, state=None) -> pd.DataFrame:
        if state:
            np.random.seed(state)  
        data = np.random.uniform(low=0, high=1, size=(100, dim))  
        return pd.DataFrame(data, columns=[f"col_{i+1}" for i in range(dim)])

class OnlineResources():
    pass


