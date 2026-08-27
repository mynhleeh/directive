# Deep Flow Tracing

## Tracing the Flow
When an intern asks how a specific feature works, trace the journey of data from input to output. 

### Step-by-Step Approach
1. **Identify the Entry Point**: Where does the request start? (e.g., a specific button click on the frontend, or an API endpoint in the backend like `POST /login`).
2. **Follow the Request**: What receives the request? (e.g., the Router or Controller).
3. **Trace the Logic**: Where does the Controller send the data? (e.g., the Service layer or a specific function).
4. **Data Access**: Does it interact with a database? (e.g., the Repository layer or ORM model).
5. **The Response**: How does the data get back to the user?

## Explaining the Flow
- Present the flow in a numbered list (1, 2, 3...) or a sequence diagram.
- Explain *why* data is passed to a certain layer, not just *that* it is passed.
- **Example**: "1. The `UserController` receives your login details. 2. It hands them over to the `AuthService` because the Controller's job is just to route traffic, while the Service does the heavy lifting of checking passwords."

## Mentoring on Debugging
If the intern is stuck trying to understand the flow, suggest where they can add `console.log()` / `print()` statements or where they should place a breakpoint in their IDE to see the data at that specific moment.
