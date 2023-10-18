# Financial Analyzer

## Introduction

In today's dynamic and complex financial landscape, having a clear understanding of your financial situation is essential. The Financial Analyzer App provides a comprehensive solution to manage and analyze your finances effectively. The purpose of this application is to analyze users' current and previous financial behavior, find out if there are changes in patterns and finally summarize the report back to the user. The solutions is a combination of statistical analysis of data and decision making powered by Large Language Model services. Using the power of OpenAI APIs make the summaries more readable to the end users.

## Getting Started

### Dependencies

* Tested on Python 3.10.12
* OpenAI API Key
* MongoDB

### Installation

1. Install the required packages using the command: `pip install -r requirements.txt`

2. If mongodb is not available, use `docker-compose up` to start a mongodb instance.

3. Create a `.env` file in the root directory and add the following variables:

    ```text
    MONGO_CONNECTION_STRING=""
    DB_NAME=""
    COLLECTION_NAME=""
    OPENAI_API_KEY=""
    ```

4. Run the fast API server using the command: `uvicorn app.main:app --reload`

5. Open the swagger UI at `http://127.0.0.1/api/docs`

## Key Features

* Upload financial data
* Analyze financial data
* Summarize financial data
* Provide the summary in user readable format
* Choose the best summary from multiple options

## Contact

Feel free to contact me for any feedback, suggestions or collaborations.

* **Email**: [sifatnabil@gmail.com](mailto:sifatnabil@gmail.com)
* **LinkedIn**: [linkedin.com/in/sifatnabil](https://www.linkedin.com/in/sifatnabil/)
