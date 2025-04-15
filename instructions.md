# Backend-test

Take-Home Project: Minimal Orders API with AWS Integration

Scenario:
You're building a minimal order processing API for a mobile app (React Native) that allows users to place orders for products. Your task is to build a small backend service that supports basic order management.

## Requirements

### Core API Endpoints

    POST /orders – Create a new order.
    GET /orders/{id} – Fetch details of a specific order.
    GET /orders – List all orders.
    DELETE /orders/{id} – Cancel/delete an order.

Each order should contain:

    id (UUID)
    userId
    items (array of { productId, quantity })
    status (e.g. "created", "cancelled")
    createdAt

### Tech Requirements

    Use any language/framework you're comfortable with (Node.js, Python, Go, Java, etc.).
    Store data in AWS DynamoDB, S3 or whichever storage you're more comfortable with (on AWS).
    Use AWS Lambda, Express or similar lightweight setup.
    Add a simple README with how to run it locally or deploy via AWS (even mock AWS if needed).

### Bonus (Optional)

    Include a basic authentication mechanism (e.g., simple token or mocked).
    Add test cases for your endpoints.
    Use of infrastructure-as-code (e.g., CDK, Terraform, or Serverless Framework).

### Evaluation Criteria

    Code structure & clarity
    API design & RESTful practices
    AWS usage (correct, minimal, and effective)
    Error handling & validation
    Testing (even basic)
    Documentation (README)

### Time Expectation

You should be able to complete the core API + AWS integration in 3–4 hours. Bonus parts are optional.

### Cost

This project shouldn't incur any cost but we know that sometime AWS is greedy, if you have any cost related to this project, we will reimburse you for a maximal cost of 20 euros.