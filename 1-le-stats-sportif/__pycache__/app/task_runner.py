"""
Importing the libraries
"""
from queue import Queue
from threading import Thread, Lock
import multiprocessing
import os
import json
from app.data_ingestor import DataIngestor

class ThreadPool:
    """
    Threadpool class
    """
    def __init__(self):
        """
        ThreadPool initialization
        """
        # Setting the number of threads accordingly
        threads_number = os.environ.get("TP_NUM_OF_THREADS")
        if threads_number is None:
            threads_number = multiprocessing.cpu_count()

        # Thread list
        self.threads = []

        # Queue consisting of: {job_id, question, question_type}
        self.job_queue = Queue()

        # Dictionary consisting of: {'key': job_id, 'value': result}
        self.job_id_dict = {}

        self.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

        for _ in range(threads_number):
            task_runner = TaskRunner(self.job_queue, self, self.job_id_dict, self.data_ingestor)
            self.threads.append(task_runner)

        for thread in self.threads:
            thread.start()

    def add_task(self, job_id, data, question_type, result, state):
        """
        Function to add job in job_queue and set the job_id value to None (result)
        """

        # I put result there because I had Pylint error "unused argument"
        # Initialized result with None in routes.py
        self.job_id_dict[job_id] = result
        self.job_queue.put((job_id, data, question_type, state))

class TaskRunner(Thread):
    """
    TaskRunner class to handle asynchronous task execution.
    """

    def __init__(self, job_queue, thread_pool, job_id_dict, data_ingestor):
        super().__init__()
        self.job_queue = job_queue
        self.thread_pool = thread_pool
        self.job_id_dict = job_id_dict
        self.data_ingestor = data_ingestor
        self.lock = Lock()

    def run(self):
        """
        Execute the task and update the job_id_dict with the result.
        """
        while True:
            # Get pending job 
            job = self.job_queue.get()

            # Getting the variables
            question = job[1]['question']
            question_type = job[2]
            job_id = job[0]
            state = job[3]

            # Define a mapping of question_type to method calls for removing else if
            method_mapping = {
                "/api/states_mean": lambda: self.data_ingestor.states_mean(question),
                "/api/global_mean": lambda: self.data_ingestor.global_mean(question),
                "/api/state_mean": lambda: self.data_ingestor.state_mean(question, state),
                "/api/best5": lambda: self.data_ingestor.best_five(question),
                "/api/worst5": lambda: self.data_ingestor.worst_five(question),
                "/api/diff_from_mean": lambda: self.data_ingestor.diff_from_mean(question),
                "/api/state_diff_from_mean": 
                lambda: self.data_ingestor.state_diff_from_mean(question, state),
                "/api/mean_by_category": lambda: self.data_ingestor.mean_by_category(question),
                "/api/state_mean_by_category": 
                lambda: self.data_ingestor.state_mean_by_category(question, state)
            }

            # Check the question type and add the result to dictionary
            if question_type in method_mapping:
                result = method_mapping[question_type]()
            else:
                result = {"error": "Invalid question_type"}

             # Acquire the lock before updating the shared resource
            with self.lock:
                self.job_id_dict[job_id] = result
            
            # Stopping when there are no jobs left
            if job is None:
                break

            # Creating the files and writing the results
            with open('results/' + str(job_id), 'w', encoding='utf-8') as file:
                result_json = json.dumps(self.job_id_dict[job_id])
                file.write(result_json)
