# AeroForge Intelligence

**Aerospace material, TIG weld and property-risk decision support**  
K Shiva Teja · Roll No. 25EG512B02 · IT-B

## Functional modules

- JWT/BCrypt user access
- source-labelled aerospace material reference catalogue with 14 alloy/condition records
- credited public aerospace/material imagery linked to each original image record
- physical material-batch registration in TiDB
- TIG weld capture and automatic heat-input calculation
- measured mechanical-test register, separate from estimates
- traceable property/risk screening using the selected alloy's published baseline
- high-risk alerts and acknowledgement
- dashboard charts, analytics and CSV reports
- clear **reference / measured / estimated** data labels

The frontend has separate pages for Overview, Reference Catalogue, Material Batches, Weld Records, Mechanical Tests, AI Prediction, Risk Alerts, Reports & Analytics, and Data Provenance.

## Technology

Java 21 · Spring Boot · Spring Security · JWT · Flyway · TiDB · React 19 · Vite · Axios · Recharts

## Run on macOS

```bash
docker start aeroforge-tidb
docker ps --filter name=aeroforge-tidb
```

Backend:

```bash
cd backend
./mvnw spring-boot:run
```

Flyway automatically applies migrations V2 and V3 and loads fourteen source-labelled reference alloys. It does not create fake physical batches or laboratory tests.

Frontend (second terminal):

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>.

## Demonstration workflow

1. Sign in.
2. Review Reference Catalogue and source links.
3. Register an actual or clearly labelled training batch.
4. Record TIG current, voltage and travel speed.
5. Add laboratory values only when a real report is available.
6. Run an estimate using the weld, HAZ width and repair count.
7. Review risks, alerts and analytics.
8. Export a CSV prediction report.

## Scientific boundary

This is a functional academic decision-support system—not flight-certified software. The estimator is a transparent rule-based screening model, not a trained ML model and not a model trained on proprietary ISRO data. It starts from the selected catalogue alloy's source-labelled nominal tensile, yield and elongation values and applies explicit TIG heat-input, HAZ-width and repair penalties. Its confidence field indicates rule coverage, not validated predictive accuracy. Catalogue values are representative published references, not minimum design allowables. Flight hardware requires approved specifications, traceable certificates, qualified processes, testing and authorized engineering sign-off.

## Data integrity

- **Reference:** public NASA/NIST technical sources; comparison use only.
- **Measured:** entered only from a real certificate or laboratory report.
- **Estimated:** calculated screening output; never displayed as certified evidence.
- No fake physical batch, supplier certificate, tensile test, or proprietary ISRO record is preloaded.
- Catalogue images are credited public records and link to their original Wikimedia Commons file pages.

## ISRO research alignment

The project responds to the publicly described ISRO VSSC RESPOND Basket 2025 topic **“Material Property Prediction Using Machine Learning & Deep Learning Models”** under Structures and AI, concerning TIG-welded thin-shell launch-vehicle structures, welding parameters, HAZ morphology, repairs and mechanical properties. AeroForge is not an ISRO product and is not endorsed by ISRO.

