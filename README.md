**Project Presentation: Multi-threaded Flask Server for Data Processing**

**Introduction:**
The project involves the development of a multi-threaded Flask server aimed at efficiently processing data requests. Leveraging Flask, a micro web framework for Python, the objective is to build an application capable of handling various data processing tasks concurrently.

**Project Structure:**
1. **Thread Pool Mechanism:**
   - Implementation of a thread pool to manage concurrent execution of tasks.
   - Utilization of a ThreadPool class to manage a fixed number of threads.
   - Efficient processing of incoming requests using a TaskRunner class.

2. **Data Processing:**
   - Loading and extracting information from a CSV file during server startup.
   - Calculation of statistics requested at the request level.
   - Various endpoints designed to cater to specific data processing tasks.

3. **Endpoints Implemented:**
   - `/api/states_mean`: Calculate the mean of data values for each state over the entire time interval (2011 - 2022) and sort them in ascending order.
   - `/api/state_mean`: Calculate the mean of data values for a specific state over the entire time interval (2011 - 2022).
   - `/api/best5` and `/api/worst5`: Calculate the mean of data values for all states and return the top 5 or bottom 5 states.
   - `/api/global_mean`: Calculate the global mean of data values over the entire time interval (2011 - 2022).
   - Various other endpoints for different data processing tasks as specified in the requirements.

4. **Handling Requests:**
   - Assigning a job ID to each request and queuing the job for processing.
   - Asynchronous processing of jobs using a thread pool mechanism.
   - Writing the result of each calculation to a file with the corresponding job ID.

5. **Graceful Shutdown:**
   - Implementation of a `/api/graceful_shutdown` endpoint to gracefully shut down the server.
   - No longer accepting new requests, finishing processing existing requests, and then shutting down.

6. **Monitoring and Management:**
   - Endpoints such as `/api/jobs` and `/api/num_jobs` to monitor job status and count.
   - `/api/get_results/<job_id>` endpoint to retrieve results of processed jobs.

**Flask Framework:**
Flask, an open-source micro web framework, is utilized for building the server application. Its minimalist and flexible nature allows for rapid development of web applications using Python. Flask provides essential tools for URL routing, request handling, session management, templating, and cookie management.

**Installation and Setup:**
- Clone the project repository.
- Create and activate a virtual environment.
- Install the required dependencies using the provided `requirements.txt`.
- Start the Flask server.

**Conclusion:**
The project showcases the development of a robust multi-threaded Flask server capable of handling complex data processing tasks efficiently. By leveraging Flask's simplicity and flexibility along with multi-threading capabilities, a scalable solution for processing data requests in real-time is achieved.
