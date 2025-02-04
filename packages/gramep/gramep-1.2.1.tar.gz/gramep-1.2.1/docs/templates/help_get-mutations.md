<div class="termy" data-termynal data-ty-macos data-ty-title="shell"><span data-ty="input" data-ty-prompt="$">gramep get-mutations --help</span><span data-ty>                                                                                                                                                                                              
   Usage: gramep get-mutations [OPTIONS]                                                                                                       
                                                                                                                                             
   Perform k-mers analysis and optionally generate a report.                                                                                   
                                                                                                                                               
  ╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
  │ *  --rpath                  TEXT     📂 Path to reference sequence. [default: None] [required]                                            │
  │ *  --spath                  TEXT     📂 Path to sequence. [default: None] [required]                                                      │
  │ *  --save-path              TEXT     📂 Path to save results. [default: None] [required]                                                  │
  │ *  --word           -w      INTEGER  📏 Word size. [default: None] [required]                                                             │
  │ *  --step           -s      INTEGER  ⏭ Step size. [default: None] [required]                                                              │
  │    --apath                  TEXT     📂 Path to annotation file. [default: None]                                                          │
  │    --mode                   TEXT     ✔ Mode. Options: snps (only SNPs) or indels (indels and SNPs). [default: snps]                       │
  │    --snps-max               INTEGER  ✔ Max number of SNPs allowed. [default: 1]                                                           │
  │    --dictonary      -d      TEXT     🧬📖 DNA dictionary. [default: DNA]                                                                  │
  │    --create-report                   📋 Create report.                                                                                    │
  │    --chunk-size             INTEGER  📦 Chunk size for loading sequences. [default: 100]                                                  │
  │    --help                            Show this message and exit.                                                                          │
  ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
  
   
   <br></span></div>