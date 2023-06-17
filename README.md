# Map Matching Project

This project implements map matching, which is the process of matching observed geographic coordinates to the underlying road network. The goal is to find the most likely route that a user has followed based on their recorded positions. The road network data was taken for San Francisco.

## Project Structure

The project is organized into two main folders:

- `frontend`: Contains the frontend code for the map matching project.
- `backend`: Contains the backend code for the map matching project.
- `input`: Contains the sample input GPX traces.
- `backend`: Contains the output after processing.

## Prerequisites

Before running the project, ensure that you have the following prerequisites installed:

- Node.js (for running the frontend)
- Python 3 (for running the backend)

## How to Run

### Frontend

To run the frontend, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the `frontend` folder: `cd frontend`.
3. Install the required Node modules by running: `npm i`.
4. Once the installation is complete, start the frontend server by running: `npm start`.
5. The frontend application will be accessible at `http://localhost:3000` in your web browser.

### Backend

To run the backend, follow these steps:

1. Open a separate terminal or command prompt.
2. Navigate to the `backend` folder: `cd backend`.
3. Install the required Python packages by running: `pip install -r requirements.txt`.
4. Once the installation is complete, start the backend server by running: `python server.py`.
5. The backend server will start running and listen for requests on `http://localhost:5000`.

**Note:** Ensure that you start the backend server before using the frontend application, as it relies on the backend API for map matching functionality.

## Contributing

Contributions to the map matching project are welcome. If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch to your fork.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the codebase in accordance with the terms specified in the license.

## Acknowledgements

We would like to acknowledge the contributions and support from the open-source community and various libraries used in this project.

Please feel free to reach out with any questions, feedback, or issues you may encounter.
