# CI | Tidbits | Test Intelligence

> **Bite-sized how-to** | ~10 min setup

---

## What is Test Intelligence?

Harness Test Intelligence (TI) uses AI-powered call graph analysis to figure out which tests are actually affected by your code changes — and only runs those. Everything else gets skipped.

The result: faster CI pipelines without sacrificing confidence. Harness typically reports **70–90% reduction in test execution time** on large Java codebases.

**How it works:**
1. On the first run, TI executes your full test suite and builds a call graph (a map of which code each test touches).
2. On every subsequent run, Harness compares the changed files in your PR/push against that call graph.
3. Only tests that touch changed code are selected and run. Everything else is intelligently skipped.

---

## Prerequisites

Before you start, make sure you have:

- A Harness CI pipeline (Cloud or self-hosted runner)
- A Java project using **Maven** (surefire plugin) or **Gradle**
- A Git connector pointed at your repo
- Test Intelligence enabled on your Harness account (available on Team and Enterprise plans)

> **Note:** The first pipeline run after enabling TI will always run the full test suite — this is intentional. TI needs that baseline to build its call graph.

---

## Step 1 — Replace your `Run` step with a `Tests` step

Test Intelligence only works through the dedicated **Tests** step. You cannot enable it on a regular `Run` step.

In the **Pipeline Studio** (visual editor):

1. Open your CI stage and locate your existing test step.
2. Delete (or disable) the existing `Run` step that runs your tests.
3. Click **Add Step → Test Intelligence**.

---

## Step 2 — Configure the Run Tests step

Fill in the step fields as follows.

### For Maven

| Field | Value |
|---|---|
| **Command** | `mvn test` |
| **Test Report Paths** | `**/*.xml` (Surefire default output location) |
| **Intelligence Mode** | ✅ Enabled |

---

## Step 3 — Pipeline YAML reference

If you prefer to work in YAML directly, here are complete `RunTests` step definitions.

### Maven — YAML

```yaml
- step:
    type: RunTests
    name: Run Tests with TI
    identifier: Run_Tests_TI
    spec:
      connectorRef: <your_docker_or_k8s_connector>
      image: maven:3.9-eclipse-temurin-17
      language: Java
      buildTool: Maven
      args: test
      runOnlySelectedTests: true
      reports:
        type: JUnit
        spec:
          paths:
            - "**/*.xml"
      resources:
        limits:
          memory: 1Gi
          cpu: "1"
```

> **Tip:** Replace `<your_docker_or_k8s_connector>` with your actual connector identifier. For Harness Cloud runners, you can omit `connectorRef` and `image`.

---

## Step 4 — Enable caching (strongly recommended)

TI stores its call graph in Harness's backend, but your **Maven/Gradle dependency cache** should be handled separately for fastest builds. Add a **Save Cache** and **Restore Cache** step to your pipeline around the `RunTests` step.

```yaml
# Before RunTests step
- step:
    type: RestoreCacheS3   # or RestoreCacheGCS / RestoreCacheHarness
    name: Restore Maven Cache
    identifier: Restore_Cache
    spec:
      connectorRef: <your_s3_connector>
      bucket: my-ci-cache
      key: maven-{{ checksum "pom.xml" }}
      archiveFormat: Tar

# After RunTests step
- step:
    type: SaveCacheS3
    name: Save Maven Cache
    identifier: Save_Cache
    spec:
      connectorRef: <your_s3_connector>
      bucket: my-ci-cache
      key: maven-{{ checksum "pom.xml" }}
      sourcePaths:
        - /root/.m2
      archiveFormat: Tar
```

---

## Step 5 — Run your pipeline and verify

1. **Trigger your pipeline.** The first run will execute all tests — this is expected behavior while TI builds its initial call graph.

2. **Make a small code change** in a subsequent commit (e.g., edit one class). Push and trigger again.

3. **Check the Run Tests step output.** You should see a TI summary like:

   ```
   Test Intelligence Report
   ─────────────────────────────────────
   Total tests:        482
   Tests selected:      17
   Tests skipped:      465
   Time saved:         ~8 min 34 sec
   ```

4. **Review the TI tab** in the Harness execution view. It shows which tests were selected, which were skipped, and the overall time savings trend across runs.

---

## Common Issues & Tips

**TI isn't selecting fewer tests**
- Confirm `runOnlySelectedTests: true` is set in your step spec.
- Check that your test report paths match where your build tool actually outputs XML files.
- Remember: the first run always executes all tests. You need at least two runs to see selection in action.

**Maven Surefire isn't generating XML reports**
- Add `-Dsurefire.useFile=true` to your `args` if you're seeing missing reports.
- Ensure your `pom.xml` includes the `maven-surefire-plugin` at version `2.22+` for JUnit 5 compatibility.

**Gradle tests not being detected**
- Add `useJUnitPlatform()` to your `test` block in `build.gradle` if using JUnit 5.
- Make sure the `--tests` argument isn't hardcoded in your Gradle test task, as TI injects its own test filter.

**Pipeline fails on the `RunTests` step with a connector error**
- Double-check your `connectorRef` value matches the connector identifier in your Harness project settings.

---

## What's next?

- **Test Splitting** — Combine TI with parallelism to split the selected tests across multiple containers for even faster runs.
- **Branch-level baselines** — TI maintains separate call graphs per branch, so PRs targeting `main` use `main`'s baseline.
- **Test Reports** — Explore the full test reporting dashboard in Harness to track flaky tests and failure trends over time.

---

## Resources

- [Harness Developer Hub — Test Intelligence](https://developer.harness.io/docs/continuous-integration/use-ci/run-tests/test-intelligence/)
- [Run Tests step reference](https://developer.harness.io/docs/continuous-integration/use-ci/run-tests/run-tests-step-settings/)
- [Harness CI overview](https://developer.harness.io/docs/continuous-integration/)

# E-Commerce Application — Harness Test Intelligence Demo

A Java Spring Boot e-commerce platform with a comprehensive unit test suite
designed to demonstrate **Harness Test Intelligence (TI)** in a CI pipeline.

---

## Project Structure

```
src/
├── main/java/com/example/ecommerce/
│   ├── model/
│   │   ├── Product.java         — Product entity with stock management
│   │   ├── Customer.java        — Customer with loyalty tiers
│   │   ├── Order.java           — Order with lifecycle state machine
│   │   ├── OrderItem.java       — Line item with discount logic
│   │   ├── Coupon.java          — Coupon with validation & calculation
│   │   └── Address.java         — Embeddable address
│   ├── repository/              — Spring Data JPA repositories
│   ├── service/
│   │   ├── ProductService.java  — Inventory & search logic
│   │   ├── CustomerService.java — Registration, tiers, deactivation
│   │   └── OrderService.java    — Full order lifecycle + pricing
│   ├── util/
│   │   ├── PricingCalculator.java      — Tax, shipping, tier discounts
│   │   └── OrderNumberGenerator.java   — Sequential order numbers
│   └── exception/               — Custom exceptions
└── test/java/com/example/ecommerce/
    ├── model/                   — Unit tests for all model logic
    ├── service/                 — Mockito-based service tests
    └── util/                    — Utility class tests
```

---

## Test Coverage (~200+ tests)

| Test Class                 | Tests | What it covers                                |
|----------------------------|-------|-----------------------------------------------|
| `ProductTest`              | ~20   | Stock management, builder, validation          |
| `OrderItemTest`            | ~15   | Line totals, discount calculations             |
| `CouponTest`               | ~25   | Validity, discount types, caps, usage limits   |
| `AddressTest`              | ~12   | Formatting, US detection                       |
| `OrderTest`                | ~15   | Item management, cancellation/shipping logic   |
| `PricingCalculatorTest`    | ~30   | Tax by country, shipping tiers, tier discounts |
| `OrderNumberGeneratorTest` | ~15   | Format validation, uniqueness, date extraction |
| `ProductServiceTest`       | ~30   | CRUD, search, stock update, deactivation       |
| `CustomerServiceTest`      | ~25   | Registration, tier upgrades, deactivation      |
| `OrderServiceTest`         | ~30   | Order creation, cancellation, lifecycle        |

---

## Running the Tests

```bash
# Run all tests
mvn test

# Run a specific test class
mvn test -Dtest=ProductServiceTest

# Run a specific test method
mvn test -Dtest=PricingCalculatorTest#calculateTax_forKnownCountries
```

---

## How to Use with Harness Test Intelligence

1. Import the `.harness/pipeline.yaml` into your Harness project
2. Connect your GitHub repo
3. Push a code change — e.g., modify `PricingCalculator.java`
4. Harness TI will **only run** `PricingCalculatorTest` (and related tests)
   instead of the full ~200-test suite
5. Compare run time vs. full suite to see the savings

### Example TI Savings

| Change Made                     | Full Suite | With TI        |
|---------------------------------|------------|----------------|
| Edit `PricingCalculator.java`   | ~45s       | ~8s (1 class)  |
| Edit `Coupon.java`              | ~45s       | ~10s (2 classes)|
| Edit `OrderService.java`        | ~45s       | ~15s (3 classes)|
| Edit `README.md` (no .java)     | ~45s       | ~2s (0 tests)  |

---

## Tech Stack

- **Java 17** + **Spring Boot 3.2**
- **JUnit 5** + **Mockito** + **AssertJ**
- **H2** in-memory database (tests)
- **Maven** build tool
- **Harness CI** with Test Intelligence
