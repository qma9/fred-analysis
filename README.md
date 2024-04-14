Write a tool in Python that communicates with a free API, retrieves some data and performs an analysis of that data. For example, you can use the World POP API to retrieve and analyse world population data.

Here are some ideas of how to use the topics covered in the class in this assignment:

1. Communicate with the API using concurrent programming. The challenge is to make sure that API requests stay within the rate limit of the API you're using, but that at the same time retrieving a lot of data doesn't block the application.

2. Graphical user interfaces are not covered in this course, so you could perform an analysis and store the result in a CSV file. Another possibility is to use a framework for dashboards such as Plotly Dash or Streamlit.

3. Add type annotations to the classes and functions you write so they're easy to read and test.

4. Use iterators and generators to write a data processing pipeline that fits in nicely with the existing Python tooling such as itertools but that is also memory-efficient due to using generators.

5. If you want to store the data you retrieve locally in a database, you can use a context manager to manage opening and closing the database connection like I show in the class.

6. Use lamdba functions to define and apply simple filters on your data.

You can take this assignment as far as you like, but I suggest to start simple and as a first step, write a script that retrieves some data from the API using concurrency. After that, expand the program step by step to include processing, filters, and optionally, a basic GUI interface.

To help you get started, you can find all the code examples I've shown during the class as a download here. In case you have any questions, just let me know!

Sharing Your Work

Once you've created the application, post your work in a comment here so we can see how you've set it up! Examples of things you could share:

A link to a Git repository containing the code you wrote.
A description of the main challenges you faced while building this project.