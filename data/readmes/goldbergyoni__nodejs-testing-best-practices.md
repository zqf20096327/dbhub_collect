![Header](./graphics/testing-best-practices-banner.png 'Node.js Testing Best Practices')

<br/>

## A detailed guide to modern testing with Node.js

**1. ✅ 50+ Best Practices List -** Detailed instructions on how to write modern tests in the RIGHT way

**2. 📊 Example application -** A Complete showcase of a typical Node.js backend with performant tests setup (40 tests in 5 seconds! including database!)

**3. 🚀 Advanced topics -** Go well beyond the basics. This guide covers hot topics like testing with data(base), testing interactions with external services including contracts, testing with message queues and more

<br/><br/>

## Authors

<img width="50" height="50" src="graphics/team/yoni.jpg"/>

**Yoni Goldberg**

Speaking about this soon at the following conferences: City.js Athens 🇬🇷, React.Next Tel-Aviv 🇮🇱, Render Atlanta 🇺🇸

<img width="50" height="50" src="graphics/team/michael.jpg"/>

**Michael Salomon**
            
      
<img width="50" height="50" src="graphics/team/daniel.jpg"/>

**Daniel Gluskin**

<br/>

_Lessons Written in Blood: Hard-Won Insights from Consulting with 50 Companies_

<br/><br/>

# `Table of contents`

- [`Strategy & Workflow`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-1-strategy-and-workflow) - Which tests should you write in 2025? (5 best practices)
- [`Database And Infrastructure Setup`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-2-infrastructure-and-database-setup) - Optimizing your DB, MQ and other infra for testing (6 best practices)
- [`Web Server Setup`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-3-web-server-setup) - Good practices for starting and stopping the backend API (3 best practices)
- [`The Test Anatomy`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-4-the-test-anatomy) - The bread and butter of a component test (6 best practices)
- [`Integration`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-5-integrations-with-other-services-and-apis) - Techniques for testing collaborations with 3rd party components (8 best practices)
- [`Dealing With Data`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-6-dealing-with-data) - Patterns and practices for testing the application data and database (8 best practices)
- [`Message Queue`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-7-message-queues) - Correctly testing flows that start or end at a queue (8 best practices)
- [`Mocking`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#section-8-mocking)(6 best practices)

<br/><br/>

### Athens workshop + Online course

**- 🧑‍🏫 Online course:** Learn all of these patterns & practices in a [comprehensive online course - On special sale until April 30th](https://testjavascript.com/)

**- 🇬🇷 Athens workshop:** [Attend my workshop in City.js Athens](https://greece.cityjsconf.org/) + Bonus: Get royal access to my online course

<br/><br/>

### Example Application

- [`Our Showcase`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#-example-application) - An example Node.js component that embodies selected list of important best practices

### Other Recipes

- [`More Examples And Platforms`](https://github.com/testjavascript/nodejs-integration-tests-best-practices#-recipes) - A list of more examples that cover more platforms and topics

<br/><br/><br/>

# ✅ Best Practices

<br/>

## **Section 1: Strategy and Workflow**

<br/>

### ⚪️ 1. Always START with integration/component tests

🏷&nbsp; **Tags:** `#strategic`

:white_check_mark: **Do:** No matter when testing starts, the first tests to write should be component tests. But what exactly are component/integration tests? They focus on testing an entire component (e.g., a microservice) as-is, through its API, with all layers included—database and al

[...截断...]

l—while faking anything extraneous. This approach delivers both high confidence (it's like the production environment!) and a great developer experience.

Why start here? When a new sprint or feature begins, the first known details are about the component's expected behavior. Developers can immediately outline what the API/MQ will receive and what kind of response it should return. Naturally, testing this public interface first makes the most sense. This powerful testing approach brings immense value: it is realistic, demands less effort than covering every function with tests, requires close to zero mocking, triggers high coverage, and keeps the tester focused on what truly matters

On the other hand, writing unit tests for inner functions before the overall outcome is clear is a wasted effort. Even classic TDD books emphasize this approach—check out the [the double verification loop model](https://miro.medium.com/max/700/0*c5ahAZusp87Bo6Io.jpg).

At the end of the day, every input and output of a component must be covered with component tests. This is the bread and butter of your testing strategy—the Swiss Army knife that catches 99% of the bugs. This strategy is known as the 'Testing Diamond'

![Component tests](/graphics/component-diagram.jpg 'Component Tests')

<br/><br/>

### ⚪️ 2. Run a very few E2E, selectively consider unit tests

🏷&nbsp; **Tags:** ``

:white\*check_mark: **Do:** Write just a tiny handful of E2E tests on top of component tests like 3-10, tests, maybe a couple more for larger components, but nothing beyond that. While "E2E" means different things to different testers, in a backend context, it refers to tests that run against live collaborators (i.e., multiple microservices) on a real infrastructure. Since component tests catch 99% of bugs, E2E tests should focus on different risks: configuration issues, misunderstandings with third-party services, infrastructure problems, and similar surprises. Catching these issues requires only a few well-placed tests

When are unit tests needed? Only when dealing with non-trivial logic or algorithms. If a module has significant complexity, isolating it from distractions can make testing easier. [This article greatly outlines when unit tests shine](https://blog.stevensanderson.com/2009/11/04/selective-unit-testing-costs-and-benefits/)

<br/><br/>

### ⚪️ 3. Cover features, not functions

🏷&nbsp; **Tags:** ``

Focus your tests on features, not just functions. Features represent the core behavior of your application—often reflected in API routes—and testing them ensures an automated focus on what truly matters. This approach also helps set the right priorities and often requires fewer tests than function-level testing.

Coverage reports are a great way to see which controllers, modules, and folders are exercised by tests. They help identify which critical features have been tested and, just as importantly, highlight gaps where essential functionality might still be missing. To verify meaningful coverage, compare test reports with requirements, check coverage reports to confirm key features are included, and ensure core routes and messages are covered by tests
<br/><br/>

### ⚪️ 4. Write the tests _during_ coding, never after

🏷&nbsp; **Tags:** `#strategic`

:white_check_mark: **Do:** Write tests when it's most convenient—before or during coding—but never after everything is built. Waiting too long means losing the anti-regression safety net that tests provide

Imagine a developer spends three hours writing great, fully working code (let’s call this point "A"). Then, she codes for six more hours, only to realize that a bug was introduced five hours ago. If she had written tests at point A, they would have caught the issue immediately, preventing wasted effort. Like in rock climbing, tests secure progress—the earlier they are written, the less risk of falling back due to regressions

Tests should also be designed for frequent execution, running every few minutes like a r