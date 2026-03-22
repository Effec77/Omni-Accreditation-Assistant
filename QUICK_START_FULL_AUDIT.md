# Quick Start: Full NAAC Audit

## 🚀 How to Run a Full NAAC Audit

### Step 1: Start the Backend
```bash
cd accreditation_copilot/api
python start_api.py
```
Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Step 2: Start the Frontend
```bash
cd accreditation_copilot/frontend
npm run dev
```
Wait for: `Local: http://localhost:3000`

### Step 3: Upload Your SSR Document
1. Open browser: http://localhost:3000
2. Click the **Upload** button (📤 icon)
3. Select your SSR PDF (e.g., `Comprehensive_University_A+_SSR.pdf`)
4. Files will auto-upload to backend

### Step 4: Ingest the Document
1. Click **"Ingest Files"** button
2. Wait for confirmation: "Files ingested successfully!"
3. You'll see: ✓ Ingested (green checkmark)

### Step 5: Run Full NAAC Audit
1. Click the green **"Run Full NAAC Audit"** button
2. Wait 2-5 minutes (evaluating all 11 criteria)
3. View comprehensive results!

## 📊 What You'll See

### Overall Grade Card
- **CGPA**: Your score on 4-point scale (e.g., 3.42)
- **Letter Grade**: A++, A+, A, B++, B+, B, C, or D
- **Accreditation Status**: Accredited or Not Accredited

### Summary Stats
- Total Criteria Evaluated: 11
- Total Metrics Evaluated: 11
- Framework: NAAC

### Improvement Roadmap
- Actionable suggestions to improve your grade
- Focus areas based on weak criteria
- Specific recommendations for high-impact improvements

### Criterion Breakdown
Detailed view of each of the 7 main NAAC criteria:
- **Criterion 1** (100 points): Curricular Aspects
- **Criterion 2** (350 points): Teaching-Learning & Evaluation ⭐ HIGHEST WEIGHT
- **Criterion 3** (200 points): Research, Innovations & Extension
- **Criterion 4** (100 points): Infrastructure & Learning Resources
- **Criterion 5** (100 points): Student Support & Progression
- **Criterion 6** (100 points): Governance, Leadership & Management
- **Criterion 7** (50 points): Institutional Values & Best Practices

Each criterion shows:
- Current grade (A+, A, B+, etc.)
- Average grade points (0-4 scale)
- Weight in points
- Progress bar visualization
- Individual metrics evaluated

## 🎯 Understanding Your Results

### CGPA Scale
- **3.51-4.00**: A++ (Outstanding) 🌟
- **3.26-3.50**: A+ (Excellent) ⭐
- **3.01-3.25**: A (Very Good) ✨
- **2.76-3.00**: B++ (Good)
- **2.51-2.75**: B+ (Above Average)
- **2.01-2.50**: B (Average)
- **1.51-2.00**: C (Below Average)
- **0.00-1.50**: D (Poor)

### Accreditation Threshold
- **CGPA ≥ 1.51**: Accredited ✅
- **CGPA < 1.51**: Not Accredited ❌

### Key Insight
You can have mixed criterion grades (A+, A, B+) and still achieve overall A+ if:
- Strong performance in **Criterion 2** (350 points - highest weight)
- Strong performance in **Criterion 3** (200 points - second highest)
- Decent performance across other criteria

## 🧪 Testing the Endpoint Directly

Run the test script:
```bash
cd accreditation_copilot
python test_full_audit_endpoint.py
```

This will:
- Call the API endpoint directly
- Display results in terminal
- Save full JSON to `full_audit_result.json`

## 🔍 Troubleshooting

### "Please upload and ingest files first"
- Make sure you clicked "Ingest Files" after uploading
- Wait for green ✓ Ingested confirmation

### Backend not responding
- Check backend is running: `cd accreditation_copilot/api && python start_api.py`
- Verify port 8000 is not in use

### Frontend not loading
- Check frontend is running: `cd accreditation_copilot/frontend && npm run dev`
- Verify port 3000 is not in use

### Audit takes too long
- Full audit evaluates 11 criteria - this is normal
- Typical time: 2-5 minutes
- Don't refresh the page while running

## 📁 Test Data Location

Your test SSR document should be at:
```
D:/NAAC_Test_PDFs/Comprehensive_University_A+_SSR.pdf
```

## 🎓 Next Steps After Full Audit

1. **Review Weak Criteria**: Focus on criteria with grade < B+
2. **Prioritize High-Weight Criteria**: Criterion 2 and 3 have biggest impact
3. **Follow Improvement Suggestions**: Implement recommended actions
4. **Re-run Audit**: After improvements, run full audit again to track progress
5. **Export Results**: (Future feature) Export comprehensive report

## 💡 Pro Tips

1. **One-Time Ingestion**: Once ingested, you can run multiple audits without re-ingesting
2. **Focus on Weights**: Improving Criterion 2 (350 points) has 3.5x more impact than Criterion 7 (50 points)
3. **Realistic Expectations**: A+ requires CGPA 3.26+, which means strong performance across most criteria
4. **Documentation Quality**: Better evidence in SSR = higher confidence scores = better grades

## 🚨 Important Notes

- Framework documents are already ingested (1,315 chunks from NAAC/NBA PDFs)
- System uses official NAAC weights (1000 points total)
- Grading is based on weighted average, not individual criterion grades
- Minimum CGPA 1.51 required for accreditation

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] SSR document uploaded
- [ ] Files ingested (green ✓ shown)
- [ ] "Run Full NAAC Audit" button clicked
- [ ] Results displayed with CGPA and grade
- [ ] Criterion breakdown visible
- [ ] Improvement suggestions shown

---

**Ready to test?** Follow the 5 steps above and you'll have your comprehensive NAAC grade in minutes! 🎉
