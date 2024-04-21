"""
Importing pandas library to read from csv file
"""
import pandas as pd

class DataIngestor:
    """
    DataIngestor class to handle the data
    """
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = pd.read_csv(self.csv_path, usecols=['LocationDesc',
                                                        'Data_Value', 
                                                        'Question', 
                                                        'Stratification1', 
                                                        'StratificationCategory1'])
        # Sorting the values alphabetically
        self.data = self.data.sort_values(['LocationDesc','Stratification1', 'StratificationCategory1' ])

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]


    def states_mean(self, question):
        """
        Calculate the mean values for each state for a given question.
        """
        # Getting the datasets for my question
        question_data = self.data[self.data['Question'] == question]

        # Calculating the mean value
        mean_values = question_data.groupby('LocationDesc')['Data_Value'].mean()
        mean_values = mean_values.sort_values(ascending=True)

        # Create an empty dictionary to store the state means
        state_means_dict = {}

        # Creating the dictionary
        for state, mean_value in mean_values.items():
            state_means_dict[state] = mean_value

        return state_means_dict


    def state_mean(self, question, state):
        """
        Calculate the mean value for a given state and question.
        """
        question_data = self.data[(self.data['Question'] == question) &
                        (self.data['LocationDesc'] == state)]

        # Calculating the mean value for the given state
        mean_value = question_data['Data_Value'].mean()

        return {state: mean_value}

    def global_mean(self, question):
        """
        Calculate the global mean value for a given question
        """
        # Getting the datasets for the given question
        question_data = self.data[self.data['Question'] == question]

        # Calculating the global mean value for the given question
        global_mean_value = question_data['Data_Value'].mean()

        # Creating and returning the dictionary
        return {'global_mean': global_mean_value}

    def best_five(self, question):
        """
        Get the top five states with the best values for a given question.
        """
        question_data = self.data[self.data['Question'] == question]
        mean_values = question_data.groupby('LocationDesc')['Data_Value'].mean()
        if question in self.questions_best_is_min:
            sorted_state_mean = mean_values.sort_values(ascending=True)
        else:
            sorted_state_mean = mean_values.sort_values(ascending=False)

        top_five_states = dict(list(sorted_state_mean.items())[:5])
        return top_five_states

    def worst_five(self, question):
        """
        Get the top five states with the worst values for a given question.
        """
        question_data = self.data[self.data['Question'] == question]
        mean_values = question_data.groupby('LocationDesc')['Data_Value'].mean()
        if question in self.questions_best_is_max:
            sorted_state_mean = mean_values.sort_values(ascending=True)
        else:
            sorted_state_mean = mean_values.sort_values(ascending=False)

        top_five_states = dict(list(sorted_state_mean.items())[:5])
        return top_five_states

    def diff_from_mean(self, question):
        """
        Calculate the difference of each state's mean value from the global mean value 
        for a given question.
        """
        global_mean = self.global_mean(question)['global_mean']
        data_values_states_mean = self.states_mean(question)

        diff_dict = {}
        for state, state_mean in data_values_states_mean.items():
            diff_dict[state] = global_mean - state_mean

        return diff_dict

    def state_diff_from_mean(self, question, state):
        """
        Calculate the difference of a given state's mean value from the global mean value 
        for a given question.
        """
        data_value_global_mean = self.global_mean(question)['global_mean']
        data_values_state_mean = self.state_mean(question, state)[state]
        diff = data_value_global_mean - data_values_state_mean
        return {state : diff}

    def mean_by_category(self, question):
        """
        Calculate the mean values for each category and stratification for a given question.
        """
        # Getting the datasets for the specified question
        question_data = self.data[self.data['Question'] == question]

        # Calculate mean values for each stratification
        mean_values = question_data.groupby(['LocationDesc'
        , 'StratificationCategory1','Stratification1'])['Data_Value'].mean()

        # Changing the key from tuple to string and making the dictionary
        mean_values_dict = {}
        for key, value in mean_values.items():
            mean_values_dict[str(key)] = value

        return mean_values_dict


    def state_mean_by_category(self, question, state):
        """
        Calculate the mean values for each category and stratification 
        for a given question and state.
        """
        # Getting the datasets for the specified question and state
        question_data = self.data[(self.data['Question'] == question) &
                        (self.data['LocationDesc'] == state)]

        # Calculate mean values for each stratification
        mean_values = question_data.groupby(['StratificationCategory1',
                        'Stratification1'])['Data_Value'].mean()

        # Changing the key from tuple to string and making the dictionary
        mean_values_dict = {}
        for key, value in mean_values.items():
            mean_values_dict[str(key)] = value

        return {state: mean_values_dict}
