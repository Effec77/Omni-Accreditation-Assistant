# CRITICAL ISSUE: Framework Data Missing

## Problem Discovered

The backend only works with criterion 3.2.1 because **there are NO framework documents ingested**.

### Evidence:
```
Framework chunks in database: 0
Institution chunks in database: 59
```

The `accreditation_copilot/data/raw_docs/naac/` folder is empty (only has .gitkeep).

## Why This Matters

The system works by:
1. **Framework Index**: Contains NAAC/NBA requirements for each criterion
2. **Institution Index**: Contains your university's SSR document
3. **Comparison**: Compares institution evidence against framework requirements

Without framework data, the system can't properly evaluate ANY criterion.

## Why 3.2.1 "Works"

3.2.1 appears to work because:
- It uses hardcoded keywords from `naac_metric_map.yaml`
- These keywords were manually tuned for 3.2.1
- It's not actually comparing against official NAAC requirements

## Solution

You need to add NAAC framework documents to:
```
accreditation_copilot/data/raw_docs/naac/
```

### What Documents to Add:

1. **NAAC Manual for Universities** - The official NAAC accreditation manual that describes all criteria
2. **NAAC SSR Guidelines** - Guidelines that explain what evidence is needed for each criterion
3. **Criterion-specific documents** - Any NAAC documents that detail requirements for criteria 1.2.1, 2.1.1, 3.2.1, 3.3.1, 3.4.1, 4.1.2, 5.1.1, 6.2.2, 7.1.2

### Where to Find These:

- NAAC Official Website: https://www.naac.gov.in/
- Look for "Manuals" or "Guidelines" section
- Download PDFs for University accreditation

### After Adding Documents:

1. Place PDF files in `accreditation_copilot/data/raw_docs/naac/`
2. Run the framework ingestion script (there should be one for ingesting framework docs separately from institution docs)
3. Verify framework chunks are created:
   ```bash
   python accreditation_copilot/check_framework_data.py
   ```

## Temporary Workaround

Until you add framework documents, the system will continue to rely on hardcoded keywords in `naac_metric_map.yaml`. You could:

1. Update the keyword lists for each criterion in that file
2. But this is NOT recommended - it's better to use actual NAAC documents

## UI Fixes Completed

✅ Dropdown with checkboxes - DONE
✅ Multi-criterion selection - DONE  
✅ Search functionality - DONE
✅ Ingestion persistence tracking - DONE

## Next Steps

1. **URGENT**: Add NAAC framework documents to `data/raw_docs/naac/`
2. Ingest framework documents
3. Test all 11 criteria
4. The system will then work properly for all criteria

---

**Bottom Line**: The system architecture is correct, but it's missing the critical framework data needed to evaluate criteria properly.
