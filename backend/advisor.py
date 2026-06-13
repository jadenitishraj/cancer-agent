def get_clinical_response(query: str) -> str:
    """Generates structured medical advisory responses for oncology queries."""
    q = query.lower()
    
    if "egfr" in q or "lung" in q:
        return (
            "🧬 **EGFR-Mutated NSCLC Clinical Advisory**:\n\n"
            "1. **First-Line Standard of Care**: Osimertinib (Tagrisso) is the preferred Level 1 "
            "recommendation. It targets sensitizing mutations (Exon 19 del, L858R) and crosses the blood-brain barrier.\n"
            "2. **Resistance Mechanisms**: Emergence of C797S mutations in exon 20 or MET oncogene amplification "
            "are common bypass pathways.\n"
            "3. **Next Steps**: Patients progressing on Osimertinib should be screened for MET amplification to "
            "consider combination trials (e.g., Savolitinib + Osimertinib)."
        )
    elif "brca" in q or "breast" in q:
        return (
            "🧬 **BRCA-Mutated Breast Cancer Advisory**:\n\n"
            "1. **Mechanism**: Germline BRCA1/2 mutations cause homologous recombination deficiency (HRD), "
            "impairing double-stranded DNA repair.\n"
            "2. **Targeted Therapy**: PARP inhibitors (Olaparib, Talazoparib) leverage synthetic lethality to target HRD cells.\n"
            "3. **Chemotherapy Selection**: Conveys high sensitivity to platinum-based doublets (carboplatin, cisplatin).\n"
            "4. **Trials**: Screen for phase II/III trials evaluating PARP inhibitor combinations (e.g., with anti-VEGF)."
        )
    elif "immunotherapy" in q or "checkpoint" in q:
        return (
            "🛡️ **Cancer Immunotherapy Guide**:\n\n"
            "1. **Mechanism**: Blocks PD-1 (Pembrolizumab, Nivolumab), PD-L1 (Atezolizumab), or CTLA-4 (Ipilimumab) "
            "to reactivate T-cell anti-tumor responses.\n"
            "2. **Biomarkers**: PD-L1 Tumor Proportion Score (TPS), Microsatellite Instability-High (MSI-H), and "
            "Tumor Mutational Burden (TMB) predict response.\n"
            "3. **Toxicity**: Monitor for immune-related adverse events (colitis, pneumonitis, thyroiditis) requiring steroids."
        )
    elif "trial" in q or "study" in q:
        return (
            "🧪 **Clinical Trial Matching Protocol**:\n\n"
            "1. **Inclusion Criteria**: Verify cancer stage, biomarker profile, and previous therapy lines.\n"
            "2. **ECOG Status**: Standard trials require ECOG 0 or 1 performance status; ECOG 2+ requires special protocols.\n"
            "3. **Phase Guide**: Phase I (Safety/Dose), Phase II (Efficacy), Phase III (Comparison with standard care).\n"
            "4. **Action**: Query ClinicalTrials.gov using NCT identifiers and cross-check exclusion criteria."
        )
    
    return (
        "🩺 **OncoAgent Clinical Assistant**:\n\n"
        "Welcome! I am OncoAgent, your oncology research AI companion. I can assist with queries on:\n"
        "- **Targeted Genomics** (e.g., EGFR, BRCA1/2, KRAS, ALK)\n"
        "- **Clinical Trial Matching** & eligibility criteria (ECOG status)\n"
        "- **Immunotherapies** and molecular checkpoint inhibitors\n\n"
        "How can I assist your clinical search or case analysis today?"
    )
