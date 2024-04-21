# Multi-threaded Flask Server for Real-time Data Processing


### Introduction
This project focuses on the development of a multi-threaded Flask server capable of real-time data processing. The server implementation utilizes advanced techniques such as thread pooling and efficient task management to handle concurrent data requests seamlessly.

## Implementation Details

### ThreadPool Class
- **Initialization (`__init__()`):**
  - Sets the number of threads based on specifications.
  - Initializes a job queue (`job_queue`) and a dictionary (`job_id_dict`) to track job statuses.
  - Initializes a `DataIngestor` instance for data processing functions.

- **Adding Tasks (`add_task()`):**
  - Implements logic to add a job to the queue, including job ID, data, and question type.
  - Initializes the `job_id_dict` with `None` values for result tracking.

### TaskRunner Class
- **Initialization (`__init__()`):**
  - Accepts parameters such as job queue, thread pool instance, job ID dictionary, and data ingestor instance.
  - Utilizes a lock mechanism for synchronization during dictionary updates.

- **Task Execution (`run()`):**
  - Threads process jobs by waiting for tasks from the job queue.
  - Upon extraction, the thread identifies the question type and invokes the corresponding function from `DataIngestor`.
  - Updates the `job_id_dict` with the result and utilizes locks for thread safety.
  - Upon completion, results are written to the `results` directory with the corresponding job ID.

### routes.py File
- **Endpoint Implementation:**
  - Implements the `get_response(job_id)` method to extract results from the `job_id_dict`.
  - Checks for validity and returns appropriate messages or processed results.
  - Subsequent functions increment job IDs and enqueue tasks, adding them to the `job_id_dict`.

### DataIngestor Class
- **Data Processing Logic:**
  - Reads data from the CSV file and extracts relevant columns.
  - Implements various data processing methods for different types of requests.
  - Each method follows a similar logic pattern: extract question-specific data, process the data, and return the resulting dictionary.

## Request Handling Mechanism
- Upon receiving a request, the server associates a unique job ID with it.
- The request is encapsulated into a closure and placed in a job queue for processing by a thread pool.
- A thread retrieves a job from the job queue, executes the associated operation, and writes the result to a file named after the job ID in the `results/` directory.

## Server Endpoints
- `/api/states_mean`: Calculates the mean of data values for each state and sorts them in ascending order.
- `/api/state_mean`: Calculates the mean of data values for a specific state.
- `/api/best5`: Calculates the mean of data values for all states and returns the top 5.
- `/api/worst5`: Calculates the mean of data values for all states and returns the bottom 5.
- `/api/global_mean`: Calculates the mean of data values across all states.
- `/api/diff_from_mean`: Calculates the difference between the global mean and state mean for all states.
- `/api/state_diff_from_mean`: Calculates the difference between the global mean and state mean for a specific state.
- `/api/mean_by_category`: Calculates the mean value for each segment within categories for all states.
- `/api/state_mean_by_category`: Calculates the mean value for each segment within categories for a specific state.
- `/api/graceful_shutdown`: Initiates a graceful shutdown of the server.
- `/api/jobs`: Retrieves all job IDs and their statuses.
- `/api/num_jobs`: Retrieves the number of remaining jobs for processing.
- `/api/get_results/<job_id>`: Retrieves the result of a specific job ID.
